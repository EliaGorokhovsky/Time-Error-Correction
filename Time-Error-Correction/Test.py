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
ensembleSize = 20
ensembletimeseriesX = [[] for i in range(ensembleSize)]
ensembletimeseriesY = [[] for i in range(ensembleSize)]
ensembletimeseriesZ = [[] for i in range(ensembleSize)]
timelist = []
error = 5

ensemble = [[point[0] + random.gauss(0, error), point[1] + random.gauss(0, error), point[2] + random.gauss(0, error)] for i in range(ensembleSize)]
times = int(200/dt)
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
    if round(time, 4) == 17.5:
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 0, 0, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 0, 1, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 0, 2, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 1, 0, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 1, 1, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 1, 2, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 2, 0, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 2, 1, point)
        Graphics.plot_bivariate(["blue", "red"], [25, 50], DataAssimilation.get_state_incs(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), DataAssimilation.obs_incs_EAKF(EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])), point, [0.1, 0.1, 0.1])), EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True]), 2, 2, point)
        
    point = integration(function, point, time, dt)       
    if round(time, 4)%2.5 == 0 and time != 0:
        ensemble = assimilation(ensemble, point, [error/10, error/10, error/10], [True, True, True])
    if round(time, 4)%10 == 0:
        print(round(time, 4))
    time += dt
    #print(i/times)

#Graphics.graph_projection(["black"] + ["green" for i in range(5)], ["solid"] + ["dotted" for i in range(5)], [2] + [1 for i in range(5)], ["Truth", "Ensemble", "_nolegend_", "_nolegend_", "_nolegend_", "_nolegend_"], [timelist for i in range(6)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(5)], title="L63", xlabel="x", ylabel="y", zlabel="z")
Graphics.graph_projection(["black"] + ["green" for i in range(ensembleSize)], ["solid"] + ["dotted" for i in range(ensembleSize)], [2] + [1 for i in range(ensembleSize)], ["Truth", "Ensemble"] + ["_nolegend_" for i in range(ensembleSize - 1)], [timelist for i in range(ensembleSize + 1)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(ensembleSize)], title="L63", xlabel="x", ylabel="y", zlabel="z", ylim=[-20,20])
Graphics.graph_projection(["black"] + ["green" for i in range(ensembleSize)], ["solid"] + ["dotted" for i in range(ensembleSize)], [2] + [1 for i in range(ensembleSize)], ["Truth", "Ensemble"] + ["_nolegend_" for i in range(ensembleSize - 1)], [timeseriesX] + [ensembletimeseriesX[i] for i in range(ensembleSize)], [timeseriesY] + [ensembletimeseriesY[i] for i in range(ensembleSize)], [timeseriesZ] + [ensembletimeseriesZ[i] for i in range(ensembleSize)], title="L63", xlabel="x", ylabel="y", zlabel="z", ylim=[-20,20])

