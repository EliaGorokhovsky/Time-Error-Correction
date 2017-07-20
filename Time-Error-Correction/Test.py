# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import Process
import Graphics
import AnalysisOperations

Experiment = Process.Process()
Experiment.choose_methods(system="L63", integration="RK4", assimilation="EAKF")
truthList, timeList = Experiment.get_truth(0, 200, 0.01, [1,1,1])
print("Truth Generated")
truthLists = AnalysisOperations.get_var_lists_from_points(truthList)
obsList, obsTimeList = Experiment.get_observations(0.5, [0.5, 0.5, 0.5])
print("Observations Generated")
obsLists = AnalysisOperations.get_var_lists_from_points(obsList)
ensembleList, ensembleTimeList = Experiment.run_ensemble(0, 200, 0.01, 20, [0.5,0.5,0.5], [0.5,0.5,0.5], obsList[0], [True, True, True])
print("Ensemble Run")
ensembleLists = AnalysisOperations.get_ensemble_var_lists_from_time_series(ensembleList)
Graphics.graph_projection(["black", "orange"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter"] + ["dotted" for i in range(len(ensembleLists))], [1, 10] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Observations", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [truthLists[0], obsLists[0]] + [ensembleLists[i][0] for i in range(len(ensembleLists))], [truthLists[1], obsLists[1]] + [ensembleLists[i][1] for i in range(len(ensembleLists))], [truthLists[2], obsLists[2]] + [ensembleLists[i][2] for i in range(len(ensembleLists))], title="L63", xlabel="X", ylabel="Y", zlabel="Z")
Graphics.graph_projection(["black", "orange"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter"] + ["dotted" for i in range(len(ensembleLists))], [1, 10] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Observations", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists))], [truthLists[0], obsLists[0]] + [ensembleLists[i][0] for i in range(len(ensembleLists))], title="Time Series in X", xlabel="Time", ylabel="X")
Graphics.graph_projection(["black", "orange"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter"] + ["dotted" for i in range(len(ensembleLists))], [1, 10] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Observations", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists))], [truthLists[1], obsLists[1]] + [ensembleLists[i][1] for i in range(len(ensembleLists))], title="Time Series in Y", xlabel="Time", ylabel="Y")
Graphics.graph_projection(["black", "orange"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter"] + ["dotted" for i in range(len(ensembleLists))], [1, 10] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Observations", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists))], [truthLists[2], obsLists[2]] + [ensembleLists[i][2] for i in range(len(ensembleLists))], title="Time Series in Z", xlabel="Time", ylabel="Z")