#imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pm4py
from pm4py.objects.conversion.log import converter as log_converter 

crop_id=[ '','Corn','Cotton','Rice','Sorghum','Soybeans','Sunflower','','','','Peanuts','Tobacco','Sweet Corn','Pop or Orn Corn','Mint','','','','','','','Barley','Durum Wheat','Spring Wheat','Winter Wheat','Other Small Grains','Dbl Crop WinWht/Soybeans','Rye','Oats','Millet','Speltz','Canola','Flaxseed','Safflower','Rape Seed','Mustard','Alfalfa','Other Hay/Non Alfalfa','Camelina','Buckwheat','','Sugarbeets','Dry Beans','Potatoes','Other Crops','Sugarcane','Sweet Potatoes','Misc Vegs & Fruits','Watermelons','Onions','Cucumbers','Chick Peas','Lentils','Peas','Tomatoes','Caneberries','Hops','Herbs','Clover/Wildflowers','Sod/Grass Seed','Switchgrass','Fallow/Idle Cropland','Pasture/Grass','Forest','Shrubland','Barren','Cherries','Peaches','Apples','Grapes','Christmas Trees','Other Tree Crops','Citrus','Pecans','Almonds','Walnuts','Pears','','','','Clouds/No Data','Developed','Water','','','','Wetlands','Nonag/Undefined','','','','Aquaculture','','','','','','','','','','','','','','','','','','','Open Water','Perennial Ice/Snow','','','','','','','','','Developed/Open Space','Developed/Low Intensity','Developed/Med Intensity','Developed/High Intensity','','','','','','','Barren','','','','','','','','','','Deciduous Forest','Evergreen Forest','Mixed Forest','','','','','','','','','Shrubland','','','','','','','','','','','','','','','','','','','','','','','','Grassland/Pasture','','','','','','','','','','','','','','Woody Wetlands','','','','','Herbaceous Wetlands','','','','','','','','','Pistachios','Triticale','Carrots','Asparagus','Garlic','Cantaloupes','Prunes','Olives','Oranges','Honeydew Melons','Broccoli','Avocados','Peppers','Pomegranates','Nectarines','Greens','Plums','Strawberries','Squash','Apricots','Vetch','Dbl Crop WinWht/Corn','Dbl Crop Oats/Corn','Lettuce','Dbl Crop Triticale/Corn','Pumpkins','Dbl Crop Lettuce/Durum Wht','Dbl Crop Lettuce/Cantaloupe','Dbl Crop Lettuce/Cotton','Dbl Crop Lettuce/Barley','Dbl Crop Durum Wht/Sorghum','Dbl Crop Barley/Sorghum','Dbl Crop WinWht/Sorghum','Dbl Crop Barley/Corn','Dbl Crop WinWht/Cotton','Dbl Crop Soybeans/Cotton','Dbl Crop Soybeans/Oats','Dbl Crop Corn/Soybeans','Blueberries','Cabbage','Cauliflower','Celery','Radishes','Turnips','Eggplants','Gourds','Cranberries','','','','Dbl Crop Barley/Soybeans']

def rotation_prediction_preprocess(cdllist, L=7, W=5, val_year=2):
    CTM=[]
    Tmarker=[]
    CID=[]
    year=[]
    id=0
    for i in cdllist:
        for j in range(len(i)-(W+val_year)):
            tL = [crop_id[int(x)] for x in np.array(i[j:j+W])]
            tL = ['']+tL+['']
            CTM.append(tL)
            Tmarker.append(np.arange(0,L,1))
            CID.append([f'Site {id}-W{j+1}']*(L))
            year.append([pd.Timestamp(y,1,1) for y in i.index[j:j+W]])
        id+=1

    CTMf = np.array(CTM).flatten()#reformed windowed list
    Tmarkerf = np.array(Tmarker).flatten()#sequential time marker(1-6)
    CIDf = np.array(CID).flatten()#case id with window number
    #yearf = np.array(year).flatten()
    log = log_converter.apply(pd.DataFrame({'case:concept:name':CIDf, 'concept:name':CTMf, 'time:timestamp':Tmarkerf}))
    return log

def dfg_to_transition_matrix(dfg_matrix, crop_id=crop_id):
    TM=np.zeros((len(crop_id),len(crop_id)))

    for i in range(len(crop_id)):
        for j in range(len(crop_id)):
            if (dfg_matrix['suc']==(crop_id[i],crop_id[j])).sum()!=0:
                TM[i,j]=int(dfg_matrix[dfg_matrix['suc']==(crop_id[i],crop_id[j])]['freq'])
    TM/=TM.sum(axis=1)[:,None]
    return TM

def assessment(cdllist, TM ,BestX=3, Pi=-2, Ei=-1, crop_id=crop_id):
    SVP=[] #x test(state vector prediction)
    SVE=[] #y test(state vector evaluation)
    for i in cdllist:
        SVP.append(crop_id[int(np.array(i)[Pi])])
        SVE.append(crop_id[int(np.array(i)[Ei])])
    SVE=np.array(SVE)
    SVP=np.array(SVP)

    iSVP=[np.where(np.array(crop_id)==c)[0][0] for c in SVP]
    predictBestX=[np.array(crop_id)[np.argsort(TM[i])[-BestX:][::-1]] for i in iSVP]
    AC=np.array([SVE[x] in predictBestX[x] for x in range(SVE.shape[0])])

    print(f'Predicting: {cdllist[0].index[Ei]}')    
    print(f'True positive found in top {BestX} prediction: ',AC.sum())
    print('Recall: ', AC.sum()/SVE.shape[0])
    print('Precision: ', (AC.sum()/SVE.shape[0])/(BestX))
    print('True positive:\n', np.unique(SVE[AC], return_counts=True))
    print('Prediction:\n',np.unique(predictBestX,return_counts=True))
    print('---------------------------------------------------------------')