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

def get_adaptive_likelihood(point, error, errorType, dt, system, integration, *params):
    """
    Prototype method to get observation likelihood based on time error as well as state error.
    """
    if "Time" not in errorType:
        return point, error
    if len(params) == 0:
        params = None
    times = [MiscFunctions.generate_typed_error(point, error, errorType, dt, system, integration, params) for i in range(5000)]
    varLists = AnalysisOperations.get_var_lists_from_points(times)
    sortedVarList0 = np.sort(list(set(varLists[0])))
    sortedVarList1 = np.sort(list(set(varLists[1])))
    sortedVarList2 = np.sort(list(set(varLists[2])))
    sortedVarList3 = np.sort(list(set(varLists[3])))
#    Graphics.graph_projection(["blue", "orange"], ["scatter", "scatter"], [10, 10], ["Simulated observations", "Linear Scale"], [varLists[3], [min(varLists[3])-1 for i in range(len(varLists[3]))]], [varLists[0], varLists[0]], xlabel="Time", ylabel="x")
#    Graphics.graph_projection(["blue", "orange"], ["scatter", "scatter"], [10, 10], ["Simulated observations", "Linear Scale"], [varLists[3], [min(varLists[3])-1 for i in range(len(varLists[3]))]], [varLists[1], varLists[1]], xlabel="Time", ylabel="y")
#    Graphics.graph_projection(["blue", "orange"], ["scatter", "scatter"], [10, 10], ["Simulated observations", "Linear Scale"], [varLists[3], [min(varLists[3])-1 for i in range(len(varLists[3]))]], [varLists[2], varLists[2]], xlabel="Time", ylabel="z")
#    Graphics.rank_histogram([sortedVarList0[50*i] for i in range(math.ceil(len(sortedVarList0)/50))], "orange", 1, title="Rank Histogram for Simulated Observations in X")
#    Graphics.rank_histogram([sortedVarList1[50*i] for i in range(math.ceil(len(sortedVarList1)/50))], "orange", 1, title="Rank Histogram for Simulated Observations in Y")
#    Graphics.rank_histogram([sortedVarList2[50*i] for i in range(math.ceil(len(sortedVarList2)/50))], "orange", 1, title="Rank Histogram for Simulated Observations in Z")
#    Graphics.rank_histogram([sortedVarList3[50*i] for i in range(math.ceil(len(sortedVarList3)/50))], "orange", 1, title="Rank Histogram for Simulated Observations in Time")
    Graphics.kernel_density_estimation(sortedVarList0, ["red"], [0.15], [1], ["solid"], ["_nolegend_"], title="Probability Distribution for X at time" + str(point[3]))    
    Graphics.kernel_density_estimation(sortedVarList1, ["red"], [0.3], [1], ["solid"], ["_nolegend_"], title="Probability Distribution for Y at time" + str(point[3]))    
    Graphics.kernel_density_estimation(sortedVarList2, ["red"], [0.15], [1], ["solid"], ["_nolegend_"], title="Probability Distribution for Z at time" + str(point[3]))    
    Graphics.kernel_density_estimation(sortedVarList3, ["red"], [0.01], [1], ["solid"], ["_nolegend_"], title="Probability Distribution for T at time" + str(point[3]))                    
    return [np.mean(l) for l in varLists], [np.std(l) for l in varLists]

