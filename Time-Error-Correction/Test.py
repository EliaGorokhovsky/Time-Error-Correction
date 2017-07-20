# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import Process
import Graphics
import AnalysisOperations

Experiment = Process.Process()
Experiment.choose_methods(system="L63", integration="RK4", assimilation="EAKF")
truthList, timeList = Experiment.get_truth(0, 200, 0.01, [1,1,1])
truthLists = AnalysisOperations.get_var_lists_from_truths(truthList)
Graphics.graph_projection(["black"], ["solid"], [1], "Truth", [truthLists[0]], [truthLists[1]], [truthLists[2]], title="L63", xlabel="X", ylabel="Y", zlabel="Z")
