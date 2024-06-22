import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys

try:
    smooth = sys.argv[1]
except IndexError:
    smooth = 'ALL'
fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(12,15))#, sharex=True)
#ax=ax.flatten()
for i,Case in enumerate(['Idaho','NorthDakota','Colorado']):
  print('Case:',Case, ' Smooth:',smooth)
  timelog=pd.read_hdf('Event_log/log_'+Case+'_310524_'+smooth+'_df.h5')
  #timelog=pd.read_hdf('Event_log/log_'+Case+'_240524_max09_df.h5')
  #timelog=pd.read_hdf('Event_log/log_148sites_240129_df.h5')

  #source usda field crops usual planting and harvesting --idaho
  #https://downloads.usda.library.cornell.edu/usda-esmis/files/vm40xr56k/dv13zw65p/w9505297d/planting-10-29-2010.pdf
  #potato_usual=[[pd.Timestamp(2009, 4, 6).dayofyear,pd.Timestamp(2009, 6, 9).dayofyear]
  #              ,[pd.Timestamp(2009, 8, 15).dayofyear,pd.Timestamp(2009, 10, 27).dayofyear]]

  #alfalfa_usual=[[0,0]
  #               ,[pd.Timestamp(2009, 5, 22).dayofyear,pd.Timestamp(2009, 10, 20).dayofyear]]

  #sugarbeets_usual=[[pd.Timestamp(2009, 3, 24).dayofyear,pd.Timestamp(2009, 5, 5).dayofyear]
  #                  ,[pd.Timestamp(2009, 9, 15).dayofyear,pd.Timestamp(2009, 11, 10).dayofyear]]

  #springwheat_usual=[[pd.Timestamp(2009, 3, 21).dayofyear,pd.Timestamp(2009, 5, 26).dayofyear]
  #                   ,[pd.Timestamp(2009, 8, 4).dayofyear,pd.Timestamp(2009, 9, 29).dayofyear]]

  #winterwheat_usual=[[pd.Timestamp(2008, 9, 8).dayofyear,pd.Timestamp(2008, 11, 3).dayofyear]
  #                   ,[pd.Timestamp(2009, 7, 23).dayofyear,pd.Timestamp(2009, 9, 14).dayofyear]]

  if Case=='Idaho':
    potato_usual=[[pd.Timestamp(2009, 4, 6).dayofyear,pd.Timestamp(2009, 4, 28).dayofyear
    ,pd.Timestamp(2009, 5, 19).dayofyear,pd.Timestamp(2009, 6, 9).dayofyear]
    ,[pd.Timestamp(2009, 8, 15).dayofyear,pd.Timestamp(2009, 9, 22).dayofyear
    ,pd.Timestamp(2009, 10, 13).dayofyear,pd.Timestamp(2009, 10, 27).dayofyear]]

    sugarbeets_usual=[[pd.Timestamp(2009, 3, 24).dayofyear,pd.Timestamp(2009, 4, 3).dayofyear
                        ,pd.Timestamp(2009, 4, 21).dayofyear,pd.Timestamp(2009, 5, 5).dayofyear]
                      ,[pd.Timestamp(2009, 9, 15).dayofyear,pd.Timestamp(2009, 10, 8).dayofyear
                        ,pd.Timestamp(2009, 10, 30).dayofyear,pd.Timestamp(2009, 11, 10).dayofyear]]

    springwheat_usual=[[pd.Timestamp(2009, 3, 21).dayofyear,pd.Timestamp(2009, 4, 7).dayofyear
                          ,pd.Timestamp(2009, 5, 3).dayofyear,pd.Timestamp(2009, 5, 26).dayofyear]
                          ,[pd.Timestamp(2009, 8, 4).dayofyear,pd.Timestamp(2009, 8, 13).dayofyear
                            ,pd.Timestamp(2009, 9, 8).dayofyear,pd.Timestamp(2009, 9, 29).dayofyear]]

    winterwheat_usual=[[pd.Timestamp(2008, 9, 8).dayofyear,pd.Timestamp(2008, 11, 3).dayofyear]
                      ,[pd.Timestamp(2009, 7, 23).dayofyear,pd.Timestamp(2009, 9, 14).dayofyear]]
    barley_usual=[]#not availabel in the USDA report
    dybean_usual=[]#not availabel in the USDA report
  elif Case=='Colorado':
                    #fall potato 55.2k acres
                    potato_usual=[[pd.Timestamp(2009, 5, 2).dayofyear,pd.Timestamp(2009, 5, 6).dayofyear
                    ,pd.Timestamp(2009, 5, 25).dayofyear,pd.Timestamp(2009, 5, 31).dayofyear]
                    ,[pd.Timestamp(2009, 9, 6).dayofyear,pd.Timestamp(2009, 9, 15).dayofyear
                    ,pd.Timestamp(2009, 10, 11).dayofyear,pd.Timestamp(2009, 10, 17).dayofyear]]
      
      #summer potato 3.9k acres
                    potato_summer_usual=[[pd.Timestamp(2009, 4, 8).dayofyear,pd.Timestamp(2009, 4, 14).dayofyear
                    ,pd.Timestamp(2009, 5, 18).dayofyear,pd.Timestamp(2009, 5, 27).dayofyear]
                    ,[pd.Timestamp(2009, 8, 6).dayofyear,pd.Timestamp(2009, 8, 17).dayofyear
                    ,pd.Timestamp(2009, 9, 25).dayofyear,pd.Timestamp(2009, 10, 4).dayofyear]]

                    sugarbeets_usual=[[pd.Timestamp(2009, 3, 30).dayofyear,pd.Timestamp(2009, 4, 7).dayofyear
                    ,pd.Timestamp(2009, 4, 30).dayofyear,pd.Timestamp(2009, 5, 10).dayofyear]
                    ,[pd.Timestamp(2009, 9, 30).dayofyear,pd.Timestamp(2009, 10, 10).dayofyear
                    ,pd.Timestamp(2009, 11, 4).dayofyear,pd.Timestamp(2009, 11, 12).dayofyear]]

                    springwheat_usual=[[pd.Timestamp(2009, 3, 28).dayofyear,pd.Timestamp(2009, 4, 9).dayofyear
                    ,pd.Timestamp(2009, 5, 16).dayofyear,pd.Timestamp(2009, 5, 23).dayofyear]
                    ,[pd.Timestamp(2009, 7, 23).dayofyear,pd.Timestamp(2009, 8, 3).dayofyear
                    ,pd.Timestamp(2009, 9, 17).dayofyear,pd.Timestamp(2009, 9, 29).dayofyear]]

                    winterwheat_usual=[[pd.Timestamp(2008, 9, 1).dayofyear,pd.Timestamp(2008, 9, 11).dayofyear
                    ,pd.Timestamp(2008, 10, 2).dayofyear,pd.Timestamp(2008, 10, 11).dayofyear]
                    ,[pd.Timestamp(2009, 6, 27).dayofyear,pd.Timestamp(2009, 7, 2).dayofyear
                    ,pd.Timestamp(2009, 7, 21).dayofyear,pd.Timestamp(2009, 7, 29).dayofyear]] 
                    barley_usual=[[pd.Timestamp(2009, 3, 14).dayofyear,pd.Timestamp(2009, 5, 16).dayofyear]
                            ,[pd.Timestamp(2009, 7, 20).dayofyear,pd.Timestamp(2009, 9, 14).dayofyear]]
                    dybean_usual=[[pd.Timestamp(2009, 5, 20).dayofyear,pd.Timestamp(2009, 6, 25).dayofyear]
                            ,[pd.Timestamp(2009, 9, 4).dayofyear,pd.Timestamp(2009, 10, 20).dayofyear]]
  elif Case=='NorthDakota':
      potato_usual=[[pd.Timestamp(2009, 4, 28).dayofyear,pd.Timestamp(2009, 5, 5).dayofyear
                    ,pd.Timestamp(2009, 5, 30).dayofyear,pd.Timestamp(2009, 6, 6).dayofyear]
                    ,[pd.Timestamp(2009, 9, 2).dayofyear,pd.Timestamp(2009, 9, 10).dayofyear
                    ,pd.Timestamp(2009, 10, 7).dayofyear,pd.Timestamp(2009, 10, 16).dayofyear]]

      sugarbeets_usual=[[pd.Timestamp(2009, 4, 19).dayofyear,pd.Timestamp(2009, 4, 24).dayofyear
                      ,pd.Timestamp(2009, 5, 18).dayofyear,pd.Timestamp(2009, 5, 26).dayofyear]
                      ,[pd.Timestamp(2009, 9, 17).dayofyear,pd.Timestamp(2009, 9, 30).dayofyear
                      ,pd.Timestamp(2009, 10, 17).dayofyear,pd.Timestamp(2009, 10, 25).dayofyear]]

      springwheat_usual=[[pd.Timestamp(2009, 4, 16).dayofyear,pd.Timestamp(2009, 4, 24).dayofyear
                      ,pd.Timestamp(2009, 5, 25).dayofyear,pd.Timestamp(2009, 6, 3).dayofyear]
                      ,[pd.Timestamp(2009, 8, 1).dayofyear,pd.Timestamp(2009, 8, 8).dayofyear
                      ,pd.Timestamp(2009, 9, 13).dayofyear,pd.Timestamp(2009, 9, 25).dayofyear]]

      winterwheat_usual=[[pd.Timestamp(2008, 9, 6).dayofyear,pd.Timestamp(2008, 9, 10).dayofyear
                      ,pd.Timestamp(2008, 9, 25).dayofyear,pd.Timestamp(2008, 10, 2).dayofyear]
                      ,[pd.Timestamp(2009, 7, 15).dayofyear,pd.Timestamp(2009, 7, 20).dayofyear
                      ,pd.Timestamp(2009, 7, 29).dayofyear,pd.Timestamp(2009, 8, 10).dayofyear]] 
      barley_usual=[]#not availabel in the USDA report
      dybean_usual=[[pd.Timestamp(2009, 5, 14).dayofyear,pd.Timestamp(2009, 6, 13).dayofyear]
                          ,[pd.Timestamp(2009, 8, 30).dayofyear,pd.Timestamp(2009, 10, 26).dayofyear]]


  timelog['Day_of_Year'] = timelog['Timestamp'].dt.dayofyear

  crops = ['Potatoes', 'Spring Wheat', 'Sugarbeets']
  usual = [potato_usual, springwheat_usual, sugarbeets_usual]
  act=['Emergence', 'Maturity', 'Senescence', 'Dormancy']

  for j, crop in enumerate(crops):
      crop_df = timelog[timelog['Multiple_crop']==0][timelog[timelog['Multiple_crop']==0]['Crop'] == crop]
      if (i<2 or j<2):
        ax[i,j].boxplot([crop_df[crop_df['Activity'] == activity]['Day_of_Year'] for activity in ['Emergence', 'Maturity', 'Senescence', 'Dormancy']], labels=['Emergence', 'Maturity', 'Senescence', 'Dormancy'])
        hline_usual_planting =ax[i,j].hlines(usual[j][0][::3], 0.5, 1.5, ls='--', lw=1.5, color='g', label='usual planting')
        #ax[i,j].hlines(usual[j][0][1:3], 0.5, 1.5, ls='-', lw=1.5, color='g', label='usual planting (Most active)')
        hline_usual_harvesting =ax[i,j].hlines(usual[j][1][::3], 3.5, 4.5, ls='--', lw=1.5, color='r', label='usual harvesting')
        #ax[i,j].hlines(usual[j][1][1:3], 3.5, 4.5, ls='-', lw=1.5, color='r', label='usual harvesting (Most active)')
      if i==0:
          ax[i,j].set_title(f'{crop}',  fontsize=18)           
      if i==2:
        ax[i,j].tick_params(axis='x', labelsize=16)
        ax[i,j].set_xticks(range(1,5))
        ax[i,j].set_xticklabels(act, rotation=45)
      else:
          ax[i,j].set_xticklabels([])
  ax[i,0].set_ylabel(Case+'\nDay of Year', fontsize=18)
  ax[-1,1].set_xlabel('Activity',  fontsize=18)

  ax[1,2].tick_params(axis='x', labelsize=16)
  ax[1,2].set_xticks(range(1,5))
  ax[1,2].set_xticklabels(act, rotation=45)
  ax[2,2].axis('off')
  ax[2,2].legend([hline_usual_planting, hline_usual_harvesting]
                 , ['Usual Planting', 'Usual Harvesting'], loc='center', fontsize='large')
  
  crops = ['Barley','Dry Beans','Potatoes', 'Spring Wheat', 'Sugarbeets']
  usual = [barley_usual,dybean_usual, potato_usual, springwheat_usual, sugarbeets_usual]
  act=['Emergence', 'Dormancy']
  early_dor_agg=0
  late_dor_agg=0
  usual_dor_agg=0
  early_emg_agg=0
  late_emg_agg=0
  usual_emg_agg=0

  for j, crop in enumerate(crops):
      try:
          print(crop)
          crop_df = timelog[timelog['Multiple_crop']==0][timelog[timelog['Multiple_crop']==0]['Crop'] == crop]
          usual_planting=usual[j][0]#[::3]
          usual_harvesting=usual[j][1]#[::3]
          early_emg=np.sum(crop_df[crop_df['Activity']=='Emergence']['Day_of_Year']<usual_planting[0])
          late_emg=np.sum(crop_df[crop_df['Activity']=='Emergence']['Day_of_Year']>usual_planting[-1])
          usual_emg=len(crop_df[crop_df['Activity']=='Emergence'])-late_emg-early_emg

          print('Late Emergence:',late_emg)
          print('Usual Emergence:',usual_emg)
          print('Early Emergence:',early_emg,'\n')

          early_dor=np.sum(crop_df[crop_df['Activity']=='Dormancy']['Day_of_Year']<usual_harvesting[0])
          late_dor=np.sum(crop_df[crop_df['Activity']=='Dormancy']['Day_of_Year']>usual_harvesting[-1])
          usual_dor=len(crop_df[crop_df['Activity']=='Dormancy'])-late_dor-early_dor

          
          print('Late Dormancy:',late_dor)
          print('Usual Dormancy:',usual_dor)
          print('Early Dormancy:',early_dor,'\n')

          early_dor_agg+=early_dor
          late_dor_agg+=late_dor
          usual_dor_agg+=usual_dor
          early_emg_agg+=early_emg
          late_emg_agg+=late_emg
          usual_emg_agg+=usual_emg

      except:
          print('Nothing\n')
          continue
  print('All Late Emergence:',late_emg_agg)
  print('All Usual Emergence:',usual_emg_agg)
  print('All Early Emergence:',early_emg_agg,'\n')
  print('All Late Dormancy:',late_dor_agg)
  print('All Usual Dormancy:',usual_dor_agg)
  print('All Early Dormancy:',early_dor_agg,'\n')


plt.suptitle('Validation with usual planting and harvesting dates',  fontsize=24)
plt.tight_layout(rect=[0, 0.1, 1, 0.97])
plt.savefig('Result/boxplot_3crop'+smooth+'.pdf', format='pdf')
plt.show()
