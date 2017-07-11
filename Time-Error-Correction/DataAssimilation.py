# -*- coding: utf-8 -*-
"""Contains methods for data assimilation."""


import numpy as analytics
from scipy import stats
import math






def get_posterior(ensembleValues, observation, observationError):
    """
    Assuming normality, uses Bayes' Rule to find the posterior distribution from an ensemble/prior and an observation distribution.
    
    Takes ensembleValues (observed only, as returned by get_observed_values_from_ensemble), observation as array of varuable values in same order as ensemble, and assumed error in observations.
    """
    #Convenience
    numberOfVariables = len(ensembleValues)    
    
    #Priors    
    ensembleMeans = [analytics.mean(valueList) for valueList in ensembleValues]
    ensembleSpreads = [analytics.std(valueList) for valueList in ensembleValues]
    
    #Compute Posterior 
    posteriorMeans = []
    posteriorSpreads = []
    for variable in range(numberOfVariables):
        #If there is no spread in the ensemble, it is completely certain and we don't need to adjust it.
        if ensembleSpreads[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(ensembleMeans[variable])
        #If there is no spread in the observation, we are completely certain it is accurate and we can set the ensemble to its value.
        elif observationError[variable] == 0:
            posteriorSpreads.append(0)
            posteriorMeans.append(observation[variable])
            
        #If there is spread in both ensemble and observation:
        #                 ______________________
        #                /__________1___________
        #std-post =     /____1____  + ___1___    
        #             \/(std-pri)^2  (std-obs)^2
        # and
        #
        #mean-post = (std-post)^2 *   ___mean-pri___  +  ____obs____
        #                              (std-pri)^2       (std-obs)^2
        #
        #where pri is prior, obs is observed, and post is posterior
        
        else:
            posteriorSpreads.append(math.sqrt(ensembleSpreads[variable]**-2 + observationError[variable]**-2))
            posteriorMeans.append((posteriorSpreads[-1]**2)*(ensembleMeans[variable]*ensembleSpreads[variable]**-2 + observation[variable]*observationError[variable]**-2))
            
    return posteriorSpreads, posteriorMeans
    
    
    
    
    

def regress_obs_incs(ensembleValues, observationIncrements):
    """
    Regresses observation increments onto other variables for each observed variable.
    
    Takes ensembleValues(with observedStatus) and observation increments. Length of observationIncrements should equal that of ensembleValues.
    """
    for observed in range(len(observationIncrements)):
        if ensembleValues[observed][0]:
            for unobserved in range(len(observationIncrements)):
                slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleValues[observed],ensembleValues[unobserved])
                for point in range(len(ensembleValues[0][1])):  #Apply increments
                    ensembleValues[unobserved][1][point] += observationIncrements[observed][point]*slope
    return ensembleValues
    




def obs_incs_EAKF(ensembleValues, posteriorMeans, posteriorSpreads):
    """
    Calculates observation increments based on prior and posterior distributions.
    
    Takes ensemble values like get_posterior and information about posterior analogous to output of get_posterior.
    Returns observation increments.
    """                    
    #Priors    
    ensembleMeans = [analytics.mean(valueList) for valueList in ensembleValues]
    ensembleSpreads = [analytics.std(valueList) for valueList in ensembleValues]
    observedIncrements = [[] for valueList in ensembleValues]
    for var in range(len(ensembleValues)):
        meanDifference = posteriorMeans[var] - ensembleMeans[var]
        spreadRatio = posteriorSpreads[var] / ensembleSpreads[var]
        for point in ensembleValues[var]:
            newValue = point + meanDifference
            distanceFromPosteriorMean = newValue - posteriorMeans[var]
            distanceFromPosteriorMean *= spreadRatio
            observedIncrements[var].append(posteriorMeans[var] + distanceFromPosteriorMean)
    return observedIncrements
        
                
                
            
            
    
    
