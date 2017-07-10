# -*- coding: utf-8 -*-
"""Contains various functions needed for data assimilation"""

import Functions
import IntegrationMethods
import VariousFunctions
import random
import numpy
import math
import matplotlib.pyplot as plt
from scipy import stats
    

def genEnsemble_3var(pos, size, stdevSpace):    #Generate an ensemble given an observation.
    ens = []
    for i in range(size):
        newX = random.gauss(pos[0], stdevSpace[0])
        newY = random.gauss(pos[1], stdevSpace[1])
        newZ = random.gauss(pos[2], stdevSpace[2])
        ens.append([newX,newY,newZ])
    return ens

def genEnsemble_4var(pos, size, stdevSpace, stdevTime, times, timeSeries, usedIntegration, usedFunction, params):
    ens = []
    for i in range(size):
        #May change later to accomodate negative time
        newTime = abs(ErrorGeneration.genTimeError(0,stdevTime))
        trueVal = getPosAtTime(times, timeSeries, newTime, usedIntegration, usedFunction, params)
        newX = random.gauss(trueVal[0], stdevSpace[0])
        newY = random.gauss(trueVal[1], stdevSpace[1])
        newZ = random.gauss(trueVal[2], stdevSpace[2])
        trueTime = 0
        ens.append([[newTime, trueTime], [newX,newY,newZ]])
    return ens    

def EAKF_3var(ensemble, observationStdev, observation, timesToCheck):
#------------------------------------------------------------------------------
#STARTING INFO
    ensembleX = []
    ensembleY = []
    ensembleZ = []

    for i in range(len(ensemble)):
        ensembleX.append(ensemble[i][0])
        ensembleY.append(ensemble[i][1])
        ensembleZ.append(ensemble[i][2])
    ensembleVals = [ensembleX, ensembleY, ensembleZ]
    stdevs = [numpy.std(ensembleVals[0]), numpy.std(ensembleVals[1]), numpy.std(ensembleVals[2])]
    means = [numpy.mean(ensembleVals[0]), numpy.mean(ensembleVals[1]), numpy.mean(ensembleVals[2])]    
#------------------------------------------------------------------------------
#FIND POSTERIOR
    postStdev = []
    postMean = []
    for i in range(3):
        if  stdevs[i] == 0:
            stdevPost = 0
            meanPost = means[i]
        elif observationStdev[i] == 0:
            stdevPost = 0
            meanPost = observation[i]
        else:   
            sumOfInverseSquares = (stdevs[i]**(-2)) + (observationStdev[i]**(-2))
            stdevPost = math.sqrt(sumOfInverseSquares**(-1))
            sumOfInverseSquareMeans = means[i]*(stdevs[i]**(-2)) + observation[i]*(observationStdev[i]**(-2))
            meanPost = (stdevPost**2)*sumOfInverseSquareMeans
        postMean.append(meanPost)
        postStdev.append(stdevPost)
#------------------------------------------------------------------------------
#ADJUST ENSEMBLE
    for i in range(3):      #For all space variables
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        stdevs = [numpy.std(ensembleVals[0]), numpy.std(ensembleVals[1]), numpy.std(ensembleVals[2])]
        means = [numpy.mean(ensembleVals[0]), numpy.mean(ensembleVals[1]), numpy.mean(ensembleVals[2])]
        #OBSERVED INCREMENTS!!!!
        #Mean
        newVal = list(ensembleVals[i])     #placeholder
        meanChange = postMean[i] - means[i]
        for j in range(len(newVal)):
            newVal[j] += meanChange

        #Stdevs
        meanDist = []
        for j in range(len(newVal)):
            meanDist.append(newVal[j] - postMean[i])
        stdevRatio = postStdev[i]/stdevs[i]
        for j in range(len(meanDist)):
            meanDist[j]*=stdevRatio
        for j in range(len(newVal)):
            newVal[j] = postMean[i] + meanDist[j]
        obs_inc = []
        for j in range(len(newVal)):
            obs_inc.append(newVal[j] - ensembleVals[i][j])
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #STATE INCREMENTS
        newEnsembleVals = [[],[],[]]
        state_incs = [[],[],[]]
        for j in range(3):
            slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleVals[i],ensembleVals[j])
            for k in range(len(ensemble)):
                state_incs[j].append(obs_inc[k]*slope)
        for j in range(len(ensembleVals)):
            for k in range(len(ensembleVals[j])):
                newEnsembleVals[j].append(ensembleVals[j][k] + state_incs[j][k])
        ensembleVals = list(newEnsembleVals)
        
    newEnsemble = []
    for i in range(len(ensembleVals[0])):
        newEnsemble.append([ensembleVals[0][i], ensembleVals[1][i], ensembleVals[2][i]])
            
    return newEnsemble
                
        
            
#==============================================================================
#BELOW IS THE EXPERIMENTAL MODEL
#==============================================================================            
        
   

