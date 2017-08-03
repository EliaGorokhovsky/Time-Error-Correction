"""Analytical operations with time series."""

import math

def get_var_lists_from_points(truths):      #identical to get_observed_values_from_ensemble(get_values_from_ensemble(x), [True for i in range(len(x))])
    """
    Converts list of points into lists of variable values.
    """
    return [[truths[j][i] for j in range(len(truths))] for i in range(len(truths[0]))]      #More up-to-date than ensemble operations thanks to list comprehensions.


def get_ensemble_var_lists_from_time_series(ensembleTimeSeries):
    """
    Converts ensemble time series into ensembleSize lists of variables.    
    """
    return [[[ensembleTimeSeries[step][point][var] for step in range(len(ensembleTimeSeries))] for var in range(len(ensembleTimeSeries[0][0]))] for point in range(len(ensembleTimeSeries[0]))]
    
def get_RMSE(ensembleMeanList, truthList, inclusionStatus):
    """
    Returns RMSE over all timesteps, assuming ensemble and truth run for same amount.
    
    Takes list of ensemble means, truths.
    """
    dist = lambda x,y,inclusionStatus :  math.sqrt(sum([(y[i]-x[i])**2 for i in range(len(x)) if inclusionStatus[i]]))
    return math.sqrt((sum([dist(ensembleMeanList[i], truthList[i], inclusionStatus)**2 for i in range(len(ensembleMeanList))])/len(ensembleMeanList)))

def get_points_from_var_lists(varLists):
    """
    Converts list of variable values into list of points.
    """
    return [[varLists[i][j] for i in range(len(varLists))] for j in range(len(varLists[0]))]