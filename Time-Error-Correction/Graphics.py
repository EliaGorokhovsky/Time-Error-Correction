# -*- coding: utf-8 -*-
"""Contains functions for graphically viewing data."""

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats, integrate
import numpy as np
import matplotlib.mlab as mlab
import math




def graph_projection(colors, lineStyles, lineWidths, labels, xLists, yLists, *zLists, **kwargs):
    """
    Graphs a 2-d or 3-d projection of a system.  
    
    Takes arrays of colors, line styles, line widths, labels (_nolegend_ for no label) and datasets to plot. All should be the same size.
    """
    if zLists != ():
        #graph in 3-d
        zLists = zLists[0]      #Python optional args return as tuples.
        fig = plot.figure()
        ax = fig.gca(projection = '3d')
        for dataset in range(len(colors)):
            if lineStyles[dataset] == "scatter":
                ax.scatter(xLists[dataset], yLists[dataset], zs=zLists[dataset], color=colors[dataset], label=labels[dataset], s=lineWidths[dataset])
            else:
                ax.plot(xLists[dataset], yLists[dataset], zs=zLists[dataset], color=colors[dataset], linestyle=lineStyles[dataset], linewidth=lineWidths[dataset], label=labels[dataset])
        legend = ax.legend(loc='upper right', shadow=True)
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        for label in legend.get_texts():
            label.set_fontsize('large')   
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        if "title" in kwargs:
            plot.title(kwargs["title"])  
        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"])
        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"])
        if "zlabel" in kwargs:
            ax.set_zlabel(kwargs["zlabel"])
        if "xlim" in kwargs:
            ax.set_xlim(kwargs["xlim"][0], kwargs["xlim"][1])
        if "ylim" in kwargs:
            ax.set_ylim(kwargs["ylim"][0], kwargs["ylim"][1])
        if "zlim" in kwargs:
            ax.set_zlim(kwargs["zlim"][0], kwargs["zlim"][1])
    else:
        fig = plot.figure()
        ax = fig.gca()
        for dataset in range(len(colors)):
            if lineStyles[dataset] == "scatter":
                ax.scatter(xLists[dataset], yLists[dataset], color=colors[dataset], label=labels[dataset], s=lineWidths[dataset])
            else:
                ax.plot(xLists[dataset], yLists[dataset], color=colors[dataset], linestyle=lineStyles[dataset], linewidth=lineWidths[dataset], label=labels[dataset])
        legend = ax.legend(loc='upper right', shadow=True)
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        for label in legend.get_texts():
            label.set_fontsize('large')   
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        if "title" in kwargs:
            plot.title(kwargs["title"])
        if "xlabel" in kwargs:
            ax.set_xlabel(kwargs["xlabel"])
        if "ylabel" in kwargs:
            ax.set_ylabel(kwargs["ylabel"])
        if "xlim" in kwargs:
            ax.set_xlim(kwargs["xlim"][0], kwargs["xlim"][1])
        if "ylim" in kwargs:
            ax.set_ylim(kwargs["ylim"][0], kwargs["ylim"][1])
            


def rank_histogram(binList, colors, linewidths, **kwargs):
    fig = plot.figure()
    ax = fig.gca()
    widths = [binList[i+1] - binList[i] for i in range(len(binList)-1)]
    normalFit = mlab.normpdf(binList, np.mean(binList), np.std(binList))
    ax.plot(binList, normalFit, "r--")   
    areaValue = 1/len(widths)    
    ax.bar(binList[:-1], [areaValue/widths[i] for i in range(len(widths))], width=widths, color=colors, linewidth=linewidths)
    if "title" in kwargs:
        plot.title(kwargs["title"])
    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"])
    if "xlim" in kwargs:
        ax.set_xlim(kwargs["xlim"][0], kwargs["xlim"][1])
    if "ylim" in kwargs:
        ax.set_ylim(kwargs["ylim"][0], kwargs["ylim"][1])
        
        
def kernel_density_estimation(points, colors, bandwidths, lineWidths, lineStyles, labels, **kwargs):
    fig = plot.figure()
    ax = fig.gca()
    newPoints = [min(points) - 50*0.01 + i*0.01 for i in range(50)] + list(points) + [max(points) + 0.01 + i*0.01 for i in range(50)]
    for dataset in range(len(colors)):
#        probabilityValues = [0 for i in range(len(newPoints))]
#        for i in range(len(points)):
#            norm = np.array(mlab.normpdf(newPoints, points[i], bandwidths[dataset]))
#            newProbabilityValues = [probabilityValues[i] + norm[i] for i in range(len(norm))]
#            probabilityValues = newProbabilityValues[:]
#        area = abs(integrate.simps(probabilityValues, x=newPoints, even='avg'))
#        probabilityValues /= area
#        ax.plot(newPoints, probabilityValues, color=colors[dataset], linestyle = lineStyles[dataset], linewidth=lineWidths[dataset], label=labels[dataset])
        probabilityValues = stats.gaussian_kde(points, bw_method="silverman")
        ax.plot(points, probabilityValues(points), color=colors[dataset], linestyle = lineStyles[dataset], linewidth=lineWidths[dataset], label=labels[dataset])
    normalFit = mlab.normpdf(points, np.mean(points), np.std(points))
    ax.plot(points, normalFit, "r--", label="Gaussian Fit to Data")   
    legend = ax.legend(loc='upper right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')
    for label in legend.get_texts():
        label.set_fontsize('large')   
    for label in legend.get_lines():
        label.set_linewidth(1.5)
    if "title" in kwargs:
        plot.title(kwargs["title"])  
    if "xlabel" in kwargs:
        ax.set_xlabel(kwargs["xlabel"])
    if "ylabel" in kwargs:
        ax.set_ylabel(kwargs["ylabel"])
    if "zlabel" in kwargs:
        ax.set_zlabel(kwargs["zlabel"])
    if "xlim" in kwargs:
        ax.set_xlim(kwargs["xlim"][0], kwargs["xlim"][1])
    if "ylim" in kwargs:
        ax.set_ylim(kwargs["ylim"][0], kwargs["ylim"][1])
    if "zlim" in kwargs:
        ax.set_zlim(kwargs["zlim"][0], kwargs["zlim"][1])    
        
        


def normal_rhf(ensembleValues, likelihood, observation, newEnsemble):
    baseValues = [i*0.01 for i in range((math.floor(min(ensembleValues))-5)*100, (math.ceil(max(ensembleValues))+5)*100)]
    likeDistribution = mlab.normpdf(np.array(baseValues), observation, np.array(likelihood))
    likeEnsemble = mlab.normpdf(np.array(ensembleValues), observation, np.array(likelihood))
    likeNewEnsemble = mlab.normpdf(np.array(newEnsemble), observation, np.array(likelihood))
    priorDist = mlab.normpdf(np.array(baseValues), np.mean(ensembleValues), np.std(ensembleValues))
    postDist = mlab.normpdf(np.array(baseValues), np.mean(newEnsemble), np.std(newEnsemble))

    fig = plot.figure()
    ax = fig.gca()
    ax.plot(baseValues, likeDistribution, color="red")
    ax.plot(baseValues, priorDist, color="green")
    ax.plot(baseValues, postDist, color="blue")
    #ax.scatter(ensembleValues, likeEnsemble, color="green")
    #ax.scatter(newEnsemble, likeNewEnsemble, color="blue")
        
        
    
    

    




                
            
