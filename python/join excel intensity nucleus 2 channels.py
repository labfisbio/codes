# -*- coding: utf-8 -*-
"""
script to calculate statistics and plot bar graph for data from nucleus intensity.ijm macro
input: csv files inside folder with data of 2 channels nucleus intensity
1st channel int --  1 nucleus
2nd channel int -- 1 nucleus
1st channel int --  2 nucleus
2nd channel int -- 2 nucleus
output: bar plot with statistical comparison
@author: Andre Thomaz (athomaz@ifi.unicamp.br) @ 2022-02-14
"""

############################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as sts
#############################################################

group1 = 'ctr'
group2 = 'doxo'


############# Statistical Tests ##############################
def test_gaussian(sample):
    stat, p = sts.shapiro(sample)
    print('Statistics=%.3f, p=%.6f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')
        
def test_ks(sample1, sample2):
    print("Testing statistical significance")
    #stat, p = sts.ks_2samp(sample1, sample2, alternative='two-sided', mode='auto')
    stat, p = sts.mannwhitneyu(sample1, sample2)
    print('Statistics=%.3f, p=%.6f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
    	print('p: Same distribution (fail to reject H0)')
    else:
    	print('p: Different distribution (reject H0)')
        
def test_t(sample1, sample2):
    print("Testing statistical significance")
    stat, p = sts.ttest_ind(sample1, sample2)
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    # interpret
    alpha = 0.05
    if p > alpha:
        print('Same distributions (fail to reject H0)')
    else:
    	print('Different distributions (reject H0)')
#####################################





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

def label_diff(i ,j ,text ,Y , X=x_ticks):
   
    ax = plt.gca()
    x = (X[i]+X[j])/2
    
    y = 1.15*max(Y[i], Y[j])
    
    y_high = 1.2*max(Y[i], Y[j])
    y_low = 1.115*min(Y[i], Y[j])
    
    
    if text == "****":
        text_space = 0.015
    else:
        text_space = 0.010

    text_height = y*1.12

    props = {'connectionstyle':'bar','arrowstyle':'-',
                 'shrinkA':0,'shrinkB':0,'linewidth':2, 'color':'black'}
    ax.annotate(text, xy=(x-text_space , text_height ), zorder=10, fontsize=26)
    ax.annotate('', xy=(X[i],y), xytext=(X[j],y), arrowprops=props)
    
    #extend left or right bar difference in column height
    props2 = {'arrowstyle':'-', 'linewidth':2, 'color':'black'}
    
    
    if Y[j] > Y[i]:
        ax.annotate('', xy=(X[0], y_high), xytext=(X[0], y_low), arrowprops=props2, zorder=20)    
    else: 
        ax.annotate('', xy=(X[1], y_high), xytext=(X[1], y_low), arrowprops=props2, zorder=20) 



int_ctr = pd.DataFrame([])
int_doxo = pd.DataFrame([])

#for each folder grabs the values of rcorr
for folder in os.listdir():
    
    if os.path.isdir(folder):
        os.chdir(folder)
        for file in os.listdir():
            if file.split('.')[1] == 'csv':
                if folder == group1:
                    data = pd.read_csv(file)
                    int_ctr = int_ctr.append(data, ignore_index=True)
                elif folder == group2:
                    data = pd.read_csv(file)
                    int_doxo = int_doxo.append(data, ignore_index=True)
        os.chdir('..')
int_ctr = int_ctr.drop(int_ctr.columns[0], axis=1)
int_doxo =  int_doxo.drop(int_doxo.columns[0], axis=1)

int_ctr_myo = int_ctr.iloc[::2]
int_ctr_fak = int_ctr.iloc[1::2]

int_doxo_myo = int_doxo.iloc[::2]
int_doxo_fak = int_doxo.iloc[1::2]


#Test IntDenMyo
print('###############')
print('Testing gaussian ctr Myo')
test_gaussian(int_ctr_myo['RawIntDen'])
print('Testing gaussian doxo Myo')
test_gaussian(int_doxo_myo['RawIntDen'])
print('Testing ctr Myo and doxo Myo')
test_t(int_ctr_myo['RawIntDen'], int_doxo_myo['RawIntDen'])




int_ctr_myo_mean = int_ctr_myo['RawIntDen'].mean()
int_ctr_myo_sem = int_ctr_myo['RawIntDen'].sem()

int_doxo_myo_mean = int_doxo_myo['RawIntDen'].mean()
int_doxo_myo_sem = int_doxo_myo['RawIntDen'].sem()

int_doxo_myo_mean = int_doxo_myo_mean/int_ctr_myo_mean
int_doxo_myo_sem = int_doxo_myo_sem/int_ctr_myo_mean
int_ctr_myo_sem = int_ctr_myo_sem/int_ctr_myo_mean
int_ctr_myo_mean = int_ctr_myo_mean/int_ctr_myo_mean

y_heights = [int_ctr_myo_mean, int_doxo_myo_mean]
sems = [int_ctr_myo_sem, int_doxo_myo_sem]
x_labels = ['CTR', 'Doxo-Myo-Vb']
y_label = "Myosin Vb Intensity at Nucleus (A.U.)"



fig, ax = plt.subplots()
plot(fig, y_heights, sems, x_labels, y_label)
label_diff(0, 1, 'N.S.', y_heights)    

#Test IntDenMyo
print('###############')
print('Testing gaussian ctr FAK')
test_gaussian(int_ctr_fak['RawIntDen'])
print('Testing gaussian doxo FAK')
test_gaussian(int_doxo_fak['RawIntDen'])
print('Testing ctr Myo and doxo Myo')
test_ks(int_ctr_fak['RawIntDen'], int_doxo_fak['RawIntDen'])




int_ctr_fak_mean = int_ctr_fak['RawIntDen'].mean()
int_ctr_fak_sem = int_ctr_fak['RawIntDen'].sem()

int_doxo_fak_mean = int_doxo_fak['RawIntDen'].mean()
int_doxo_fak_sem = int_doxo_fak['RawIntDen'].sem()

int_doxo_fak_mean = int_doxo_fak_mean/int_ctr_fak_mean
int_doxo_fak_sem = int_doxo_fak_sem/int_ctr_fak_mean
int_ctr_fak_sem = int_ctr_fak_sem/int_ctr_fak_mean
int_ctr_fak_mean = int_ctr_fak_mean/int_ctr_fak_mean

y_heights = [int_ctr_fak_mean, int_doxo_fak_mean]
sems = [int_ctr_fak_sem, int_doxo_fak_sem]
x_labels = ['CTR', 'Doxo-FAK']
y_label = "FAK Intensity at Nucleus (A.U.)"



fig, ax = plt.subplots()
plot(fig, y_heights, sems, x_labels, y_label)
label_diff(0, 1, 'N.S.', y_heights)    






