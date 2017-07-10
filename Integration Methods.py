# -*- coding: utf-8 -*-
"""A collection of functions to approximately solve differential equations."""

#------------------------------------------------------------------------------
#           EULER'S METHOD - ONE STEP
#------------------------------------------------------------------------------
def eulers_method(f, params, pos, t, dt):      #currently only works for autonomous systems
    """Simple linear approximation."""
    k = pos
    
    for i in range(len(pos)): 
        k[i] = dt*f(params, pos, t)[i]
        
    for i in range(len(pos)):
        pos[i] += k[i]
    return pos
#------------------------------------------------------------------------------ 
#           RK2 - TWO-STEP RUNGE KUTTA
#------------------------------------------------------------------------------        
def rk2_3var(f, params, pos, t, dt):         #currently only works for autonomous systems
    """Third-order Runge-Kutta."""
    k1 = pos #placeholder
    k2 = pos #placeholder
    
    for i in range(len(pos)):      #intermediate vars
        k1[i] = dt*f(params, pos, t)[i]    #STEP 1
    
    pos2 = list(pos) #placeholder
    for i in range(len(pos)):      #STEP 2
        pos2[i] = pos[i] + (k1[i]/2)
    for i in range(len(pos)):
        k2[i] = dt*f(params, pos2, t + (dt/2))[i]
    
    for i in range(len(pos)):   #Adding to position
        pos[i] += k2[i]
    
    return pos
#------------------------------------------------------------------------------
#           RK4 - FOUR-STEP RUNGE KUTTA
#------------------------------------------------------------------------------            
def rk4_3var(f, params, pos, t, dt):         #currently only works for autonomous systems    
    """Fourth-order Runge-Kutta"""
    k1 = pos #placeholder
    k2 = pos #placeholder
    k3 = pos #placeholder
    k4 = pos #placeholder
    length = len(pos)
    
    for i in range(length):          #STEP 1
        k1[i] = dt*f(params, pos, t)[i]
        
    pos2 = list(pos)                  #STEP 2
    for i in range(length):
        pos2[i] = pos[i] +(k1[i]/2)
    for i in range(length):
        k2[i] = dt*f(params, pos2, t + (dt/2))[i]
        
    pos3 = list(pos)                 #STEP 3
    for i in range(length):
        pos3[i] = pos[i] + (k2[i]/2)
    for i in range(length):
        k3[i] = dt*f(params, pos3, t + (dt/2))[i]
        
    pos4 = list(pos)                 #STEP 4
    for i in range(length):
        pos4[i] = pos[i] + k3[i]
    for i in range(length):
        k4[i] = dt*f(params, pos4, t + dt)[i]
        
    for i in range(length):
        pos[i] += (k1[i]/6) + (k2[i]/3) + (k3[i]/3) + (k4[i]/6)
    return pos
    
    
