# -*- coding: utf-8 -*-
"""Testfile for testing the code."""
#TODO: unittests should replace test file eventually.

import DataAssimilation
import EnsembleOperations
import IntegrationMethods
import Systems
import Graphics

Graphics.graph_projection(["red", "blue", "green"], ["dotted", "dashed", "solid"], [1, 2, 3], ["red", "green", "_nolabel_"], [[1,2], [1,3], [1,4]], [[1,4], [1,3], [1,2]], title="Graph", xlabel="X", ylabel="Y")
