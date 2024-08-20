# -*- coding: utf-8 -*-
"""
script to calculate statistics and plot bar graph for any number of groups
input: csv files inside folders for each group, filenames should end with cell number before .csv 01, 02, etc
protein: should be the proetin to be analyzed that comes before cell number in filename
output: bar plot with statistical comparison
!!! statannotations only works with seaborn <=11.2
@author: Prof. Andre Thomaz (athomaz@unicamp.br) @ 2024-03-18
"""

############################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#import statistical_tests as st
from statannotations.Annotator import Annotator
from itertools import combinations
#############################################################

#parameters
#Number of bars will be number of groups in groups list
groups = ['CT', 'DOX', 'PBP', 'PBP+DOX']
protein = 'PTK2'
x_label = 'Treatment'
y_label = 'PTK2 Intensity at Nucleus'
fig_name = 'FAK.png'


#load all data from the folders
df_groups = pd.DataFrame([]) 
for group in groups:
    os.chdir(group)
    for file in os.listdir():
        cell_number = file.split(protein+'_')[1][0:2]
        df = pd.read_csv(file)
        df['group'] = group
        df['cell number'] = cell_number
        df_groups = pd.concat([df_groups, df], ignore_index=True)

    os.chdir('..')

#dictionary with number of cells per group
n_cells = {}
for group in groups:
    n_cells[group] = df_groups[df_groups['group'] == group]['cell number'].nunique()


print('######################################################')
print('Number of cells per group')
print(n_cells)
print('######################################################')


#old statistical test, statannotation does it now
#Test IntDenGroup
# for group in enumerate(groups):
#     print('###############')
#     print('Testing gaussian', group)
#     group_mask = df_groups['group'] == group
#     st.test_gaussian(df_groups[group_mask]['RawIntDen'])




# for combs in group_combs:
#     print('###############')
#     print('Testing statistical difference')
#     print(combs[0])
#     print(combs[1])
#     group_mask_1 = df_groups['group'] == combs[0]
#     group_mask_2 = df_groups['group'] == combs[1]
#     st.mannwhitneyu(df_groups[group_mask_1]['RawIntDen'], df_groups[group_mask_2]['RawIntDen'])



#Calculations to get groups means and groups sems
df_groups_means = []
df_groups_sems = [] 

for group in groups:
    group_mask = df_groups['group'] == group
    df_groups_means.append(df_groups[group_mask]['RawIntDen'].mean())
    df_groups_sems.append(df_groups[group_mask]['RawIntDen'].sem())


df_groups['RawIntDen'] = df_groups['RawIntDen'].div(df_groups_means[0])


df_groups_sems = df_groups_sems/df_groups_means[0]
df_groups_means = df_groups_means/df_groups_means[0]

df_means = pd.DataFrame([])

for i, group in enumerate(groups):
    df_means.at[i, 'Mean'] = df_groups_means[i]
    df_means.at[i, 'SEM'] = df_groups_sems[i]
    df_means.at[i, 'group'] = group




#From statannotation github example
pairs = list(combinations(groups, 2))


plot_params = {
    'data': df_groups,
    'x' : 'group',
    'y' : 'RawIntDen',
    'order' : groups,
    'palette' : 'gray',
    #'hue' : 'group',
    'edgecolor' : 'black', 
    'ci' : None,
    'dodge': False,
    }

with sns.plotting_context('notebook', font_scale=1.4):
    # Create new plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    


    # Plot with seaborn
    sns.barplot(ax=ax, **plot_params)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    for i in range(df_means['group'].nunique()):
       plt.plot([i,i], [df_means.at[i,'Mean']-df_means.at[i, 'SEM'], df_means.at[i,'Mean']+df_means.at[i, 'SEM']], c='black', linewidth=1, alpha=0.5)
       plt.plot([i-0.08,i+0.08], [df_means.at[i,'Mean']-df_means.at[i, 'SEM'], df_means.at[i,'Mean']-df_means.at[i, 'SEM']], c='black', linewidth=1, alpha=0.5)
       plt.plot([i-0.08,i+0.08], [df_means.at[i,'Mean']+df_means.at[i, 'SEM'], df_means.at[i,'Mean']+df_means.at[i, 'SEM']], c='black', linewidth=1, alpha=0.5)

    # Add annotations
    annotator = Annotator(ax, pairs, **plot_params)
    annotator.configure(test='Mann-Whitney').apply_and_annotate()

plt.savefig(fig_name, dpi=600)
    


