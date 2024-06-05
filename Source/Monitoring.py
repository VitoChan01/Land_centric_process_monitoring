import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches

cmdin = sys.argv[1]
if cmdin=='ID':
    Case='Idaho'
elif cmdin=='CO':
  Case='Colorado'
elif cmdin=='ND':
  Case='NorthDakota'
else:
  Case='All'

try:
    yt = sys.argv[2]
except IndexError:
    yt = 2022

try:
    crop = sys.argv[3]
except IndexError:
    crop = None

try:
    filtering = sys.argv[4]
except IndexError:
    filtering = None

try:
    width = float(sys.argv[5])
except IndexError:
    width = 1.5

def allpreprocess(timelog,crop=None, filtering=None, width=1.5):
    '''
    Create doy column
    if crop is true subset cases by crop, 
    if filtering is true remove multiple crop cases, filter outlier cases by width*IQR and remove incomplete cases
    '''
    timelog['DayOfYear'] = timelog['Timestamp'].dt.dayofyear
    
    #subset crop
    if crop:
        timelog=timelog[timelog['Crop'] == crop]
    if filtering:
        def filterdf(df, width):
            q_1 = df['DayOfYear'].quantile(0.25)
            q_3  = df['DayOfYear'].quantile(0.75)
            q_low = q_1 - width*(q_3-q_1)
            q_hi  = q_3 + width*(q_3-q_1)

            df_filtered = df[(df['DayOfYear'] < q_hi) & (df['DayOfYear'] > q_low)]
            return df_filtered 
        #Remove multiple crop cases
        timelog=timelog[timelog['Multiple_crop'] == 0]
        filter_temp=[]
        for i,e in enumerate(['Emergence','Maturity','Senescence','Dormancy']):
            temp_df=timelog[timelog['Activity'] == e].copy()
            temp_df=filterdf(temp_df, width)
            filter_temp.append(temp_df)
        filtered_timelog=pd.concat(filter_temp)
        ucid,counts=np.unique(filtered_timelog['CaseID'], return_counts=True)
        filter_case=[counts[np.where(ucid==cid)[0][0]] for cid in filtered_timelog['CaseID']]
        filtered_timelog['filter_case']=filter_case
        filtered_timelog=filtered_timelog[filtered_timelog['filter_case'] == 4]
        double_id=[]
        for e in ['Emergence','Maturity','Senescence','Dormancy']:
            artifact_idx=np.where(np.unique(filtered_timelog[filtered_timelog['Activity'] == e]['CaseID'], return_counts=True)[1]>1)[0]
            for j in artifact_idx:
                double_id.append(np.unique(filtered_timelog[filtered_timelog['Activity'] == e]['CaseID'])[j])
        for id in double_id:
            filtered_timelog=filtered_timelog[filtered_timelog['CaseID'] != id]
        return filtered_timelog
    else:
        return timelog
    
#Load the data
if Case=='All':
    timelog1=pd.read_hdf('Event_log/log_NorthDakota_310524_ALL_df.h5')
    timelog2=pd.read_hdf('Event_log/log_Colorado_310524_ALL_df.h5')
    timelog3=pd.read_hdf('Event_log/log_Idaho_310524_ALL_df.h5')
    
    timelog1=allpreprocess(timelog1, crop, filtering, width)
    timelog2=allpreprocess(timelog2, crop, filtering, width)
    timelog3=allpreprocess(timelog3, crop, filtering, width)
    
    timelog=pd.concat([timelog1,timelog2,timelog3])

    num_sites=0
    for CaseI in ['NorthDakota','Colorado','Idaho']:
        sites_pth = 'Source/Data/'+CaseI+'/sites/'
        site_names = os.listdir(sites_pth)
        num_sites+=len(site_names)

else:
    sites_pth = 'Source/Data/'+Case+'/sites/'
    site_names = os.listdir(sites_pth)
    num_sites=len(site_names)

    timelog=pd.read_hdf('Event_log/log_'+Case+'_310524_ALL_df.h5')
    timelog=allpreprocess(timelog, crop, filtering, width)

timelog['year']=timelog['CaseID'].apply(lambda x: x[-4:])
timelog=timelog[timelog['year']==str(yt)]
emg_timelog=timelog[(timelog['Activity'] == 'Emergence')]
mat_timelog=timelog[(timelog['Activity'] == 'Maturity')]
sen_timelog=timelog[(timelog['Activity'] == 'Senescence')]
dor_timelog=timelog[(timelog['Activity'] == 'Dormancy')]
#getting number of site at each stage at each day. 0: no crop, 1: emergence, 2: maturity, 3: senescence, 4: dormancy
progress_array = np.zeros((5,365))
progress_array[0]+=num_sites

for i in range(365):
    #get the new stage of the day
    new_emg=len(emg_timelog[(emg_timelog['DayOfYear'] == i)])
    new_mat=len(mat_timelog[(mat_timelog['DayOfYear'] == i)])
    new_sen=len(sen_timelog[(sen_timelog['DayOfYear'] == i)])
    new_dor=len(dor_timelog[(dor_timelog['DayOfYear'] == i)])
    #update the progress array
    progress_array[0][i]=progress_array[0][i-1]-new_emg
    progress_array[1][i]=progress_array[1][i-1]+new_emg-new_mat
    progress_array[2][i]=progress_array[2][i-1]+new_mat-new_sen
    progress_array[3][i]=progress_array[3][i-1]+new_sen-new_dor
    progress_array[4][i]=progress_array[4][i-1]+new_dor

plot_array = np.zeros((num_sites,365))
for i in range(365):
    marker=int(progress_array[0][i])
    plot_array[:marker,i]=1
    plot_array[marker:marker+int(progress_array[1][i]),i]=2
    marker+=int(progress_array[1][i])
    plot_array[marker:marker+int(progress_array[2][i]),i]=3
    marker+=int(progress_array[2][i])
    plot_array[marker:marker+int(progress_array[3][i]),i]=4
    marker+=int(progress_array[3][i])
    plot_array[marker:marker+int(progress_array[4][i]),i]=5

cmap = ListedColormap(['steelblue', 'green', 'yellow', 'orange', 'red'])
bounds = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
norm = BoundaryNorm(bounds, cmap.N)

plt.imshow(plot_array, cmap=cmap, norm=norm, origin='upper',alpha=0.6)
plt.xlabel('Day of year')
plt.ylabel('Number of site')

colors = ['steelblue', 'green', 'yellow', 'orange', 'red']
labels = ['None', 'Emergence', 'Maturity', 'Senescence', 'Dormancy']
patches = [mpatches.Patch(color=color, alpha=0.6, label=label) for color, label in zip(colors, labels)]


plt.legend(handles=patches, fontsize='large', loc='center left', bbox_to_anchor=(1, 0.5))
plt.title(Case+f' {yt}\nCrop: {crop}, filtering: {filtering}')
plt.savefig('Result\Monit_sim.pdf') 
plt.show()