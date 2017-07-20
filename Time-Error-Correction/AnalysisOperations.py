# -*- coding: utf-8 -*-
"""Analytical operations with time series."""

def get_var_lists_from_points(truths):      #identical to get_observed_values_from_ensemble(get_values_from_ensemble(x), [True for i in range(len(x))])
    """
    Converts list of points into lists of variable values.
    """
    return [[truths[j][i] for j in range(len(truths))] for i in range(len(truths[0]))]      #More up-to-date than ensemble operations thanks to list comprehensions.

