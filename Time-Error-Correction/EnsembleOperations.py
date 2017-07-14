# -*- coding: utf-8 -*-
"""Contains various operations on ensemble formatting."""




def copy_ensemble_values(ensembleValues):
    return [[ensembleValues[i][0], ensembleValues[i][1][:]] for i in range(len(ensembleValues))]



def get_values_from_ensemble(ensemble, observedStatus):
    """
    Converts ensemble (array of n-dimensional points) into n arrays of values.Returns array containing arrays in form [observedStatus, [variable values]].
    
    observedStatus is list of booleans stating if a variable is observed (used directly in assimilation).
    Assumes length of observedStatus = length of each ensemble point.
    """
    values = []
    for status in observedStatus:
        values.append([status, []])
    for i in range(len(ensemble)):
        for var in range(len(ensemble[i])):
            values[var][1].append(ensemble[i][var])
    return values
    




def get_observed_values_from_ensemble(values):
    """
    Converts array of values (analogous to output of get_values_from_ensemble) into arrays of observed values.
    Ignores unobserved values.
    """
    observedValues = []
    for i in values:
        if i[0]:
            observedValues.append(i[1])
    return observedValues




    
def get_ensemble_from_values(values):
    """
    Converts 2-d array of values (analogous to output of get_values_from_ensemble) into standard ensemble format.
    """
    ensemble = [[] for i in range(len(values[0][1]))]
    for var in range(len(values)):
        for point in range(len(values[var][1])):
            ensemble[point].append(values[var][1][point])
    return ensemble
    


    