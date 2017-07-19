# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import DataAssimilation
import EnsembleOperations
import IntegrationMethods
import Systems
import Graphics
import random

point = [1,1,1]
time = 0
dt = 0.01
function = Systems.Lorenz63
integration = IntegrationMethods.rk4
assimilation = DataAssimilation.EAKF
timeseriesX = []
timeseriesY = []
timeseriesZ = []
ensembleSize = 60
ensembletimeseriesX = [[] for i in range(ensembleSize)]
ensembletimeseriesY = [[] for i in range(ensembleSize)]
ensembletimeseriesZ = [[] for i in range(ensembleSize)]
timelist = []
error = 0.1
assimTimes = [i/10 for i in range(2000)]

ensemble = [[point[0] + random.gauss(0, error), point[1] + random.gauss(0, error), point[2] + random.gauss(0, error)] for i in range(ensembleSize)]
times = int(200/dt+1)
for i in range(times):
    timeseriesX.append(point[0])
    timeseriesY.append(point[1])
    timeseriesZ.append(point[2])
    timelist.append(time)
    for j in range(ensembleSize):
        ensembletimeseriesX[j].append(ensemble[j][0])
        ensembletimeseriesY[j].append(ensemble[j][1])
        ensembletimeseriesZ[j].append(ensemble[j][2])
    for j in range(len(ensemble)):
        ensemble[j] = integration(function, ensemble[j], time, dt)  
        
    point = integration(function, point, time, dt)       
    if round(time, 4) in assimTimes and time != 0:
        ensemble = assimilation(ensemble, [point[0] + random.gauss(0, error), point[1] + random.gauss(0, error), point[2] + random.gauss(0, error)], [error, error, error], [True, True, True])
    if round(time, 4)%10 == 0:
        print("Time", round(time, 4))
    time += dt
    #print(i/times)

#Graphics.graph_projection(["black"] + ["green" for i in range(5)], ["solid"] + ["dotted" for i in range(5)], [2] + [1 for i in range(5)], ["Truth", "Ensemble", "_nolegend_", "_nolegend_", "_nolegend_", "_nolegend_"], [timelist for i in range(6)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(5)], title="L63", xlabel="x", ylabel="y", zlabel="z")
Graphics.graph_projection(["black"] + ["green" for i in range(ensembleSize)], ["solid"] + ["dotted" for i in range(ensembleSize)], [2] + [1 for i in range(ensembleSize)], ["Truth", "Ensemble"] + ["_nolegend_" for i in range(ensembleSize - 1)], [timelist for i in range(ensembleSize + 1)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(ensembleSize)], title="L63", xlabel="x", ylabel="y", zlabel="z", ylim=[-20,20])
Graphics.graph_projection(["black"] + ["green" for i in range(ensembleSize)], ["solid"] + ["dotted" for i in range(ensembleSize)], [2] + [1 for i in range(ensembleSize)], ["Truth", "Ensemble"] + ["_nolegend_" for i in range(ensembleSize - 1)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(ensembleSize)], [timeseriesY] + [ensembletimeseriesY[i] for i in range(ensembleSize)], [timeseriesZ] + [ensembletimeseriesZ[i] for i in range(ensembleSize)], title="L63", xlabel="x", ylabel="y", zlabel="z", ylim=[-20,20])

