import pm4py
import pandas as pd
import numpy as np
from pm4py.visualization.dfg import visualizer as dfg_visualizer
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
import sys

log_name='151024'

try:
    Case = sys.argv[1]
    timelog=pd.read_hdf('Event_log/log_'+Case+'_'+log_name+'_ALL_df.h5')
    usuals=np.load('Source/Data/'+Case+'/masklayers/usuals.npy', allow_pickle=True)[0]
    keynames=list(usuals.keys())
    timelog=timelog[timelog['Crop'].isin(keynames)]
    title=Case
    title_s=title
except IndexError:
    #combining all cases
    logs = []
    crops=[]
    for Case in ['Idaho', 'NorthDakota', 'Colorado']:
        timelog=pd.read_hdf('Event_log/log_'+Case+'_'+log_name+'_ALL_df.h5')
        usuals=np.load('Source/Data/'+Case+'/masklayers/usuals.npy', allow_pickle=True)[0]
        keynames=list(usuals.keys())
        crops+=keynames
        logs.append(timelog[timelog['Crop'].isin(keynames)])
    timelog=pd.concat(logs)
    title='Idaho, NorthDakota, and Colorado'
    title_s='Idaho_NorthDakota_Colorado'


if __name__ == "__main__":
    dataframe = pm4py.format_dataframe(timelog, case_id='CaseID', activity_key='Activity', timestamp_key='Timestamp')
    log = pm4py.convert_to_event_log(dataframe)


image_path=[]
log_start = ['Early First Snow Previous','Usual First Snow Previous','Late First Snow Previous'
             ,'Early Last Snow','Usual Last Snow','Late Last Snow'
             ,'Early First Snow','Usual First Snow','Late First Snow']
counts=np.sum(list(pm4py.get_start_activities(log).values())) 

output_dir = 'Figure/dfg_com'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for event in log_start:
    if event[-8:]=='Previous':
        log_temp=pm4py.filter_start_activities(log, event)
    else:
        log_temp=pm4py.filter_event_attribute_values(log,'Activity',values=['Early First Snow Previous','Usual First Snow Previous','Late First Snow Previous']
                                        , level="event", retain=False)
        log_temp=pm4py.filter_event_attribute_values(log_temp,'Activity',values=event, level="case", retain=True)
    #counts if want relative frequency
    #counts=pm4py.get_start_activities(log_temp).get(event)
    counts=pm4py.get_event_attribute_values(log_temp, "concept:name").get(event)
    activity_counts = pm4py.get_event_attribute_values(log, "concept:name")
    count_dict={}
    for activity, act_count in activity_counts.items():
        count_dict[activity]=act_count#/counts
        #counts if want relative frequency


    dfg, start_activities, end_activities = pm4py.discover_dfg(log_temp)
    #dfg=dfg_discovery.apply(log_temp,activity_counts)
    dfg_percentage = {key: round((value / counts) * 100,2) for key, value in dfg.items()}
    parameters = {
        dfg_visualizer.Variants.FREQUENCY.value.Parameters.FORMAT: "pdf"
    }
    
    #pm4py.view_dfg(dfg_percentage, start_activities, end_activities)
    gviz = dfg_visualizer.apply(dfg_percentage)#, parameters=parameters)
    #if locator==1:
    gviz.attr(label=event, fontsize='20', labelloc='t')
    #save the graph as a png file
    path='Figure/dfg_com/'+Case+'_'+event
    path=path.replace(" ", "_")
    gviz.render(path, format='png')
    gviz.render(path, format='svg')
    image_path.append(path+'.png')

plt.figure(figsize=(20, 20))
for i,path in enumerate(image_path):
    img = mpimg.imread(path)
    plt.subplot(3, 3, i+1)
    
    plt.imshow(img)
    plt.axis('off')  # Hide axes
plt.suptitle(title,fontsize=20)
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Figure/'+title_s+'_DFG_byseason.pdf')
plt.show(block=False)
plt.pause(3)
plt.close('all')

plt.figure(figsize=(10, 8))
#for i,path in enumerate(image_path[3:6]):
img = mpimg.imread(image_path[3])
#plt.subplot(1, 3, i+1)

plt.imshow(img)
plt.axis('off') 
#plt.suptitle(title,fontsize=20)
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Figure/'+title_s+'_DFG_earlylastsnow.pdf')
plt.show(block=False)
plt.pause(3)
plt.close('all')

plt.figure(figsize=(10, 8))
img = mpimg.imread(image_path[4])

plt.imshow(img)
plt.axis('off')
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Figure/'+title_s+'_DFG_usuallastsnow.pdf')
plt.show(block=False)
plt.pause(3)
plt.close('all')

plt.figure(figsize=(10, 8))
img = mpimg.imread(image_path[5])

plt.imshow(img)
plt.axis('off')  
plt.tight_layout(rect=[0, 0.03, 1, 0.99])
plt.savefig('Figure/'+title_s+'_DFG_latelastsnow.pdf')
plt.show(block=False)
plt.pause(3)
plt.close('all')