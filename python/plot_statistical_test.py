# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 13:36:05 2022

@author: athomaz
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


x_ticks = [0.15, 0.3]
#Plot######################
def plot(fig, y_heights, sems, x_labels, y_label):
    
   
  
    ax = fig.add_axes([-0,0,1,2.5])
    ax.bar(x_ticks, y_heights,  color=['black', 'grey'], edgecolor="black", 
           yerr=(sems),error_kw=dict(lw=2,capthick=2, capsize=30, zorder=0),  
            linewidth=4, width=0.12)
    
    
    plt.ylim([0,1.3*max(y_heights)])
    plt.xticks(x_ticks)
    plt.yticks(fontsize=24)
    ax.set_xticklabels(x_labels, fontsize=24)
    plt.ylabel(y_label, fontsize=28, labelpad=14)
    ax.tick_params(which='major', length=10, width=3)
    
    ax.spines['bottom'].set_linewidth(3)
    ax.spines['left'].set_linewidth(3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
      
# Custom function to draw the diff bars

def label_diff(ax, i ,j ,text ,Y , X, text_height, linewidth=2, color='black', fontsize=14):
   
    ax = ax
    x = (X[i]+X[j])/2
    
    y = 1.15*max(Y[i], Y[j])
    
    y_high = 1.2*max(Y[i], Y[j])
    y_low = 1.115*min(Y[i], Y[j])
    
    
    if text == "****":
        text_space = 0.015
    else:
        text_space = 0.010

    

    props = {'connectionstyle':'bar','arrowstyle':'-',
                 'shrinkA':0,'shrinkB':0,'linewidth':linewidth, 'color':color}
    
    ax.annotate(text, xy=(x-text_space , text_height ), zorder=10, annotation_clip=False, color=color, fontsize=fontsize)
    ax.annotate('', xy=(X[i],y), xytext=(X[j],y), arrowprops=props, annotation_clip=False)
    
    #extend left or right bar difference in column height
    props2 = {'arrowstyle':'-', 'linewidth':linewidth, 'color':color}
    
    
    if Y[j] > Y[i]:
        ax.annotate('', xy=(X[0], y_high), xytext=(X[0], y_low), arrowprops=props2, zorder=20)    
    else: 
        ax.annotate('', xy=(X[1], y_high), xytext=(X[1], y_low), arrowprops=props2, zorder=20) 