# -*- coding: utf-8 -*-
"""Operates the experimental process."""
import AnalysisOperations
import Systems
import IntegrationMethods
import DataAssimilation
import MiscFunctions
import EnsembleOperations
import numpy as np
import ExperimentalThings

class Process:
    """
    Runs a single test; contains all variables that must be remembered.
    """
    def __init__(self, assimilation):
        """
        Initializes storage methods, etc.
        """
        self.timeList = []              #Stores times.
        self.truthsList = []            #Stores true values. truthsList[i] corresponds to timeList[i].
        self.obsList = []               #Stores observations. obsList[i] corresponds to timeList[i/(dt*obsInterval)]
        self.ensembleList = []          #Stores ensembles. ensembleList[i] corresponds to timeList[i].
        self.ensembleMeansList = []     #Stores ensemble means.        
        self.obsTimeList = []           #Stores times at which observations are taken.      
        self.ensembleTimeList = []      #Stores times for ensemble list.        
        
        self.dt = 0                     #The timestep for truth.              
        self.experimentalStatus = assimilation

      
    def choose_methods(self, **kwargs):
        """
        Writes the model, integration method, assimilation method to the Process object memory.
        kwargs include system, integration, assimilation.
        """
        if "system" in kwargs:                                  #If there is an argument labelled "system"
            if kwargs["system"] in Systems.methodsHash:         #If that system exists in the Systems file, remember it.    
                self.system = Systems.methodsHash[kwargs["system"]]
            else:                                               #Otherwise, abort.
                raise ValueError(kwargs["system"], "is not a valid dynamical system for testing.")
        else:
            self.system = Systems.Lorenz63                      #Default system
            
        if "integration" in kwargs:
            if kwargs["integration"] in IntegrationMethods.methodsHash:
                self.integrationMethod = IntegrationMethods.methodsHash[kwargs["integration"]]
            else:
                raise ValueError(kwargs["integration"], "is not a valid integration method for testing.")
        else:
            self.integrationMethod = IntegrationMethods.rk4        
            
        if "assimilation" in kwargs:
            if kwargs["assimilation"] in DataAssimilation.methodsHash:
                self.assimilationMethod = DataAssimilation.methodsHash[kwargs["assimilation"]]
            else:
                raise ValueError(kwargs["assimilation"], "is not a valid assimilation method for testing.")
        else:
            self.assimilation = DataAssimilation.EAKF
        
        if "params" in kwargs:
            self.systemParameters = kwargs["params"]
        else: 
            self.systemParameters = None

    

        
    
    def get_truth(self, startTime, endTime, dt, startPosition):
        """
        Gets the true values and times for each time between startTime and endTime, inclusive, with an interval of dt.        
        """
        self.dt = dt
        pos = list(startPosition)
        time = 0
        intervalLength = endTime - startTime
        steps = int(intervalLength / self.dt)
        for step in range(steps + 1):
            self.truthsList.append(list(pos))
            self.timeList.append(time)
            pos = self.integrationMethod(self.system, pos, time, self.dt)
            time += self.dt
        return self.truthsList, self.timeList
        
        
        
        
        
    def get_observations(self, observationInterval, error, errorType):
        """
        Generates observations every observationInterval with specified error (Gaussian stdev) in variablenum directions.
        """
        self.errorType = errorType
        observationCount = MiscFunctions.mod(self.timeList[-1] - self.timeList[0], observationInterval)[0]
        #self.obsList = [MiscFunctions.perturb_point(self.truthsList[int(observation * observationInterval / self.dt)], error) for observation in range(observationCount)]
        self.obsList = [MiscFunctions.generate_typed_error(self.truthsList[int(observation * observationInterval / self.dt)], error, self.errorType, self.dt, self.system, self.integrationMethod, self.systemParameters) for observation in range(observationCount+1)]
        self.obsTimeList = [round(float(observation * observationInterval), 5) for observation in range(observationCount+1)]
        return self.obsList, self.obsTimeList
        
        
        
        
    def run_ensemble(self, startTime, endTime, dt, ensembleSize, reportedError, ensembleSpread, startPoint, observedStatus, inflateScalars):
        """
        Integrates ensemble points through model, performing assimilation.
        """        
        self.ensembledt = dt
        ensemble = [MiscFunctions.perturb_point(startPoint, ensembleSpread) for i in range(ensembleSize)]
        time = 0
        intervalLength = endTime - startTime
        steps = int(intervalLength / self.ensembledt)
        for step in range(steps + 1):
            if round(time, 5) in self.obsTimeList and time != 0:
                ensemble = EnsembleOperations.inflate(ensemble, inflateScalars)
                #previousEnsemble = AnalysisOperations.get_var_lists_from_points(EnsembleOperations.copy_ensemble(ensemble))
                if self.experimentalStatus and self.assimilationMethod != DataAssimilation.RHF:
                    observation, observationLikelihood = ExperimentalThings.get_adaptive_likelihood(self.obsList[self.obsTimeList.index(round(time, 5))], reportedError, self.errorType, self.dt, self.system, self.integrationMethod, self.systemParameters)
                    ensemble = self.assimilationMethod(ensemble, observation, observationLikelihood, observedStatus)
                elif self.experimentalStatus and self.assimilationMethod == DataAssimilation.RHF:
                    observationLikelihood = ExperimentalThings.get_adaptive_likelihood(self.obsList[self.obsTimeList.index(round(time, 5))], reportedError, self.errorType, self.dt, self.system, self.integrationMethod, self.systemParameters, ensemble=ensemble)
                    ensemble = self.assimilationMethod(ensemble, 0, observationLikelihood, observedStatus)
                else:
                    ensemble = self.assimilationMethod(ensemble, self.obsList[self.obsTimeList.index(round(time, 5))], np.array(reportedError), observedStatus)
                #ensembleValues = AnalysisOperations.get_var_lists_from_points(ensemble)
                #print("Assimilated X from N("+str(np.mean(previousEnsemble[0]))+"|"+str(np.std(previousEnsemble[0]), ddof=1)+") to N(" + str(np.mean(ensembleValues[0]))+"|"+str(np.std(ensembleValues[0]), ddof=1)+") using observation N(" + str(self.obsList[self.obsTimeList.index(round(time, 5))][0])+"|"+str(reportedError[0])+") at time", time)
                #print("Assimilated Y from N("+str(np.mean(previousEnsemble[1]))+"|"+str(np.std(previousEnsemble[1]), ddof=1)+") to N(" + str(np.mean(ensembleValues[1]))+"|"+str(np.std(ensembleValues[1]), ddof=1)+") using observation " + str(self.obsList[self.obsTimeList.index(round(time, 5))][1]))
                #print("Assimilated Z from N("+str(np.mean(previousEnsemble[2]))+"|"+str(np.std(previousEnsemble[2]), ddof=1)+") to N(" + str(np.mean(ensembleValues[2]))+"|"+str(np.std(ensembleValues[2]), ddof=1)+") using observation " + str(self.obsList[self.obsTimeList.index(round(time, 5))][2]))
                #print("Assimilated from", previousEnsemble, "to", ensembleValues, "using observation", self.obsList[self.obsTimeList.index(round(time, 5))])
            self.ensembleList.append(EnsembleOperations.copy_ensemble(ensemble))
            self.ensembleTimeList.append(time)
            ensemble = [self.integrationMethod(self.system, point, time, self.ensembledt) for point in ensemble]
            time += self.ensembledt
        return self.ensembleList, self.ensembleTimeList





    def get_ensemble_means(self):
        """
        Returns lists of variable means with length equal to number of timesteps.
        """           
        self.ensembleMeansList = [[np.mean(AnalysisOperations.get_var_lists_from_points(self.ensembleList[step])[var]) for var in range(len(AnalysisOperations.get_var_lists_from_points(self.ensembleList[step])))] for step in range(len(self.ensembleList))]
        return self.ensembleMeansList      
            
            
            
            
            
    
    
        
                
        
        

        
        

