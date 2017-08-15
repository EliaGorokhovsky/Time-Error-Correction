"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import Process
import Graphics
import AnalysisOperations

Experiment = Process.Process(False)
error = [1, 1, 1, 0.1]
startTime = 0
endTime = 200
Experiment.choose_methods(system="L63+time", integration="RK4", assimilation="EAKF")
truthList, timeList = Experiment.get_truth(startTime, endTime, 0.01, [1,1,1,0])
print("Truth Generated")
truthLists = AnalysisOperations.get_var_lists_from_points(truthList)
obsList, obsTimeList = Experiment.get_observations(0.5, error, ["State", "State", "State", "Time"])
print("Observations Generated")
obsLists = AnalysisOperations.get_var_lists_from_points(obsList)
ensembleList, ensembleTimeList = Experiment.run_ensemble(startTime, endTime, 0.01, 80, error, error, obsList[0], [True, True, True, False], [2, 2, 2, 0])
print("Ensemble Run")
ensembleMeans = Experiment.get_ensemble_means()
ensembleMeansLists = AnalysisOperations.get_var_lists_from_points(ensembleMeans)
ensembleLists = AnalysisOperations.get_ensemble_var_lists_from_time_series(ensembleList)
print("RMSE:", AnalysisOperations.get_RMSE(ensembleMeans, truthList, [True, True, True, False]))
Graphics.graph_projection(["black", "orange", "red"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter", "dashed"] + ["dotted" for i in range(len(ensembleLists))], [1, 10, 0.75] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Actual Observations", "Ensemble Mean", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [truthLists[0], obsLists[0], ensembleMeansLists[0]] + [ensembleLists[i][0] for i in range(len(ensembleLists))], [truthLists[1], obsLists[1], ensembleMeansLists[1]] + [ensembleLists[i][1] for i in range(len(ensembleLists))], [truthLists[2], obsLists[2], ensembleMeansLists[2]] + [ensembleLists[i][2] for i in range(len(ensembleLists))], title="L63", xlabel="X", ylabel="Y", zlabel="Z")
Graphics.graph_projection(["black", "orange", "blue", "red"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter", "scatter", "dashed"] + ["dotted" for i in range(len(ensembleLists))], [1, 10, 10, 0.75] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Actual Observations", "Reported Observations", "Ensemble Mean", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsLists[3], obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists)+1)], [truthLists[0], obsLists[0], obsLists[0], ensembleMeansLists[0]] + [ensembleLists[i][0] for i in range(len(ensembleLists))], title="Time Series in X", xlabel="Time", ylabel="X", ylim=[-20,20])
Graphics.graph_projection(["black", "orange", "blue", "red"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter", "scatter", "dashed"] + ["dotted" for i in range(len(ensembleLists))], [1, 10, 10, 0.75] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Actual Observations", "Reported Observations", "Ensemble Mean", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsLists[3], obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists)+1)], [truthLists[1], obsLists[1], obsLists[1], ensembleMeansLists[1]] + [ensembleLists[i][1] for i in range(len(ensembleLists))], title="Time Series in Y", xlabel="Time", ylabel="Y", ylim=[-20,20])
Graphics.graph_projection(["black", "orange", "blue", "red"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter", "scatter", "dashed"] + ["dotted" for i in range(len(ensembleLists))], [1, 10, 10, 0.75] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Actual Observations", "Reported Observations", "Ensemble Mean", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsLists[3], obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists)+1)], [truthLists[2], obsLists[2], obsLists[2], ensembleMeansLists[2]] + [ensembleLists[i][2] for i in range(len(ensembleLists))], title="Time Series in Z", xlabel="Time", ylabel="Z", ylim=[-20,20])
Graphics.graph_projection(["black", "orange", "blue", "red"] + ["green" for i in range(len(ensembleLists))], ["solid", "scatter", "scatter", "dashed"] + ["dotted" for i in range(len(ensembleLists))], [1, 10, 10, 0.75] + [0.5 for i in range(len(ensembleLists))], ["Truth", "Actual Observations", "Reported Observations", "Ensemble Mean", "Ensemble"] + ["_nolegend_" for i in range(len(ensembleLists)-1)], [timeList, obsLists[3], obsTimeList] + [ensembleTimeList for i in range(len(ensembleLists)+1)], [truthLists[3], obsLists[3], obsLists[3], ensembleMeansLists[3]] + [ensembleLists[i][3] for i in range(len(ensembleLists))], title="Time", xlabel="Time", ylabel="Time", ylim=[0,200])