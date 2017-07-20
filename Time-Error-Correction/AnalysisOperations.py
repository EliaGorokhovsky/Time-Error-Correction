"""Analytical operations with time series."""

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