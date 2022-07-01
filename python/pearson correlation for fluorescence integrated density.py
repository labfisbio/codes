# -*- coding: utf-8 -*-
"""
Script to calculate the pearson correlation coeficient of the fluorescence integrated density of each channel
of the image. 

input: 3D image with 3 or 4 channels
outuput: xlsx with coeficiente for each cell folder (df_rcorr)
         xlsx with integrated density for each cell folder (df_int_den)

@author: Andre Thomaz, 02/24/2021
"""
######################################################
import numpy as np
from skimage import io
import pandas as pd
import os
######################################################

ch1_name = 'yh2ax'
ch2_name = 'myo5c'
ch3_name = 'fak'
ch4_name = 'dapi'
group = 'bclaf1-fak'

#####################################################
ch1_ch2 = ch1_name + '-' + ch2_name
ch1_ch3 = ch1_name + '-' + ch3_name
ch1_ch4 = ch1_name + '-' + ch4_name
ch2_ch3 = ch2_name + '-' + ch3_name
ch2_ch4 = ch2_name + '-' + ch4_name
ch3_ch4 = ch3_name + '-' + ch4_name

#####################################################
rcorr_total = np.array([])
#for each folder
for folder in os.listdir():
    
    if os.path.isdir(folder):
        
        os.chdir(folder)
        print(folder)
        current_folder = os.getcwd()
        
       
        ch1_array = np.array([])
        ch2_array = np.array([])
        ch3_array = np.array([])
        ch4_array = np.array([])
        
        # for each tif file in the folder
        for tif_file in os.listdir(current_folder):
            #print(tif_file) 
            if tif_file.split('.')[1] == 'tif':
            
               img = io.imread(tif_file) #load original image
            
               ch1_sumz = np.sum(np.array(img[:,:,0]))
               ch2_sumz = np.sum(np.array(img[:,:,1]))
               ch3_sumz = np.sum(np.array(img[:,:,2]))
               ch4_sumz = np.sum(np.array(img[:,:,3]))
               
               #array of intesities for each patch in the cell
               ch1_array = np.append(ch1_array, ch1_sumz)
               ch2_array = np.append(ch2_array, ch2_sumz)
               ch3_array = np.append(ch3_array, ch3_sumz)
               ch4_array = np.append(ch4_array, ch4_sumz)
        
       
        
        #pearson calculation after all patches computed
        pearson_ch1_ch2 = np.corrcoef(ch1_array, ch2_array)[0][1]
        pearson_ch1_ch3 = np.corrcoef(ch1_array, ch3_array)[0][1]
        pearson_ch1_ch4 = np.corrcoef(ch1_array, ch4_array)[0][1]
        pearson_ch2_ch3 = np.corrcoef(ch2_array, ch3_array)[0][1]
        pearson_ch2_ch4 = np.corrcoef(ch2_array, ch4_array)[0][1]
        pearson_ch3_ch4 = np.corrcoef(ch3_array, ch4_array)[0][1]
        
       
        
        #dataframe and save
        df_int_den = pd.DataFrame(np.transpose([ch1_array, ch2_array, ch3_array, ch4_array]), columns=[ch1_name, ch2_name, ch3_name, ch4_name])
               
        
        
        df_rcorr = pd.DataFrame(np.transpose([[pearson_ch1_ch2], [pearson_ch1_ch3],
                                              [pearson_ch1_ch4], [pearson_ch2_ch3], [pearson_ch2_ch4], [pearson_ch3_ch4]]), 
                                columns=[ch1_ch2, ch1_ch3, ch1_ch4, ch2_ch3, ch2_ch4, ch3_ch4], index=['rcorr'] )
                
   
        
        
        rcorr_total = np.append(rcorr_total, pearson_ch2_ch3)
        #cel_number = current_folder.split(' ')[1]
        filename_int_den = 'int-den.xlsx'
        filename_rcorr = 'rcorr.xlsx'
        
        
        df_int_den.to_excel(filename_int_den)
        df_rcorr.to_excel(filename_rcorr)
        
        
        
        
        os.chdir('..')
       
        print(folder+ " done")
df_rcorr_total = pd.DataFrame(np.transpose([rcorr_total]), columns=['rcorr'])
df_rcorr_total['group'] = group
filename_df_rcorr_total = 'rcorr_total.xlsx'
df_rcorr_total.to_excel(filename_df_rcorr_total)