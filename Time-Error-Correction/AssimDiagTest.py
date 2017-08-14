# -*- coding: utf-8 -*-
"""A module that runs a test of a single assimilation step."""
import random
import MiscFunctions
import AnalysisOperations
import numpy as np
import matplotlib.mlab as mlab
import DataAssimilation
from scipy.stats import norm
import math

def obs_inc_rank_histogram(ensembleValues, observationLikelihood, rectangularQuadrature):
    """
    Calculates observation increments for one variable using the RHF on ensemble.
    
    Takes one list of values i.e. ensembleValues[i], observation in one variable, and observation likelihood as a list of likelihood with length equal to that of ensembleValues.
    Returns list of observation ecrements of equal length to ensembleValues.
    """
    #Priors
    ensembleSpread = np.std(ensembleValues)
    print("Ensemble Spread:", ensembleSpread)
    ensembleLength = len(ensembleValues)
    print("EnsembleLength:", ensembleLength)
    sortedEnsemble, indices = MiscFunctions.sort_indices(ensembleValues)
    print("Sorted, Indices:", sortedEnsemble, indices)
    newObservationLikelihood = [observationLikelihood[indices[i]] for i in range(ensembleLength)]
    observationLikelihood = newObservationLikelihood[:]
    print("Likelihood:", observationLikelihood)
    likelihoodDensity = [(observationLikelihood[i+1] + observationLikelihood[i])/2 for i in range(len(observationLikelihood)-1)]
    print("Likelihood Density:", likelihoodDensity)

    
    #Compute partial Gaussian kernels for tails of prior.    
    distanceForUnitSpread = -1 * MiscFunctions.weighted_norm_inverse(1, 0, 1, 1/(ensembleLength + 1))
    print("Distance for unit spread:", distanceForUnitSpread)
    leftMean = sortedEnsemble[0] + distanceForUnitSpread * ensembleSpread
    leftStandardDeviation = ensembleSpread
    print("Left:", leftMean, leftStandardDeviation)
    rightMean = sortedEnsemble[-1] - distanceForUnitSpread * ensembleSpread
    rightStandardDeviation = ensembleSpread
    print("Right:", rightMean, rightStandardDeviation)
    
    #Assume flat tails in likelihood. TODO: Allow for Gaussian tails (should only be relevant for nearly Gaussian likelihoods.)
    leftProductWeight = observationLikelihood[0]    
    rightProductWeight = observationLikelihood[-1]
    #Get the mass in between each bin.
    mass = np.array([leftProductWeight/(ensembleLength + 1)] + [likelihoodDensity[i]/(ensembleLength+1) for i in range(len(likelihoodDensity))] + [rightProductWeight/(ensembleLength + 1)])
    print("Masses:", list(mass))
    
    #Get height and normalize mass for trapezoidal.
    height = np.array([-1 if sortedEnsemble[i+1]==sortedEnsemble[i] else 1/((ensembleLength+1)*(sortedEnsemble[i+1]-sortedEnsemble[i])) for i in range(len(sortedEnsemble)-1)])
    print("Height:", list(height))
    massSum = sum(mass)    
    mass /= massSum
    print("Normalized Mass:", list(mass))
    
    #Get weight for normalized partial Gaussian tails. TODO: Descriptive names
    leftAmp = leftProductWeight / massSum
    rightAmp = rightProductWeight / massSum
    print("Amps:", leftAmp, rightAmp)
    
    #Get cumulativemass at each bin bound (CDF)
    cumulativeMass = [0]
    for i in range(len(mass)):
        cumulativeMass.append(cumulativeMass[i] + mass[i])
    print("Cumulative Mass:", cumulativeMass)
    #Searching for boxes for each ensemble member. 
    lowestBox = 0          #Updated so we don't have to search boxes we've already passed.     
 
    newEnsemble = []
    #print(ensembleValues)
    for i in range(ensembleLength):
        found = False
        print("------------------------------------\nEnsemble point:", i)
        passedMass = (i+1)/(ensembleLength + 1)         #The amount of mass before each ensemble member.
        print("Mass passed:", passedMass)
        if passedMass < cumulativeMass[1]:          #If it's in the left tail
            newEnsemble.append(MiscFunctions.weighted_norm_inverse(leftAmp, leftMean, leftStandardDeviation, passedMass))
            found = True
            print("Post found in left tail:", newEnsemble[-1])
        elif passedMass > cumulativeMass[-2]:       #If it's in the right tail
            newEnsemble.append(MiscFunctions.weighted_norm_inverse(rightAmp, rightMean, rightStandardDeviation, 1-passedMass))
            newEnsemble[-1] = 2*rightMean - newEnsemble[-1]
            found = True
            print("Post found in right tail:", newEnsemble[-1])
        else:                                       #If it's in one of the uniform boxes in the middle.
            for cumulativeMassIndex in range(lowestBox, len(cumulativeMass)):  #Ignore mass after last ensemble point.
                if passedMass >= cumulativeMass[cumulativeMassIndex - 1] and passedMass <= cumulativeMass[cumulativeMassIndex] and not found:     #If the mass is greater than the total mass up to a point but less than the total mass after a point: 
                    print("Post found between", cumulativeMassIndex-1, "and", cumulativeMassIndex)
                    if rectangularQuadrature:
                        ensemblePointIndex = cumulativeMassIndex - 2    #The index of the ensemble point to the left of the area and also of the height of the bin.
                        print("Ensemble point", ensemblePointIndex)                        
                        newEnsemble.append(sortedEnsemble[ensemblePointIndex] + (passedMass-cumulativeMass[cumulativeMassIndex-1])/(cumulativeMass[cumulativeMassIndex] - cumulativeMass[cumulativeMassIndex-1])*(sortedEnsemble[ensemblePointIndex+1] - sortedEnsemble[ensemblePointIndex]))
                        found = True
                        print("Assimilating to", newEnsemble[-1])                        
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
                        elif root2 >= sortedEnsemble[ensemblePointIndex] and root2 <= sortedEnsemble[ensemblePointIndex + 1]:
                            newEnsemble.append(root2)
                        else:
                            raise ValueError("Rank Histogram Filter was unable to get a satisfactory root for trapezoidal interpolation.")
                    lowestBox = cumulativeMassIndex
                    
    observationIncrements = []
#    print("to")
#    print(newEnsemble)
#    print("using")
#    print(observationLikelihood)
#    print("")
    #Get increments
    #TEST: THIS SETS THE NEW ENSEMBLE TO THE OBSERVATION.------------------------
    #newEnsemble = [observation for i in range(ensembleLength)]
    #----------------------------------------------------------------------------
    sortedObservationIncrements = [newEnsemble[i] - ensembleValues[indices[i]] for i in range(ensembleLength)]
    observationIncrements = [None for i in range(len(indices))]
    for i in range(len(indices)):
        observationIncrements[indices[i]] = sortedObservationIncrements[i]        
    print("New Ensemble: N(",np.mean(newEnsemble),np.std(newEnsemble),")")
    #print("New Ensemble:", newEnsemble)
    return observationIncrements
    
ens = [0, -1, 1, 2, -2]                        
print(obs_inc_rank_histogram(ens, mlab.normpdf(np.array(ens), 4, 2), True))