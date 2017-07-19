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
            





                
            
