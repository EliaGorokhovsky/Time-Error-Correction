# -*- coding: utf-8 -*-
"""Contains various experimental functions."""
import MiscFunctions
import AnalysisOperations
import numpy as np
import Graphics
from scipy.stats import norm
import Systems
import IntegrationMethods
import math
import matplotlib.mlab as mlab

def get_adaptive_likelihood(point, error, errorType, dt, system, integration, *params, **kwargs):
    """
    Prototype method to get observation likelihood based on time error as well as state error.
    Kwargs:
        ensemble: If present, returns probability distribution as a discrete list of probabilities instead of a normal.
        amount: If present, dictates the amount of random ramples used to get discrete distribution. Default is 500.
    """
    if "Time" not in errorType:
        return point, error
    else:
        timeError = [0 if errorType[i] != "Time" else error[i] for i in range(len(error))]
    if "amount" in kwargs:
        amount = kwargs["amount"]
    else:
        amount = 500
    if len(params) == 0:
        params = None
    if "ensemble" not in kwargs:
        pseudoObservations = [MiscFunctions.generate_typed_error(point, error, errorType, dt, system, integration, params) for i in range(amount)]
        varLists = AnalysisOperations.get_var_lists_from_points(pseudoObservations)
        return [np.mean(l) for l in varLists], [np.std(l, ddof=1) for l in varLists]
    else:
        pseudoObservations = [MiscFunctions.generate_typed_error(point, timeError, errorType, dt, system, integration, params) for i in range(amount)]
        varLists = AnalysisOperations.get_var_lists_from_points(pseudoObservations)
        probabilities = [np.array([0.0 for j in range(len(kwargs["ensemble"]))]) for i in range(len(varLists))]
        ensembleValues = np.array(AnalysisOperations.get_var_lists_from_points(kwargs["ensemble"]))
        for var in range(len(ensembleValues)):
            if errorType[var] != "Time":
                for point in range(len(pseudoObservations)):
                    normal = np.array(mlab.normpdf(ensembleValues[var], varLists[var][point], error[var]))
                    probabilities[var] += normal
                probabilitySum = sum(probabilities[var])
                probabilities[var] /= probabilitySum
                if probabilitySum == 0:
                    probabilities[var] = np.array([1/len(probabilities[var]) for i in probabilities[var]])
        for i in probabilities:
            for j in i:
                if j < 0:
                    print("In get_adaptive_likelihood, i=", j)
        return np.array(probabilities)
                    
            
        
        
                
            
            
        

   

