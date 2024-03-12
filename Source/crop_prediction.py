import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pm4py
import rotation_prediction as rp
#Dir path
cdl_pth = 'Source/Data/cdl'


crop_id=[ '','Corn','Cotton','Rice','Sorghum','Soybeans','Sunflower','','','','Peanuts','Tobacco','Sweet Corn','Pop or Orn Corn','Mint','','','','','','','Barley','Durum Wheat','Spring Wheat','Winter Wheat','Other Small Grains','Dbl Crop WinWht/Soybeans','Rye','Oats','Millet','Speltz','Canola','Flaxseed','Safflower','Rape Seed','Mustard','Alfalfa','Other Hay/Non Alfalfa','Camelina','Buckwheat','','Sugarbeets','Dry Beans','Potatoes','Other Crops','Sugarcane','Sweet Potatoes','Misc Vegs & Fruits','Watermelons','Onions','Cucumbers','Chick Peas','Lentils','Peas','Tomatoes','Caneberries','Hops','Herbs','Clover/Wildflowers','Sod/Grass Seed','Switchgrass','Fallow/Idle Cropland','Pasture/Grass','Forest','Shrubland','Barren','Cherries','Peaches','Apples','Grapes','Christmas Trees','Other Tree Crops','Citrus','Pecans','Almonds','Walnuts','Pears','','','','Clouds/No Data','Developed','Water','','','','Wetlands','Nonag/Undefined','','','','Aquaculture','','','','','','','','','','','','','','','','','','','Open Water','Perennial Ice/Snow','','','','','','','','','Developed/Open Space','Developed/Low Intensity','Developed/Med Intensity','Developed/High Intensity','','','','','','','Barren','','','','','','','','','','Deciduous Forest','Evergreen Forest','Mixed Forest','','','','','','','','','Shrubland','','','','','','','','','','','','','','','','','','','','','','','','Grassland/Pasture','','','','','','','','','','','','','','Woody Wetlands','','','','','Herbaceous Wetlands','','','','','','','','','Pistachios','Triticale','Carrots','Asparagus','Garlic','Cantaloupes','Prunes','Olives','Oranges','Honeydew Melons','Broccoli','Avocados','Peppers','Pomegranates','Nectarines','Greens','Plums','Strawberries','Squash','Apricots','Vetch','Dbl Crop WinWht/Corn','Dbl Crop Oats/Corn','Lettuce','Dbl Crop Triticale/Corn','Pumpkins','Dbl Crop Lettuce/Durum Wht','Dbl Crop Lettuce/Cantaloupe','Dbl Crop Lettuce/Cotton','Dbl Crop Lettuce/Barley','Dbl Crop Durum Wht/Sorghum','Dbl Crop Barley/Sorghum','Dbl Crop WinWht/Sorghum','Dbl Crop Barley/Corn','Dbl Crop WinWht/Cotton','Dbl Crop Soybeans/Cotton','Dbl Crop Soybeans/Oats','Dbl Crop Corn/Soybeans','Blueberries','Cabbage','Cauliflower','Celery','Radishes','Turnips','Eggplants','Gourds','Cranberries','','','','Dbl Crop Barley/Soybeans']

cdllist=[]
for i in np.arange(0,148,1):
    Lt=pd.read_hdf(cdl_pth+f'/Site{i:03}_cdl.h5').drop([2005,2006], axis=0)
    Lt['crop'] = Lt['crop'].apply(lambda x: round(x))
    cdllist.append(Lt)

log = rp.rotation_prediction_preprocess(cdllist, L=7, W=5, val_year=2)

dfg, start_activities, end_activities = pm4py.discover_dfg(log)
log2 = pm4py.filter_event_attribute_values(log, 'concept:name', '', "event",False)
dfg, start_activities, end_activities = pm4py.discover_dfg(log2)
pm4py.view_dfg(dfg, start_activities, end_activities)

#save dfg
pm4py.save_vis_dfg(dfg, start_activities, end_activities, 'Result/dfg.pdf')

#estimate transition matrix
TM = rp.dfg_to_transition_matrix(log)
np.save('Event_log/transition_matrix.npy', TM)
#Assessment
for Pi, Ei in [[-2,-1],[-3,-2]]:#predicting the final 2 years
    prediction=rp.prediction(cdllist, TM, 3, Pi)
    rp.assessment(cdllist, prediction, 3, Ei)