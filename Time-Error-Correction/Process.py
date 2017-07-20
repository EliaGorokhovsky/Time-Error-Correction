# -*- coding: utf-8 -*-
"""Operates the experimental process."""
import Systems
import IntegrationMethods
import DataAssimilation

class Process:
    """
    Runs a single test; contains all variables that must be remembered.
    """
    def __init__(self):
        """
        Initializes storage methods, etc.
        """
        self.timeList = []              #Stores times.
        self.truthsList = []            #Stores true values. truthsList[i] corresponds to timeList[i].
        self.obsList = []               #Stores observations. obsList[i] corresponds to timeList[i/(dt*obsInterval)]
        self.ensembleList = []          #Stores ensembles. ensembleList[i] corresponds to timeList[i].
  



      
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
            self.system = DataAssimilation.EAKF
        
        if "params" in kwargs:
            self.systemParameters = kwargs["params"]
        else: 
            self.systemParameters = None
            
    
    def get_truth(self, startTime, endTime, dt, startPosition):
        pos = list(startPosition)
        time = 0
        intervalLength = endTime - startTime
        steps = int(intervalLength / dt)
        for step in range(steps + 1):
            self.truthsList.append(list(pos))
            pos = self.integrationMethod(self.system, pos, time, dt)
            self.timeList.append(time)
            time += dt
        return self.truthsList, self.timeList
        
                
        
        

        
        

