import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pm4py
import pickle
import itertools
import seed_to_harvest as sth
import os
import sys

#Dir path
cmdin = sys.argv[1]
if cmdin=='ID':
    Case='Idaho'
elif cmdin=='CO':
  Case='Colorado'
elif cmdin=='ND':
  Case='NorthDakota'

start_year=2008
try:
    smooth = sys.argv[2]
    output_name='log_'+Case+'_310524_'+smooth
except IndexError:
    smooth = 'ALL'
    output_name='log_'+Case+'_310524_'+smooth

print(f"Case: {Case}, Output name: {output_name}, Start year: {start_year}, Smooth: {smooth}")

sites_pth = 'Source/Data/'+Case+'/sites/'
cdl_pth = 'Source/Data/'+Case+'/cdl/'
season_pth = 'Source/Data/'+Case+'/season/'


output_hdf_pth = 'Event_log/'+output_name+'_df.h5'
output_xes_pth = 'Event_log/'+output_name+'.xes'

site_names = os.listdir(sites_pth)
cdl_names = os.listdir(cdl_pth)
season_names = os.listdir(season_pth)
num_sites=len(site_names)

loglist=[]
warningslist=[]
faillist=[]
#load location list
location=np.load('Source/Data/'+Case+'/masklayers/wgscenterlist.npy')
for i in np.arange(0,num_sites,1):
    #loading data
    sid=i
    ts=pd.read_hdf(sites_pth+f'/Site{sid:03}_NBARint.h5')
    cdl=pd.read_hdf(cdl_pth+f'/Site{sid:03}_cdl.h5')
    season=pd.read_hdf(season_pth+f'/Site{sid:03}_season_day.h5')
    loc=location[i]

    try:
        timelog, warnings = sth.eventtime_MACD(ts, season, cdl, sid, loc, start_year=start_year, smooth=smooth)
        loglist.append(timelog)
        warningslist.append(warnings)
    except Exception as e:
        print(f"Error encountered for site {sid}: {e}")
        faillist.append(sid)
timelog=pd.concat(loglist, axis=0, join='inner', ignore_index=True)

#cleaning according to CDL
def warn_mark(i,n):
    return f"{i:04}_{n+start_year}"
def warn_site_years(Lst):
    threshold=np.nonzero(np.array(Lst[1])<0.75)[0]
    return list(map(lambda x: warn_mark(Lst[0], x), threshold))

with open(cdl_pth+"ConsistencyPerc", "rb") as fp:   # Unpickling
    site_consistencyL = pickle.load(fp)

CaseID_anom=list(map(warn_site_years, enumerate(site_consistencyL)))

flat_CaseID_anom = list(itertools.chain.from_iterable(CaseID_anom))

timelog['Multiple_crop'] = 0

timelog.loc[timelog['CaseID'].isin(flat_CaseID_anom), 'Multiple_crop'] = 1

#report results
print('number of all detected rotation: ',timelog.shape[0]/4)
print('number of rotation failed: ',(15)*num_sites-timelog.shape[0]/4)
print('number of rotation with multiple crops on field: ',timelog[timelog['Multiple_crop'] != 0].shape[0]/4)
print('number of rotation with single crop on field: ',timelog[timelog['Multiple_crop'] == 0].shape[0]/4)
print('number of cases with multiple crops on field: ',len(flat_CaseID_anom))

#save the event log
timelog.to_hdf(output_hdf_pth, key='df', mode='w') 
if __name__ == "__main__":
    dataframe = pm4py.format_dataframe(timelog, case_id='CaseID', activity_key='Activity', timestamp_key='Timestamp')
    event_log = pm4py.convert_to_event_log(dataframe)
    pm4py.write_xes(event_log, output_xes_pth)
print('Event log saved to ',output_hdf_pth)

