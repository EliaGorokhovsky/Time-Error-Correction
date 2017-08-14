# -*- coding: utf-8 -*-
"""Contains miscellaneous functions that perform common operations."""


import math
import random
from scipy.stats import norm



def mod(a, b):
    """
    Divides a number by a number and finds the remainder.

    Takes divisor, then dividend. Returns integer quotient and remainder.    
    """
    quotient = a / b
    remainder = (quotient - math.floor(quotient))*b
    return math.floor(quotient), remainder
    
    



def perturb_point(point, error):
    """
    Generates a perturbed point given error for each variable. Used for ensemble generation and observations.
    """
    return [round(random.gauss(point[var], error[var]), 5) for var in range(len(point))]
    
    
    
    
def get_position_at_time(basePosition, baseTime, dt, targetTime, system, integration, *params):
    """
    Gets the system state at a given time.
    """
    if len(params) == 0:
        params = None
    time = baseTime
    pos = list(basePosition)
    while time != targetTime:
        if targetTime - time >= dt:
            pos = integration(system, pos, time, dt, params)
            time += dt
        else:
            timestep = targetTime - time
            pos = integration(system, pos, time, timestep, params)
            time += timestep
    return pos
    
    
    
    
    
def generate_typed_error(point, error, errorType, dt, system, integration, *params):
    """
    Perturbs a point in such a way that if error is time error, it is calculated first. errorType is of form ["Type", "Type"...]
    """
    if len(params) == 0:
        params = None
    if "Time" in errorType:
        timeError = error[errorType.index("Time")]
        point = get_position_at_time(point, point[errorType.index("Time")], dt, random.gauss(point[errorType.index("Time")], timeError), system, integration, params)
        return [round(random.gauss(point[var], error[var]), 5) if errorType[var] == "State" else point[var] for var in range(len(point))]
    else:
        return perturb_point(point, error)
        
        

def norm_inverse(p):
    """
    Uses a polynomial approximation of the inverse of the normal CDF to find the x for which the area under the function is equal to p.
    """
    #Originally by John Herrero.
    #http://home.online.no/~pjacklam/notes/invnorm
    a1 = -39.69683028665376
    a2 =  220.9460984245205
    a3 = -275.9285104469687
    a4 =  138.357751867269
    a5 = -30.99479806614716
    a6 =  2.506628277459239
    b1 = -54.4760987982241
    b2 =  161.5858368580409
    b3 = -155.6989798598866
    b4 =  66.80131188771972
    b5 = -13.28068155288572
    c1 = -0.0778484002430293
    c2 = -0.3223964580411365
    c3 = -2.400758277161838
    c4 = -2.549732539343734
    c5 =  4.374664141464968
    c6 =  2.938163982698783
    d1 =  0.0084695709041462
    d2 =  0.3224671290700398
    d3 =  2.445134137142996
    d4 =  3.754408661907416
    pLow = 0.02425
    pHigh = 1-pLow
    if p < pLow:
        q = math.sqrt(-2*math.log(p))
        return (((((c1*q + c2)*q + c3)*q + c4)*q + c5)*q + c6)/((((d1*q + d2)*q + d3)*q + d4)*q + 1)
    elif p > pHigh:
        q = math.sqrt(-2*math.log(1 - p))
        return -(((((c1*q + c2)*q + c3)*q + c4)*q + c5)*q + c6)/((((d1*q + d2)*q + d3)*q + d4)*q + 1)
    else:
        q = p - 0.5
        r = q**2
        return (((((a1*r + a2)*r + a3)*r + a4)*r + a5)*r + a6)/(((((b1*r + b2)*r + b3)*r + b4)*r + b5)*r + 1)
        



def weighted_norm_inverse(alpha, mean, standardDeviation, p):
    """
    Find x such that the CDF of a normal distribution with certain mean and sd multiplied by alpha is p.
    """
    np = p / alpha
    x = norm_inverse(np)
    x = mean + x * standardDeviation
    #return x
    return norm.ppf(p/alpha, loc=mean, scale=standardDeviation)
  


  
    
def solve_quadratic(a, b, c):
    """
    Applies the quadratic formula given 3 coefficients.
    """
    return (-b + math.sqrt(b**2 - 4*a*c))/(2*a), (-b - math.sqrt(b**2 - 4*a*c))/(2*a)
    
       
    
    
def sort_indices(aList):
    """
    Inefficient function to sort a list and return the indices of the input list in the order of list elements.
    """
    indices = []
    sortedList = []
    originalList = aList[:]
    bList = aList[:]
    while len(bList) > 0:
        minimumValue = min(bList)
        index = originalList.index(minimumValue)
        indices.append(index)
        sortedList.append(minimumValue)
        del bList[bList.index(minimumValue)]
    return sortedList, indices
        
   

    