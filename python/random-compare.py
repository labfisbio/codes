# -*- coding: utf-8 -*-
"""
Script to compare 2 sets of correlation data.
Input: xlsx files with correlations coeficientes of each group
Outuput: graphs 

@author: athomaz
"""

############################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#############################################################

###Name of xlsx files to compare#############
proteins = 'bclaf1-fak' #group1
group2 = 'random'
int_den_group1 = 'rcorr_total-'+proteins+'-exp.xlsx'
int_den_group2 = 'rcorr_total-'+proteins+'-random.xlsx'
corr_pix_group1 = 'pix_total-'+proteins+'-exp.xlsx'
corr_pix_group2 = 'pix_total-'+proteins+'-random.xlsx'

############################################


#load excel file
df_group1 = pd.read_excel(int_den_group1)
df_group2 = pd.read_excel(int_den_group2)
df = pd.concat([df_group1, df_group2], ignore_index=True)

###catplot
sns.catplot(x='group', y='rcorr', data=df, kind='swarm')
x_l = [-5,45]
y_l = [0,0]
plt.plot(x_l, y_l,'k:', alpha=0.4)
plt.yticks((-1,-0.5,0,0.5,1))
ylabel = 'Correlation Coefficient of BCLAF1 clusters \n and yH2AX (Integrated Density/cell)'
plt.ylabel(ylabel)
plt.xlabel('')
plt.tight_layout()    
plt.savefig('pearson-compare-bclaf1-fak.png', dpi=600)



#############################
df_group1 = pd.read_excel(corr_pix_group1)
df_group2 = pd.read_excel(corr_pix_group2)
#df = pd.concat([df_group1, df_group2], ignore_index=True)

#############################
plt.figure()
sns.kdeplot(df_group1['rcorr'], label=proteins)
sns.kdeplot(df_group2['rcorr'], label=group2)
plt.legend()
plt.xlabel('Histogram Pearson Pixel ')
plt.tight_layout()
plt.savefig('pixel-corr-compare-bclaf1-fak.png', dpi=600)






