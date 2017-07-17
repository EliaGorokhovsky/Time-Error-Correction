# -*- coding: utf-8 -*-
"""Contains functions for graphically viewing data."""

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from scipy import stats
import numpy as np




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
            




def plot_bivariate(colors, sizes, stateIncrements, ensembleValues, xvar, yvar, observation):
    """
    Graphs a 2-dimensional bivariate plot of observation increments. Currently experimental.
    """
    
    fig = plot.figure()
    ax = fig.gca()
    slope, intercept, r_value, p_value, std_err = stats.linregress(ensembleValues[xvar][1],ensembleValues[yvar][1])    
    print("Slope in Graph:", slope, "Slope in Assim:", stateIncrements[xvar][yvar][0]/stateIncrements[xvar][xvar][0])    
    
    for i in range(len(ensembleValues[0][1])):
        ax.arrow(ensembleValues[xvar][1][i], ensembleValues[yvar][1][i], stateIncrements[xvar][xvar][i], stateIncrements[xvar][yvar][i], linewidth=1)
        #ax.arrow(ensembleValues[xvar][1][i], ensembleValues[yvar][1][i], stateIncrements[xvar][xvar][i], 0, linewidth=1)
        #ax.arrow(ensembleValues[xvar][1][i], ensembleValues[yvar][1][i], 0, stateIncrements[xvar][yvar][i], linewidth=1)
    endpoints = [[] for i in range(len(ensembleValues))]
    for i in range(len(endpoints)):
        endpoints[i] = [ensembleValues[i][1][j] + stateIncrements[k][i][j] for j in range(len(ensembleValues[0][1])) for k in range(len(stateIncrements))]
    ax.plot([-40, 40], [intercept - 40*slope, intercept + 40*slope], color="red")
    ax.scatter(endpoints[xvar], endpoints[yvar], s = 25, color = "orange")    
    ax.scatter(ensembleValues[xvar][1], ensembleValues[yvar][1], s = sizes[0], color = colors[0])    
    ax.scatter([observation[xvar]], [observation[yvar]], s = sizes[1], color = colors[1])
        
    plot.show()
    
                
            
