import pandas as pd
import numpy as np
for i,Case in enumerate(['Idaho','NorthDakota','Colorado']):
  print('Case:',Case)
  for smooth in ['ALL','None', 'BZP','SG','WE']:
    print('Case:',Case,' Smooth:',smooth)
    timelog=pd.read_hdf('Event_log/log_'+Case+'_310524_'+smooth+'_df.h5')
    timelog=timelog[timelog['Multiple_crop']==0]
    #timelog=pd.read_hdf('Event_log/log_'+Case+'_240524_max09_df.h5')

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
      total_case=2220
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
                      total_case=2370
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
        total_case=3000

    timelog['Day_of_Year'] = timelog['Timestamp'].dt.dayofyear
    crops = ['Barley','Dry Beans','Potatoes', 'Spring Wheat', 'Sugarbeets']
    usual = [barley_usual,dybean_usual, potato_usual, springwheat_usual, sugarbeets_usual]
    act=['Emergence', 'Dormancy']

    usual_dor_agg=[]
    usual_emg_agg=[]

    for j, crop in enumerate(crops):
      try:
          crop_df = timelog[timelog['Crop'] == crop]
          usual_planting=usual[j][0]#[::3]
          usual_harvesting=usual[j][1]#[::3]
          early_emg=np.sum(crop_df[crop_df['Activity']=='Emergence']['Day_of_Year']<usual_planting[0])
          late_emg=np.sum(crop_df[crop_df['Activity']=='Emergence']['Day_of_Year']>usual_planting[-1])
          usual_emg=len(crop_df[crop_df['Activity']=='Emergence'])-late_emg-early_emg

          early_dor=np.sum(crop_df[crop_df['Activity']=='Dormancy']['Day_of_Year']<usual_harvesting[0])
          late_dor=np.sum(crop_df[crop_df['Activity']=='Dormancy']['Day_of_Year']>usual_harvesting[-1])
          usual_dor=len(crop_df[crop_df['Activity']=='Dormancy'])-late_dor-early_dor
          #print(Case+' '+crop)
          #print(usual_dor)
          #print(usual_emg,'\n')
          usual_dor_agg.append(usual_dor)
          usual_emg_agg.append(usual_emg)

      except:
          #print('Nothing\n')
          continue

    print('All Usual Emergence:',np.sum(usual_emg_agg),f' ({np.sum(usual_emg_agg)*100/total_case}%)')
    print('All Usual Dormancy:',np.sum(usual_dor_agg),f' ({np.sum(usual_dor_agg)*100/total_case}%)','\n')
