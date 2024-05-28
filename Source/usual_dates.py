import matplotlib.pyplot as plt
import pandas as pd


fig, ax = plt.subplots(nrows=3, ncols=3, figsize=(12,15))#, sharex=True)
#ax=ax.flatten()
for i,Case in enumerate(['Idaho','NorthDakota','Colorado']):
  timelog=pd.read_hdf('Event_log/log_'+Case+'_240524_max09_df.h5')
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


  timelog['Day_of_Year'] = timelog['Timestamp'].dt.dayofyear

  crops = ['Potatoes', 'Spring Wheat', 'Sugarbeets']
  usual = [potato_usual, springwheat_usual, sugarbeets_usual]

  for j, crop in enumerate(crops):
      crop_df = timelog[timelog['Multiple_crop']==0][timelog[timelog['Multiple_crop']==0]['Crop'] == crop]
      ax[i,j].boxplot([crop_df[crop_df['Activity'] == activity]['Day_of_Year'] for activity in ['Emergence', 'Maturity', 'Senescence', 'Dormancy']], labels=['Emergence', 'Maturity', 'Senescence', 'Dormancy'])
      ax[i,j].hlines(usual[j][0][::3], 0.5, 1.5, ls='--', lw=1.5, color='g', label='usual planting')
      ax[i,j].hlines(usual[j][0][1:3], 0.5, 1.5, ls='-', lw=1.5, color='g', label='usual planting (Most active)')
      ax[i,j].hlines(usual[j][1][::3], 3.5, 4.5, ls='--', lw=1.5, color='r', label='usual harvesting')
      ax[i,j].hlines(usual[j][1][1:3], 3.5, 4.5, ls='-', lw=1.5, color='r', label='usual harvesting (Most active)')
      if i==0:
           ax[i,j].set_title(f'{crop}',  fontsize=18)           
      if i==2:
        ax[i,j].tick_params(axis='x', labelsize=16)
        ax[i,j].set_xticklabels(ax[i,j].get_xticklabels(), rotation=45)
      else:
           ax[i,j].set_xticklabels([])
  ax[i,0].set_ylabel(Case+'\nDay of Year', fontsize=18)
  ax[-1,1].set_xlabel('Activity',  fontsize=18)

  ax[0,0].legend()
 

plt.suptitle('Validation with usual planting and harvesting dates',  fontsize=24)
plt.tight_layout(rect=[0, 0.075, 1, 0.97])
plt.savefig('Result/boxplot_3cropALL.pdf', format='pdf')
plt.show()
