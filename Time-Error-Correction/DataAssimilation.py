# -*- coding: utf-8 -*-
"""Contains methods for data assimilation."""


import numpy as np
from scipy import stats     
import math                 
import EnsembleOperations 
import random 
import MiscFunctions
import matplotlib.mlab as mlab
import Graphics





def get_posterior(ensembleValues, observation, observationError):
    """
    Assuming normality, uses Bayes' Rule to find the posterior distribution from an ensemble/prior and an observation distribution.
    
    Takes ensembleValues (observed only, as returned by get_observed_values_from_ensemble), observation as array of variable values in same order as ensemble, and assumed error in observations.
    """
    #Convenience
    numberOfVariables = len(ensembleValues)   
    
    #Priors    
    ensembleMeans = [np.mean(valueList) for valueList in ensembleValues]
    ensembleSpreads = [np.std(valueList, ddof=1) for valueList in ensembleValues]
    
    #Compute Posterior 
    posteriorMeans = []
    posteriorSpreads = []
    for variable in range(numberOfVariables):
        #If there is no spread in the ensemble, it is completely certain and we don't need to adjust it.
        if ensembleSpreads[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(ensembleMeans[variable])
        #If there is no spread in the observation likelihood, we are completely certain it is accurate and we can set the ensemble to its value.
        elif observationError[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(observation[variable])
            
        #If there is spread in both ensemble and observation:
        #                 ______________________
        #                /__________1___________
        #std-post =     /____1____  + ___1___    
        #             \/(std-pri)^2  (std-lik)^2
        # and
        #
        #mean-post = (std-post)^2 *   ___mean-pri___  +  ____obs____
        #                              (std-pri)^2       (std-lik)^2
        #
        #where pri is prior, obs is observed (lik is observation likelihood), and post is posterior
        
        else:
            spread = ensembleSpreads[variable]
            observationLikelihoodError = observationError[variable]
            posteriorSpread = math.sqrt(1/((spread)**-2 + (observationLikelihoodError)**-2))
            posteriorSpreads.append(posteriorSpread)
            posteriorMeans.append((posteriorSpreads[variable]**2)*(ensembleMeans[variable]*ensembleSpreads[variable]**-2 + observation[variable]*observationError[variable]**-2))
               
    return posteriorSpreads, posteriorMeans
    



    
def get_state_inc(ensembleValues, observationIncrements, index):
    """
    Regresses observation increments for one variable onto other variables.

    Takes ensembleValues in full, observation increments for one variable, and the index(position in ensembleValues) of the observed variable.    
    """
    stateIncrements = []
    for unobserved in range(len(ensembleValues)):
        slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleValues[index][1],ensembleValues[unobserved][1])
        #THIS CODE OVERRIDES THE REGRESSION.
        if index == unobserved:
            slope = 1
        else:
            slope = 0
        stateIncrements.append(list(np.array(observationIncrements)*slope))  #Multiplies all observation increments by slope.
    return stateIncrements
  

      
    
    
def apply_state_inc(ensembleValues, stateIncrements):
    """
    Applies state increments from one variable generated by get_state_inc.
    """
    newEnsembleValues = EnsembleOperations.copy_ensemble_values(ensembleValues)
    for var in range(len(stateIncrements)):
        newEnsembleValues[var][1] = [newEnsembleValues[var][1][point] + stateIncrements[var][point] for point in range(len(ensembleValues[var][1]))]
    return newEnsembleValues





def obs_inc_EAKF(ensembleValues, posteriorMean, posteriorSpread):
    """
    Calculates observation increments for one variable based on prior and posterior distributions.
    
    Takes one list of values i.e. ensembleValues[i] and information about posterior.
    Returns list of observation increments.
    """
    #Priors        
    ensembleMean = np.mean(ensembleValues)
    ensembleSpread = np.std(ensembleValues, ddof=1)
    observedIncrements = []
    meanDifference = posteriorMean - ensembleMean
    spreadRatio = posteriorSpread / ensembleSpread
    for point in ensembleValues:
        newValue = point + meanDifference
        distanceFromPosteriorMean = newValue - posteriorMean
        distanceFromPosteriorMean *= spreadRatio
        observedIncrements.append(posteriorMean + distanceFromPosteriorMean - point)
    return observedIncrements
        
        
        
        
def obs_inc_EnKF(ensembleValues, observation, observationError, posteriorMean, posteriorSpread):
    """
    Calculates observation increments for one variable based on prior and posterior distributions.

    Takes one list of values i.e. ensembleValues[i], observation in one variable, and information about posterior.
    Returns list of observation increments.
    """
#    #Priors
#    ensembleSpread = np.std(ensembleValues, ddof=1)    
#    #Generate perturbed observations
#    perturbedObservations = [random.gauss(observation, observationError) for i in ensembleValues]
#    #Adjust perturbed obs to observation mean.    
#    newPerturbedObservations = [i - np.mean(perturbedObservations) + observation for i in perturbedObservations]
#    newEnsemble = [posteriorSpread * (ensembleValues[i]/ensembleSpread + newPerturbedObservations[i]/observationError) for i in range(len(ensembleValues))]
    #THE FOLLOWING CODE IS EXPERIMENTAL
    newEnsemble = [random.gauss(posteriorMean, posteriorSpread) for i in range(len(ensembleValues))]
    return [newEnsemble[i] - ensembleValues[i] for i in range(len(newEnsemble))]




def obs_inc_rank_histogram(ensembleValues, observationLikelihood, rectangularQuadrature):
    """
    Calculates observation increments for one variable using the RHF on ensemble.
    
    Takes one list of values i.e. ensembleValues[i], observation in one variable, and observation likelihood as a list of likelihood with length equal to that of ensembleValues.
    Returns list of observation ecrements of equal length to ensembleValues.
    """
    for i in observationLikelihood:
        if i == 0:
            i = 0.05
    #Priors
    ensembleSpread = np.std(ensembleValues, ddof=1)
    ensembleLength = len(ensembleValues)
    sortedEnsemble, indices = MiscFunctions.sort_indices(ensembleValues)
    newObservationLikelihood = [observationLikelihood[indices[i]] for i in range(ensembleLength)]
    observationLikelihood = newObservationLikelihood[:]
    likelihoodDensity = [(observationLikelihood[i+1] + observationLikelihood[i])/2 for i in range(len(observationLikelihood)-1)]
    #print(ensembleLength, max(ensembleValues))
    
    #Compute partial Gaussian kernels for tails of prior.    
    distanceForUnitSpread = -1 * MiscFunctions.weighted_norm_inverse(1, 0, 1, 1/(ensembleLength + 1))
    leftMean = sortedEnsemble[0] + distanceForUnitSpread * ensembleSpread
    leftStandardDeviation = ensembleSpread
    rightMean = sortedEnsemble[-1] - distanceForUnitSpread * ensembleSpread
    rightStandardDeviation = ensembleSpread
    
    #Assume flat tails in likelihood. TODO: Allow for Gaussian tails (should only be relevant for nearly Gaussian likelihoods.)
    leftProductWeight = observationLikelihood[0]    
    rightProductWeight = observationLikelihood[-1]
    #Get the mass in between each bin.

        
    mass = np.array([leftProductWeight/(ensembleLength + 1)] + [likelihoodDensity[i]/(ensembleLength+1) for i in range(len(likelihoodDensity))] + [rightProductWeight/(ensembleLength + 1)])
    
    #Get height and normalize mass for trapezoidal.
    height = np.array([-1 if sortedEnsemble[i+1]==sortedEnsemble[i] else 1/((ensembleLength+1)*(sortedEnsemble[i+1]-sortedEnsemble[i])) for i in range(len(sortedEnsemble)-1)])
    massSum = sum(mass)  
    mass /= massSum
    
    #Get weight for normalized partial Gaussian tails. TODO: Descriptive names
    leftAmp = leftProductWeight / massSum
    rightAmp = rightProductWeight / massSum
    
    #Get cumulativemass at each bin bound (CDF)
    cumulativeMass = [0]
    for i in range(len(mass)):
        cumulativeMass.append(cumulativeMass[i] + mass[i])
        
    #Searching for boxes for each ensemble member. 
    #lowestBox = 0          #Updated so we don't have to search boxes we've already passed.     
 
    newEnsemble = []
    for i in range(ensembleLength):
        found = False
        passedMass = (i+1)/(ensembleLength + 1)         #The amount of mass before each ensemble member.
        if passedMass < cumulativeMass[1]:          #If it's in the left tail
            newEnsemble.append(MiscFunctions.weighted_norm_inverse(leftAmp, leftMean, leftStandardDeviation, passedMass))
            found = True
        elif passedMass > cumulativeMass[-2]:       #If it's in the right tail
            newEnsemble.append(MiscFunctions.weighted_norm_inverse(rightAmp, rightMean, rightStandardDeviation, 1-passedMass))
            newEnsemble[-1] = 2*rightMean - newEnsemble[-1]
            found = True
        else:                                       #If it's in one of the uniform boxes in the middle.
            for cumulativeMassIndex in range(2, len(cumulativeMass)):  #Ignore mass after last ensemble point.
                if passedMass >= cumulativeMass[cumulativeMassIndex - 1] and passedMass <= cumulativeMass[cumulativeMassIndex] and not found:     #If the mass is greater than the total mass up to a point but less than the total mass after a point: 
                
                    if rectangularQuadrature:
                        ensemblePointIndex = cumulativeMassIndex - 2    #The index of the ensemble point to the left of the area and also of the height of the bin.
                        newEnsemble.append(sortedEnsemble[ensemblePointIndex] + (passedMass-cumulativeMass[cumulativeMassIndex-1])/(cumulativeMass[cumulativeMassIndex] - cumulativeMass[cumulativeMassIndex-1])*(sortedEnsemble[ensemblePointIndex+1] - sortedEnsemble[ensemblePointIndex]))
                        found = True
                    else:
                        #We're using trapezoidal quadrature to get the new point. 
                        #box is index of cumulative mass, box - 1 is ensemble point
                        ensemblePointIndex = cumulativeMassIndex - 2    #The index of the ensemble point to the left of the area and also of the height of the bin.
                        leftHeight = height[ensemblePointIndex] * observationLikelihood[ensemblePointIndex]
                        rightHeight = height[ensemblePointIndex] * observationLikelihood[ensemblePointIndex + 1]
                        #Solve a quadratic to get its roots.
                        a = 0.5 * (rightHeight - leftHeight)/(sortedEnsemble[ensemblePointIndex + 1] - sortedEnsemble[ensemblePointIndex])      #dy/dx is the x^2 term.
                        b = leftHeight          #leftHeight (y-intercept) is x term
                        c = cumulativeMass[cumulativeMassIndex] - passedMass    #The constant +C is the mass remaining under the trapezoid.
                        root1, root2 = MiscFunctions.solve_quadratic(a, b, c)
                        root1 += sortedEnsemble[ensemblePointIndex]
                        root2 += sortedEnsemble[ensemblePointIndex]
                        if root1 >= sortedEnsemble[ensemblePointIndex] and root1 <= sortedEnsemble[ensemblePointIndex + 1]:
                            newEnsemble.append(root1)
                            found = True
                        elif root2 >= sortedEnsemble[ensemblePointIndex] and root2 <= sortedEnsemble[ensemblePointIndex + 1]:
                            newEnsemble.append(root2)
                            found = True
                        else:
                            raise ValueError("Rank Histogram Filter was unable to get a satisfactory root for trapezoidal interpolation.")
                elif cumulativeMass[cumulativeMassIndex - 1] > cumulativeMass[cumulativeMassIndex]:
                    print(cumulativeMass[cumulativeMassIndex - 1], ">", cumulativeMass[cumulativeMassIndex])
                    
    observationIncrements = []
    try:
        sortedObservationIncrements = [newEnsemble[i] - ensembleValues[indices[i]] for i in range(ensembleLength)]
    except IndexError:
        print(len(newEnsemble), ensembleLength, max(indices))
        print(cumulativeMass)
        print(massSum, mass[0])
    observationIncrements = [None for i in range(len(indices))]
    for i in range(len(indices)):
        observationIncrements[indices[i]] = sortedObservationIncrements[i]  
    return observationIncrements
    
                        



def EAKF(ensemble, observation, observationError, observedStatus):
    """
    Performs an EAKF assimilation with linear regression. 
    
    Takes ensemble in standard format, observation, assumed observation error, observedStatus as array with length = number of variables. Returns ensemble.
    """
    ensembleValues = EnsembleOperations.get_values_from_ensemble(ensemble, observedStatus) 
    observedValues = EnsembleOperations.get_observed_values_from_ensemble(ensembleValues)  
    posteriorSpreads, posteriorMeans = get_posterior(observedValues, observation, observationError)
    for i in range(len(observedValues)):
        ensembleValues = apply_state_inc(ensembleValues, get_state_inc(ensembleValues, obs_inc_EAKF(ensembleValues[i][1], posteriorMeans[i], posteriorSpreads[i]) ,i))
    ensemble = EnsembleOperations.get_ensemble_from_values(ensembleValues)
    return ensemble
                
            


def EnKF(ensemble, observation, observationError, observedStatus):
    """
    Performs an EnKF assimilation with linear regression. 
    
    Takes ensemble in standard format, observation, assumed observation error, observedStatus as array with length = number of variables. Returns ensemble.
    """
    ensembleValues = EnsembleOperations.get_values_from_ensemble(ensemble, observedStatus) 
    observedValues = EnsembleOperations.get_observed_values_from_ensemble(ensembleValues)  
    posteriorSpreads, posteriorMeans = get_posterior(observedValues, observation, observationError)
    for i in range(len(observedValues)):
        ensembleValues = apply_state_inc(ensembleValues, get_state_inc(ensembleValues, obs_inc_EnKF(ensembleValues[i][1], observation[i], observationError[i], posteriorMeans[i], posteriorSpreads[i]) ,i))
    ensemble = EnsembleOperations.get_ensemble_from_values(ensembleValues)
    return ensemble
    




def RHF(ensemble, observation, observationLikelihood, observedStatus):
    """
    Performs a Rank Histogram Filter assimilation with linear regression.
    
    Takes ensemble in standard format, observation, observationLikelihood as a list of either a standard deviation of a normal or an array of likelihood values with same length as ensemble, and observedStatus. Returns ensemble.
    """
    #print("Starting Assim Step")
    ensembleValues = EnsembleOperations.get_values_from_ensemble(ensemble, observedStatus)
    observedValues = EnsembleOperations.get_observed_values_from_ensemble(ensembleValues)
    if type(observationLikelihood[0]) is not np.ndarray:
        observationLikelihood = [mlab.normpdf(np.array(observedValues[i]), observation[i], observationLikelihood[i]) for i in range(len(observedValues))]
    for i in range(len(observedValues)):
        ensembleValues = apply_state_inc(ensembleValues, get_state_inc(ensembleValues, obs_inc_rank_histogram(observedValues[i], observationLikelihood[i], True), i))
    ensemble = EnsembleOperations.get_ensemble_from_values(ensembleValues)
    return ensemble



        
#-------------------------------------------------------------------------------
#           NO NEW METHODS BEYOND THIS POINT!
#-------------------------------------------------------------------------------    
    
methodsHash = {"EAKF" : EAKF, "EnKF" : EnKF, "RHF" : RHF}        #Stores all the assimilation methods as strings. 