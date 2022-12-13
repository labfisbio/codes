# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 13:10:29 2022

@author: athomaz
"""

############################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#############################################################

protein_1 = pd.read_csv('ptk2.csv')
protein_1 = protein_1.drop(protein_1.columns[0], axis=1)
protein_1['Y'] = protein_1['Y']/protein_1['Y'].max()
protein_2 = pd.read_csv('bclaf1.csv')
protein_2 = protein_2.drop(protein_2.columns[0], axis=1)
protein_2['Y'] = protein_2['Y']/protein_2['Y'].max()
protein_3 = pd.read_csv('ub.csv')
protein_3 = protein_3.drop(protein_3.columns[0], axis=1)
protein_3['Y'] = protein_3['Y']/protein_3['Y'].max()

plt.plot(protein_1.X, protein_1.Y,  'g-', label='PTK2',)
plt.plot(protein_2.X, protein_2.Y,  'r-', label='BCLAF1',)
plt.plot(protein_3.X, protein_3.Y,  'gray', label='UB',)
plt.ylabel('Intensity (A.U.)')
plt.xlabel("Distance ("+r'$\mu m$'+ ")")


plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig("ptk2 bclaf1 ub line profile.png", dpi=600)