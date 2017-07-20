# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import Process
import Graphics
import AnalysisOperations

Experiment = Process.Process()
Experiment.choose_methods(system="L63", integration="RK4", assimilation="EAKF")
truthList, timeList = Experiment.get_truth(0, 200, 0.01, [1,1,1])
truthLists = AnalysisOperations.get_var_lists_from_points(truthList)
obsList, obsTimeList = Experiment.get_observations(2.5, [0.5, 0.5, 0.5])
obsLists = AnalysisOperations.get_var_lists_from_points(obsList)
Graphics.graph_projection(["black", "orange"], ["solid", "scatter"], [1, 5], ["Truth", "Observations"], [truthLists[0], obsLists[0]], [truthLists[1], obsLists[1]], [truthLists[2], obsLists[2]], title="L63", xlabel="X", ylabel="Y", zlabel="Z")
Graphics.graph_projection(["black", "orange"], ["solid", "scatter"], [1, 5], ["Truth", "Observations"], [timeList, obsTimeList], [truthLists[0], obsLists[0]], title="Time Series in X", xlabel="Time", ylabel="X")
Graphics.graph_projection(["black", "orange"], ["solid", "scatter"], [1, 5], ["Truth", "Observations"], [timeList, obsTimeList], [truthLists[1], obsLists[1]], title="Time Series in Y", xlabel="Time", ylabel="Y")
Graphics.graph_projection(["black", "orange"], ["solid", "scatter"], [1, 5], ["Truth", "Observations"], [timeList, obsTimeList], [truthLists[2], obsLists[2]], title="Time Series in Z", xlabel="Time", ylabel="Z")