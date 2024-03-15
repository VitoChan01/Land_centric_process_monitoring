import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import seed_to_harvest as sth

#Evaluate smoothing

def LMM_count(ts):
    local_maxima_indices = np.where((ts[:-2] < ts[1:-1]) & (ts[1:-1] > ts[2:]))[0] + 1
    local_minima_indices = np.where((ts[:-2] > ts[1:-1]) & (ts[1:-1] < ts[2:]))[0] + 1
    return len(local_maxima_indices)+len(local_minima_indices)

years = [f'{x}' for x in np.arange(2007,2023,1)]
num_LMM_org=[]
num_LMM_IIR=[]
num_LMM_SG=[]
num_LMM_WE=[]
for i in np.arange(0,148,1):
    #loading data
    sid=i
    ts=pd.read_hdf(f'Source/Data/sites/Site{sid:03}_NBARint.h5')
    ts=ts.interpolate(method='linear',axis=0)
    for yt in years:
        #smoothing
        IIR_smoothed = sth.IIRff(ts.loc[yt]['mean'], 3, 0.05)
        sg_smoothed = signal.savgol_filter(ts.loc[yt]['mean'], window_length=31, polyorder=2)
        we_smoothed = sth.WEfilter(ts.loc[yt]['mean'],3,1000)
        #LMM
        num_LMM_org.append(LMM_count(ts.loc[yt]['mean'].values))
        num_LMM_IIR.append(LMM_count(IIR_smoothed))
        num_LMM_SG.append(LMM_count(sg_smoothed))
        num_LMM_WE.append(LMM_count(we_smoothed))

data = [num_LMM_org, num_LMM_IIR, num_LMM_SG, num_LMM_WE]
labels = ['Unfiltered', 'BZP', 'SG', 'WE']

plt.figure(figsize=(12, 4))
plt.boxplot(data, labels=labels, vert=False)
plt.title('Number of Local Maxima and Minima', fontsize=24)
plt.ylabel('Smoothing Method', fontsize=18)
plt.xlabel('Frequency', fontsize=18)
plt.tick_params(axis='y', labelsize=16) 
plt.tight_layout()
plt.savefig('Result/LMM_boxplot.pdf')
plt.show()