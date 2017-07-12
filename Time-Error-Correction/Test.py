# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import DataAssimilation
import EnsembleOperations
import IntegrationMethods
import Systems
import Graphics

point = [1,1,1]
time = 0
dt = 0.001
function = Systems.Lorenz63
integration = IntegrationMethods.eulers_method
assimilation = DataAssimilation.EAKF
timeseriesX = []
timeseriesY = []
timeseriesZ = []
for i in range(int(200/dt)):
    timeseriesX.append(point[0])
    timeseriesY.append(point[1])
    timeseriesZ.append(point[2])
    point = integration(function, point, time, dt)
    time += dt
Graphics.graph_projection(["black"], ["solid"], [1], ["Truth"], [timeseriesX], [timeseriesY], [timeseriesZ], title="L63", xlabel="x", ylabel="y", zlabel="z")
