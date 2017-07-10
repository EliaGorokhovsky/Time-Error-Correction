# -*- coding: utf-8 -*-
"""A collection of common chaotic systems stored as functions."""

import math

#------------------------------------------------------------------------------
#           LORENZ '63 ("butterfly") - define system
#------------------------------------------------------------------------------
def Lorenz63(params, pos, *t):        #where pos is an array of length 3, and params is [rho, sigma, beta]
    """System of equations resulting in a 'butterfly attractor'. Derived in Lorenz(1963). Takes 3 parameters and 3-dimensional array of positions."""  
    #default values for params:
    #rho = 28
    #sigma = 10
    #beta = 8/3
    rho = params[0]
    sigma = params[1]
    beta = params[2]
    
    v = [1,1,1]    #placeholder
    
    v[0] = sigma*(pos[1]-pos[0])
    v[1] = pos[0]*(rho-pos[2])-pos[1]
    v[2] = pos[0]*pos[1]-beta*pos[2] 
    
    return v    #returns instantaneous rate of change
    
#------------------------------------------------------------------------------
#           LORENZ '84 - define system
#------------------------------------------------------------------------------
def Lorenz84(params, pos, t):              #where pos is an array of length 3 and params is [a, b, F, G]
    """System of 3 equations with 3 variables and 4 parameters derived in Lorenz(1984)."""
    #default values for params:
    #a = 0.25
    #b = 4
    #F = 8
    #G = 1.25
    a = params[0]
    b = params[1]
    F = params[2]
    G = params[3]
    
    v = [1,1,1]
    
    v[0] = -(pos[1]**2)-(pos[2]**2)-(a*pos[0])+(a*F)
    v[1] = (pos[0]*pos[1]) - (b*pos[0]*pos[2]) - pos[1] + G
    v[2] = (b*pos[0]*pos[1]) + (pos[0]*pos[2]) - pos[2]
    
    return v    #returns instantaneous rate of change
    
#------------------------------------------------------------------------------
#           TEST 3-var
#------------------------------------------------------------------------------
def Test(params, pos, t):
    """Simple test function to verify that various functions work consistently."""
    #default values for params:
    #a = 1
    a = params[0]
    
    v = [1,1,1]
    
    v[0] = a
    v[1] = a
    v[2] = a
    
    return v     #returns instantaneous rate of change
