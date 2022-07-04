# -*- coding: utf-8 -*-
"""
Script to calculate the pearson correlation coeficient of each pixel of each patch 
of the image for images in a folder. Pacthes = small images containing the structures to be correlated

input: 2D image with 4 channels
outuput: xlsx with pearson coefficient for all cells (df_rcorr)
          xlsx at root folder with coeficientes for all cells

@author: Andre Thomaz (athomaz@ifi.unicam.br), 02/24/2021
"""
######################################################
import numpy as np
from skimage import io
import pandas as pd
import os
######################################################

ch1_name = 'yh2ax'
ch2_name = 'bclaf1'
ch3_name = 'fak'
ch4_name = 'dapi'
group = 'exp' #it will be added to the total xlsx file name
#####################################################
ch1_ch2 = ch1_name + '-' + ch2_name
ch1_ch3 = ch1_name + '-' + ch3_name
ch1_ch4 = ch1_name + '-' + ch4_name
ch2_ch3 = ch2_name + '-' + ch3_name
ch2_ch4 = ch2_name + '-' + ch4_name
ch3_ch4 = ch3_name + '-' + ch4_name

#####################################################


pix_total_ch1_ch2 = np.array([])
pix_total_ch1_ch3 = np.array([])
pix_total_ch2_ch3 = np.array([])



#for each folder
for folder in os.listdir():
    
    if os.path.isdir(folder):
        os.chdir(folder)
        print(folder)
        current_folder = os.getcwd()
        
        rcorr_ch1_ch2_total = np.array([])
        rcorr_ch1_ch3_total = np.array([])
        rcorr_ch2_ch3_total = np.array([])
        #rcorr_gamma_dapi_total = np.array([])

        # for each tif file in the folder
        for tif_file in os.listdir(current_folder):
            #print(tif_file) 
            if tif_file.split('.')[1] == 'tif': 
                
                img = io.imread(tif_file) #load image
                print(tif_file)
            
                #load channels to correlate
                ch1_sumz = np.array(img[:,:,0])
                ch2_sumz = np.array(img[:,:,1])
                ch3_sumz = np.array(img[:,:,2])
                
                           
                #transform image in 1D array and calculate pearson coefficent
                rcorr_ch1_ch2 = np.corrcoef(ch1_sumz.flatten(), ch2_sumz.flatten())[0][1]
                rcorr_ch1_ch3 = np.corrcoef(ch1_sumz.flatten(), ch3_sumz.flatten())[0][1]
                rcorr_ch2_ch3 = np.corrcoef(ch2_sumz.flatten(), ch3_sumz.flatten())[0][1]
                
             
                
              
                #make the array for all patches for each cell
                rcorr_ch1_ch2_total = np.append(rcorr_ch1_ch2_total, rcorr_ch1_ch2)
                rcorr_ch1_ch3_total = np.append(rcorr_ch1_ch3_total, rcorr_ch1_ch3)
                rcorr_ch2_ch3_total  = np.append(rcorr_ch2_ch3_total, rcorr_ch2_ch3)
                
                
        #array with all the measurements
        pix_total_ch1_ch2 = np.append(pix_total_ch1_ch2, rcorr_ch1_ch2_total)
        pix_total_ch1_ch3 = np.append(pix_total_ch1_ch3, rcorr_ch1_ch3_total)
        pix_total_ch2_ch3 = np.append(pix_total_ch2_ch3, rcorr_ch2_ch3_total)
           
        #individual saves
        df_rcorr = pd.DataFrame(np.transpose([rcorr_ch1_ch2_total, rcorr_ch1_ch3_total , rcorr_ch2_ch3_total ]), 
                                columns=[ch1_ch2, ch1_ch3, ch2_ch3])
                
       
        filename_rcorr = 'corr pixel.xlsx'
       
        
        
       
        df_rcorr.to_excel( filename_rcorr)
        
        os.chdir('..')
        #print(os.getcwd())
                
        print(folder+ " done")
        
        
#total files to DataFrame      
pix_total_ch1_ch2 = pd.DataFrame(np.transpose([pix_total_ch1_ch2]), columns=['rcorr'])
pix_total_ch1_ch3 = pd.DataFrame(np.transpose([pix_total_ch1_ch3]), columns=['rcorr'])
pix_total_ch2_ch3 = pd.DataFrame(np.transpose([pix_total_ch2_ch3]), columns=['rcorr'])

pix_total_ch1_ch2['proteins'] = ch1_ch2
pix_total_ch1_ch2['group'] = group
pix_total_ch1_ch3['proteins'] = ch1_ch3
pix_total_ch1_ch3['group'] = group
pix_total_ch2_ch3['proteins'] = ch2_ch3
pix_total_ch2_ch3['group'] = group




#save total files
filename_pix_total_ch1_ch2 = 'pix_total-'+ch1_ch2+'-'+group+'.xlsx'
pix_total_ch1_ch2.to_excel(filename_pix_total_ch1_ch2)
filename_pix_total_ch1_ch3 = 'pix_total-'+ch1_ch3+'-'+group+'.xlsx'
pix_total_ch1_ch3.to_excel(filename_pix_total_ch1_ch3)
filename_pix_total_ch2_ch3 = 'pix_total-'+ch2_ch3+'-'+group+'.xlsx'
pix_total_ch2_ch3.to_excel(filename_pix_total_ch2_ch3)