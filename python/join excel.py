"""
Script to join the outputs of rcorr calc.py and correl pixel.py and saves the graphs

input: xlsx files outputed by rho calc.py (rcorr-*, int-den-*) and correl pixel.py (corr pixel*)
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
ch2_name = 'myo5c'
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
        df_rcorr = df_rcorr.append(df, ignore_index=True)
        
        #pearson pixel by pixel for each patch
        xlsx_name_pix = "corr pixel.xlsx"
        df  = pd.read_excel(xlsx_name_pix)
        df_pix = df_pix.append(df, ignore_index=True)
        
        
        #pearson pixel by pixel for each patch FLIPPED
        # xlsx_name_pix = "corr pixel flipped.xlsx"
        # df  = pd.read_excel(xlsx_name_pix)
        # df_pix_flip = df_pix_flip.append(df, ignore_index=True)
        
        #integrated density for each channel of each patch
        # xlsx_name_int_den = "int-den.xlsx"
        # df = pd.read_excel(xlsx_name_int_den)
        # df['bclaf1'] = df['bclaf1'].div(df['bclaf1'].max())
        # df['gamma'] = df['gamma'].div(df['gamma'].max())
        # df['dapi'] = df['dapi'].div(df['dapi'].max())
        # df_int = df_int.append(df, ignore_index=True)
    
        
        print(folder + " done")
        os.chdir('..')
    

#transform rcorr dataframe into one column dataframe to catplot by seaborn
df_column = pd.DataFrame(df_rcorr[ch1_ch2])
df_column.columns = ['rcorr']
df_column["channels"] = ch1_ch2


df_intermed = pd.DataFrame(df_rcorr[ch1_ch3])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch1_ch3

df_column = df_column.append(df_intermed, ignore_index=True)

df_intermed = pd.DataFrame(df_rcorr[ch2_ch3])
df_intermed.columns = ['rcorr']
df_intermed["channels"] = ch2_ch3

df_column = df_column.append(df_intermed, ignore_index=True)


      
sns.catplot(x='channels', y='rcorr', data=df_column, kind='swarm')
x_l = [-5,45]
y_l = [0,0]
plt.plot(x_l, y_l,'k:', alpha=0.4)
plt.yticks((-1,-0.5,0,0.5,1))
plt.ylabel('Correlation Coeficient (Integrated Density/cell)')
plt.xlabel('')

plt.tight_layout()    
plt.savefig('pearson-int-den-real.png', dpi=600)

# df_total.to_excel('rcorr_total.xlsx')


#plot rcorr integrated den and mean error
# plt.figure()  
# x = np.arange(5,df_rcorr.shape[0]+5)
# plt.scatter(x, df_rcorr['bclaf1_gamma'])

# k = np.arange(20,df_rcorr.shape[0]+20)
# plt.scatter(k, df_rcorr['bclaf1_dapi'])

# z = np.arange(35,df_rcorr.shape[0]+35)
# plt.scatter(z, df_rcorr['gamma_dapi'])

# plt.gca().spines['top'].set_visible(False)
# plt.gca().spines['right'].set_visible(False)
# #plt.gca().spines['bottom'].set_position('zero')

# x_3 = [x[3], k[3], z[3]]
# y_3 = [0.5, 0.5, 0.5]
# x_l = [0,45]
# y_l = [0,0]
# plt.plot(x_l, y_l,'k:', alpha=0.4)

# plt.xlim(0,45)
# plt.ylim(-0.5,1.0)
# plt.ylabel('Correlation Coeficient (Integrated Density/cell)')
# plt.xticks((x[3], k[3], z[3]), ('bclaf1_gamma', 'bclaf1_dapi', 'gamma_dapi'))
# plt.yticks((-0.5,0,0.5,1))

# plt.errorbar(x[3], 0.5, yerr=0.1, capsize=20,)

# plt.tight_layout()


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



#plt.figure()
#sns.kdeplot(df_pix_flip['bclaf1_gamma'])
#plt.xlabel('Histogram Pearson Pixel bclaf1_gamma flipped')
#plt.xlim(-1,1)
#plt.tight_layout()
#plt.savefig('FLIPPED-pixel-corr-bclaf1-gamma.png', dpi=600)
#df = pd.DataFrame(df_pix_flip['bclaf1_gamma'])
#df.to_excel('FLIPPED-pixel-corr-bclaf1_gamma.xlsx')

#plt.figure()
#sns.kdeplot(df_pix['bclaf1_fak'])
#plt.xlabel('Histogram Pearson Pixel bclaf1_fak')
#plt.xlim(-1,1)
#plt.tight_layout()
#plt.savefig('pixel-corr-bclaf1-dapi.png', dpi=600)
#df = pd.DataFrame(df_pix['bclaf1_fak'])
#df.to_excel('pixel-corr-bclaf1_dapi.xlsx')

# plt.figure()
# sns.kdeplot(df_pix_flip['bclaf1_dapi'])
# plt.xlabel('Histogram Pearson Pixel bclaf1_dapi flipped')
# plt.xlim(-1,1)
# plt.tight_layout()
# plt.savefig('FLIPPED-pixel-corr-bclaf1-dapi.png', dpi=600)
# df = pd.DataFrame(df_pix_flip['bclaf1_dapi'])
# df.to_excel('FLIPPED-pixel-corr-bclaf1_dapi.xlsx')

#plt.figure()
#sns.kdeplot(df_pix['gamma_fak'])
#plt.xlabel('Histogram Pearson Pixel gamma_fak')
#plt.xlim(-1,1)
#plt.tight_layout()
#plt.savefig('pixel-corr-gamma-dapi.png', dpi=600)
#df = pd.DataFrame(df_pix['gamma_fak'])
#df.to_excel('pixel-corr-gamma_dapi.xlsx')

# plt.figure()
# sns.kdeplot(df_pix_flip['gamma_dapi'])
# plt.xlabel('Histogram Pearson Pixel gamma_dapi flipped')
# plt.xlim(-1,1)
# plt.tight_layout()
# plt.savefig('FLIPPED-pixel-corr-gamma-dapi.png', dpi=600)
# df = pd.DataFrame(df_pix_flip['gamma_dapi'])
# df.to_excel('FLIPPED-pixel-corr-gamma_dapi.xlsx')

# #plot the histogram of integrated density
# plt.figure()
# sns.kdeplot(df_int['gamma'])
# plt.xlabel('Integrated Density gamma')
# #plt.xlim(0,1)
# plt.tight_layout()
# plt.savefig('int-dent-bclaf1-gamma.png', dpi=600)
# df = pd.DataFrame(df_int['gamma'])
# df.to_excel('int-den-gamma.xlsx')




# plt.figure()
# sns.kdeplot(df_int['dapi'])
# plt.xlabel('Integrated Density dapi')
# #plt.xlim(0,1)
# plt.tight_layout()
# plt.savefig('int-dent-bclaf1-dapi.png', dpi=600)
# df = pd.DataFrame(df_int['dapi'])
# df.to_excel('int-den-dapi.xlsx')


# plt.figure()
# sns.kdeplot(df_int['bclaf1'])
# plt.xlabel('Integrated Density bclaf1')
# #plt.xlim(0,1)
# plt.tight_layout()
# plt.savefig('int-dent-bclaf1-bclaf1.png', dpi=600)
# df = pd.DataFrame(df_int['bclaf1'])
# df.to_excel('int-den-bclaf1.xlsx')


