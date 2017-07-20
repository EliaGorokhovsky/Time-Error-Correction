# -*- coding: utf-8 -*-
"""Contains miscellaneous functions that perform common operations."""


import math
import random



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
    return [point[var] + random.gauss(point[var], error[var]) for var in range(len(point))]