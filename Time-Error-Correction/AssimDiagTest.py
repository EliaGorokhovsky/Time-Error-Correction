# -*- coding: utf-8 -*-
"""Another Test file."""
import DataAssimilation
import random
import EnsembleOperations
import numpy
from scipy import stats

print("Running analysis of EAKF step")
error = 0.01
ensemble = [[random.gauss(1, error), random.gauss(1, error), random.gauss(1, error)] for i in range(120)]
observation = [1, 1, 1]

ensembleValues = EnsembleOperations.get_values_from_ensemble(ensemble, [True, True, True])
observedValues = EnsembleOperations.get_observed_values_from_ensemble(ensembleValues)
initialValues = EnsembleOperations.copy_ensemble_values(ensembleValues)
initialObservedValues = EnsembleOperations.get_observed_values_from_ensemble(initialValues)
variables = ["X","Y","Z"]
print("---------------\nEnsemble Operations\n---------------")
testEnsemble = [[round(random.gauss(1, error), 3), round(random.gauss(1, error), 3), round(random.gauss(1, error), 3)] for i in range(4)]
testObservedStatus = [random.choice([True, False]) for i in range(3)]
print("Testing Ensemble:", testEnsemble, "with truth values", testObservedStatus)
testVals = EnsembleOperations.get_values_from_ensemble(testEnsemble, testObservedStatus)
print("get_values_from_ensemble:", testVals)
testObsVals = EnsembleOperations.get_observed_values_from_ensemble(testVals)
print("get_observed_values_from_ensemble:", testObsVals)
testCopy = EnsembleOperations.copy_ensemble_values(testVals)
print("copy_ensemble_values:", testCopy)
testNewEnsemble = EnsembleOperations.get_ensemble_from_values(testVals)
print("get_ensemble_from_values:", testNewEnsemble)

print("---------------\nEnsemble Check 1\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")
    
posteriorSpread, posteriorMean = DataAssimilation.get_posterior(observedValues, observation, [error, error, error])


print("---------------\nget_posterior\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")
    print("Observation: N(", round(observation[i], 3), ",0.500)")
    print("Posterior: N(", round(posteriorMean[i], 3), ",", round(posteriorSpread[i], 3), ")")

observationIncrements = DataAssimilation.obs_incs_EAKF(observedValues, posteriorMean, posteriorSpread)

print("---------------\nobs_incs_EAKF\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Mean Difference:",round(observation[i] - numpy.mean(observedValues[i]), 3))
    print("Mean Increment:", round(numpy.mean(observationIncrements[i]), 3))
 
print("---------------\nEnsemble Check 2\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")

stateIncrements = DataAssimilation.get_state_incs(ensembleValues, observationIncrements)
print("---------------\nget_state_incs\n---------------")
for i in range(len(variables)):
    print(variables[i])
    slope, intercept, r_value, p_value, std_err = stats.linregress(observedValues[0], observedValues[i])  
    print("Regression Slope by X:", round(slope, 5))
    print("Regression Correlation by X:", round(r_value, 5))             
    print("Increment from Regression by X:", round(numpy.mean(stateIncrements[0][i]), 3), "\n")
    slope, intercept, r_value, p_value, std_err = stats.linregress(observedValues[1], observedValues[i]) 
    print("Regression Slope by Y:", round(slope, 5))
    print("Regression Correlation by Y:", round(r_value, 5))     
    print("Increment from Regression by Y:", round(numpy.mean(stateIncrements[1][i]), 3), "\n")
    slope, intercept, r_value, p_value, std_err = stats.linregress(observedValues[1], observedValues[i])  
    print("Regression Slope by Z:", round(slope, 5))
    print("Regression Correlation by Z:", round(r_value, 5))     
    print("Increment from Regression by Z:", round(numpy.mean(stateIncrements[2][i]), 3), "\n")
    print("Total Increment:", round(numpy.mean(stateIncrements[0][i]) + numpy.mean(stateIncrements[1][i]) + numpy.mean(stateIncrements[2][i]), 3))
#-----------------------------------------------------------------------------------------------------------------------------


    
observedValues = list(EnsembleOperations.get_observed_values_from_ensemble(ensembleValues))
print("---------------\nEnsemble Check 3\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")



newEnsembleValues = EnsembleOperations.get_observed_values_from_ensemble(DataAssimilation.apply_state_increments(ensembleValues, stateIncrements))
print("---------------\napply_state_incs\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Previous Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")    
    print("Posterior: N(", round(posteriorMean[i], 3), ",", round(posteriorSpread[i], 3), ")")
    print("Ensemble Gaussian: N(", round(numpy.mean(newEnsembleValues[i]), 3), ",", round(numpy.std(newEnsembleValues[i]), 3), ")")

observedValues = list(newEnsembleValues)
    
print("---------------\nEnsemble Check 4\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Ensemble Gaussian: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")")

print("---------------\nFinal Assimilation\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Initial Ensemble Gaussian: N(", round(numpy.mean(initialObservedValues[i]), 3), ",", round(numpy.std(initialObservedValues[i]), 3), ")")
    print("Observation: N(", round(observation[i], 3), ",0.500)")
    print("Post-Assimilation Ensemble Dist: N(", round(numpy.mean(observedValues[i]), 3), ",", round(numpy.std(observedValues[i]), 3), ")" )

testEnsemble = DataAssimilation.EAKF(ensemble, observation, [error, error, error], [True, True, True])
testResult = EnsembleOperations.get_observed_values_from_ensemble(EnsembleOperations.get_values_from_ensemble(testEnsemble, [True, True, True]))
print("---------------\nEAKF\n---------------")
for i in range(len(variables)):
    print(variables[i])
    print("Initial Ensemble Gaussian: N(", round(numpy.mean(initialObservedValues[i]), 3), ",", round(numpy.std(initialObservedValues[i]), 3), ")")
    print("Observation: N(", round(observation[i], 3), ",0.500)")
    print("Post-Assimilation Ensemble Dist: N(", round(numpy.mean(testResult[i]), 3), ",", round(numpy.std(testResult[i]), 3), ")" )


