"""
Script to join the outputs of correlation calculations and saves the graphs

input: xlsx files outputed by correlation scripts
output: graphs for each xlsx

@author: Andre
"""
############################################################
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#############################################################

ch1_name = 'yH2AX'
ch2_name = 'BCLAF1'
ch3_name = 'PTK2'
ch4_name = 'DAPI'

#####################################################
ch1_ch2 = ch1_name + '-' + ch2_name
ch1_ch3 = ch1_name + '-' + ch3_name
ch1_ch4 = ch1_name + '-' + ch4_name
ch2_ch3 = ch2_name + '-' + ch3_name
ch2_ch4 = ch2_name + '-' + ch4_name
ch3_ch4 = ch3_name + '-' + ch4_name


#start dataframes############################
df_rcorr = pd.DataFrame([])
df_pix = pd.DataFrame([])
df_pix_flip = pd.DataFrame([])
df_int = pd.DataFrame([])
df_area = pd.DataFrame([])
array_n_cluster = np.array([])

#for each folder grabs the values of rcorr
for folder in os.listdir():
    
    if os.path.isdir(folder):
        os.chdir(folder)
        
        #pearson for integrated density
        xlsx_name = 'rcorr.xlsx'
        df  = pd.read_excel(xlsx_name)
        #df_rcorr = df_rcorr.append(df, ignore_index=True)
        df_rcorr = pd.concat([df_rcorr,df], ignore_index=True)
        
        #pearson pixel by pixel for each patch
        xlsx_name_pix = 'corr pixel.xlsx'
        df  = pd.read_excel(xlsx_name_pix)
        #df_pix = df_pix.append(df, ignore_index=True)
        df_pix = pd.concat([df_pix,df], ignore_index=True)
        
        
        #area and number of clusters 
        
        csv_name = 'cluster_area.csv'
        df = pd.read_csv(csv_name)
        df = df[:-1]
        n_cluster_cell = df.shape[0]
        array_n_cluster = np.append(array_n_cluster, n_cluster_cell)
        df_area = pd.concat([df_area, df], ignore_index=True)
        
    
        print(folder + " done")
        os.chdir('..')
    
#print number of cells and patches
n_cells = df_rcorr.shape[0]
n_clusters = df_pix.shape[0]
mean_area = df_area.Area.mean()
mean_area_sem = df_area.Area.sem()
mean_n_cluster = array_n_cluster.mean()
mean_n_cluster_sem = np.std(array_n_cluster, ddof=1) / np.sqrt(np.size(array_n_cluster))
print('Total cells: ' + str(n_cells))
print('Total clusters: ' + str(n_clusters))
print('Mean cluster area: ' + str(mean_area) + ' um^2')
print('Mean cluster area SEM: ' + str(mean_area_sem) + ' um^2')
print('Mean cluster number: ' + str(mean_n_cluster))
print('Mean cluster number SEM :' + str(mean_n_cluster_sem))



#transform rcorr dataframe into one column dataframe to catplot by seaborn
df_column = pd.DataFrame(df_rcorr[ch2_ch3])
df_column.columns = ['rcorr']
df_column["channels"] = ch2_ch3


df_intermed = pd.DataFrame(df_rcorr[ch1_ch3])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch1_ch3

df_column = pd.concat([df_column,df_intermed], ignore_index=True)

df_intermed = pd.DataFrame(df_rcorr[ch1_ch2])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch1_ch2

df_column = pd.concat([df_column, df_intermed], ignore_index=True)


      
sns.catplot(x='channels', y='rcorr', data=df_column, kind='swarm')
x_l = [-5,45]
y_l = [0,0]
plt.plot(x_l, y_l,'k:', alpha=0.4)
plt.yticks((-1,-0.5,0,0.5,1))
plt.ylabel('Correlation Coeficient (Integrated Density/cell)')
plt.xlabel('')

plt.tight_layout()    
plt.savefig('pearson-int-den-real.png', dpi=600)




###########################################################################
#plot histogram of pixel correlation

plt.figure()
sns.kdeplot(df_pix[ch2_ch3], label=ch2_ch3)
plt.xlabel('Histogram Pearson Pixel ')
plt.tight_layout()
#plt.savefig('pixel-corr-bclaf1-gamma.png', dpi=600)
#df = pd.DataFrame(df_pix['bclaf1_gamma'])
#df.to_excel('pixel-corr-bclaf1_gamma.xlsx')

sns.kdeplot(df_pix[ch1_ch3], label=ch1_ch3)
sns.kdeplot(df_pix[ch1_ch2], label=ch1_ch2)
plt.legend()
plt.savefig('pixel-corr.png', dpi=600)