def EAKF_4var(ensembleWithTime, observationStdev, observation, timeError, timesToCheck):
#------------------------------------------------------------------------------
#STARTING INFO
    #TIME
    ensemble = []
    times = []
    for i in ensembleWithTime:
        times.append(i[0][0])
        ensemble.append(i[1])
    trueTime = ensembleWithTime[0][0][1]
    incList = []
    ensembleX = []
    ensembleY = []
    ensembleZ = []
    for i in range(len(ensemble)):
        ensembleX.append(ensemble[i][0])
        ensembleY.append(ensemble[i][1])
        ensembleZ.append(ensemble[i][2])
    ensembleVals = [ensembleX, ensembleY, ensembleZ]
    stdevs = [numpy.std(ensembleVals[0]), numpy.std(ensembleVals[1]), numpy.std(ensembleVals[2])]
    means = [numpy.mean(ensembleVals[0]), numpy.mean(ensembleVals[1]), numpy.mean(ensembleVals[2])]
    stateIncsList = []    
#------------------------------------------------------------------------------
#FIND POSTERIOR
    postStdev = []
    postMean = []
    for i in range(3):
        if  stdevs[i] == 0:
            stdevPost = 0
            meanPost = means[i]
        elif observationStdev[i] == 0:
            stdevPost = 0
            meanPost = observation[i]
        else:   
            sumOfInverseSquares = (stdevs[i]**(-2)) + (observationStdev[i]**(-2))
            stdevPost = math.sqrt(sumOfInverseSquares**(-1))
            sumOfInverseSquareMeans = means[i]*(stdevs[i]**(-2)) + observation[1][i]*(observationStdev[i]**(-2))
            meanPost = (stdevPost**2)*sumOfInverseSquareMeans
        postMean.append(meanPost)
        postStdev.append(stdevPost)
    
#------------------------------------------------------------------------------
#ADJUST ENSEMBLE
    for i in range(3):      #For all space variables
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        stdevs = [numpy.std(ensembleVals[0]), numpy.std(ensembleVals[1]), numpy.std(ensembleVals[2])]
        means = [numpy.mean(ensembleVals[0]), numpy.mean(ensembleVals[1]), numpy.mean(ensembleVals[2])]
        #OBSERVED INCREMENTS!!!!
        #Mean
        newVal = list(ensembleVals[i])     #placeholder
        meanChange = postMean[i] - means[i]
        for j in range(len(newVal)):
            newVal[j] += meanChange

        #Stdevs
        meanDist = []
        for j in range(len(newVal)):
            meanDist.append(newVal[j] - postMean[i])
        stdevRatio = postStdev[i]/stdevs[i]
        for j in range(len(meanDist)):
            meanDist[j]*=stdevRatio
        for j in range(len(newVal)):
            newVal[j] = postMean[i] + meanDist[j]
        obs_inc = []
        for j in range(len(newVal)):
            obs_inc.append(newVal[j] - ensembleVals[i][j])
        #- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        #STATE INCREMENTS
        newEnsembleVals = [[],[],[]]
        state_incs = [[],[],[]]
        for j in range(3):
            slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleVals[i],ensembleVals[j])
            for k in range(len(ensemble)):
                state_incs[j].append(obs_inc[k]*slope)
        slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleVals[i], times)
        
        for j in range(len(times)):
            state_inc = obs_inc[j]*slope
                #print("assimilated time from ", times[j], " to ", times[j] + state_inc )
            #times[j] += state_inc
        if trueTime in timesToCheck: 
            incList.append(state_incs)
        for j in range(len(ensembleVals)):
            for k in range(len(ensembleVals[j])):
               # print([k, len(state_incs[j])])
                newEnsembleVals[j].append(ensembleVals[j][k] + state_incs[j][k])
        ensembleVals = list(newEnsembleVals)
        
    newEnsemble = []
    for i in range(len(ensembleVals[0])):
        newEnsemble.append([[times[i], trueTime], [ensembleVals[0][i], ensembleVals[1][i], ensembleVals[2][i]]])
            
    return newEnsemble, incList     
        
        
def inflateControl(ensemble, amount):
    varListX, varListY, varListZ = VariousFunctions.getVarLists(ensemble)
    xMean = numpy.mean(varListX)
    yMean = numpy.mean(varListY)
    zMean = numpy.mean(varListZ)
    newEnsemble = []
    for i in range(len(ensemble)):
        newEnsemble.append([xMean+amount*(varListX[i]-xMean), yMean+amount*(varListY[i]-yMean), zMean+amount*(varListZ[i]-zMean)])
    return newEnsemble
    
def inflateExperimental(ensemble, amount):
    timesList = []
    positionsList = []
    for point in ensemble:
        timesList.append(point[0])
        positionsList.append(point[1])
    positionsList = inflateControl(positionsList, amount)
    newEnsemble = []
    for i in range(len(positionsList)):
        newEnsemble.append([timesList[i], positionsList[i]])
    return newEnsemble
    
    
        
    
    
        
        
    
    
    