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

ch1_name = 'yh2ax'
ch2_name = 'bclaf1'
ch3_name = 'fak'
ch4_name = 'dapi'

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

#for each folder grabs the values of rcorr
for folder in os.listdir():
    
    if os.path.isdir(folder):
        os.chdir(folder)
        
        #pearson for integrated density
        xlsx_name = "rcorr.xlsx"
        df  = pd.read_excel(xlsx_name)
        #df_rcorr = df_rcorr.append(df, ignore_index=True)
        df_rcorr = pd.concat([df_rcorr,df], ignore_index=True)
        
        #pearson pixel by pixel for each patch
        xlsx_name_pix = "corr pixel.xlsx"
        df  = pd.read_excel(xlsx_name_pix)
        #df_pix = df_pix.append(df, ignore_index=True)
        df_pix = pd.concat([df_pix,df], ignore_index=True)
    
        print(folder + " done")
        os.chdir('..')
    

#transform rcorr dataframe into one column dataframe to catplot by seaborn
df_column = pd.DataFrame(df_rcorr[ch1_ch2])
df_column.columns = ['rcorr']
df_column["channels"] = ch1_ch2


df_intermed = pd.DataFrame(df_rcorr[ch1_ch3])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch1_ch3

df_column = pd.concat([df_column,df_intermed], ignore_index=True)

df_intermed = pd.DataFrame(df_rcorr[ch2_ch3])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch2_ch3

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





