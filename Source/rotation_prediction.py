#imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter 
from pm4py.algo.clustering.trace_attribute_driven import variants
import pm4py

crop_id=[ '','Corn','Cotton','Rice','Sorghum','Soybeans','Sunflower','','','','Peanuts','Tobacco','Sweet Corn','Pop or Orn Corn','Mint','','','','','','','Barley','Durum Wheat','Spring Wheat','Winter Wheat','Other Small Grains','Dbl Crop WinWht/Soybeans','Rye','Oats','Millet','Speltz','Canola','Flaxseed','Safflower','Rape Seed','Mustard','Alfalfa','Other Hay/Non Alfalfa','Camelina','Buckwheat','','Sugarbeets','Dry Beans','Potatoes','Other Crops','Sugarcane','Sweet Potatoes','Misc Vegs & Fruits','Watermelons','Onions','Cucumbers','Chick Peas','Lentils','Peas','Tomatoes','Caneberries','Hops','Herbs','Clover/Wildflowers','Sod/Grass Seed','Switchgrass','Fallow/Idle Cropland','Pasture/Grass','Forest','Shrubland','Barren','Cherries','Peaches','Apples','Grapes','Christmas Trees','Other Tree Crops','Citrus','Pecans','Almonds','Walnuts','Pears','','','','Clouds/No Data','Developed','Water','','','','Wetlands','Nonag/Undefined','','','','Aquaculture','','','','','','','','','','','','','','','','','','','Open Water','Perennial Ice/Snow','','','','','','','','','Developed/Open Space','Developed/Low Intensity','Developed/Med Intensity','Developed/High Intensity','','','','','','','Barren','','','','','','','','','','Deciduous Forest','Evergreen Forest','Mixed Forest','','','','','','','','','Shrubland','','','','','','','','','','','','','','','','','','','','','','','','Grassland/Pasture','','','','','','','','','','','','','','Woody Wetlands','','','','','Herbaceous Wetlands','','','','','','','','','Pistachios','Triticale','Carrots','Asparagus','Garlic','Cantaloupes','Prunes','Olives','Oranges','Honeydew Melons','Broccoli','Avocados','Peppers','Pomegranates','Nectarines','Greens','Plums','Strawberries','Squash','Apricots','Vetch','Dbl Crop WinWht/Corn','Dbl Crop Oats/Corn','Lettuce','Dbl Crop Triticale/Corn','Pumpkins','Dbl Crop Lettuce/Durum Wht','Dbl Crop Lettuce/Cantaloupe','Dbl Crop Lettuce/Cotton','Dbl Crop Lettuce/Barley','Dbl Crop Durum Wht/Sorghum','Dbl Crop Barley/Sorghum','Dbl Crop WinWht/Sorghum','Dbl Crop Barley/Corn','Dbl Crop WinWht/Cotton','Dbl Crop Soybeans/Cotton','Dbl Crop Soybeans/Oats','Dbl Crop Corn/Soybeans','Blueberries','Cabbage','Cauliflower','Celery','Radishes','Turnips','Eggplants','Gourds','Cranberries','','','','Dbl Crop Barley/Soybeans']

def rotation_prediction_preprocess(cdllist, L=7, W=5, val_year=2):
    '''
    Preprocess the crop data list to be used for rotation prediction
    
    inputs:
    cdllist: List of cropping history data (list)
    L: Number of years used for estimation (int)
    W: Window length (int)
    val_year: Number of years retained for validation (int)

    outputs:
    log: Log of the preprocessed data (pm4py log)
    '''
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
    log = log_converter.apply(pd.DataFrame({'case:concept:name':CIDf, 'concept:name':CTMf, 'time:timestamp':Tmarkerf}))
    return log

def dfg_to_transition_matrix(log, crop_id=crop_id):
    '''
    Estimate the transition matrix from the log

    inputs:
    log: Preprocessed log (pm4py log)
    crop_id: Crop id list (list)

    outputs:
    TM: Transition matrix (np.array)
    '''
    dfg, start_activities, end_activities = pm4py.discover_dfg(log)
    log2 = pm4py.filter_event_attribute_values(log, 'concept:name', '', "event",False)
    dfg, start_activities, end_activities = pm4py.discover_dfg(log2)
    dfg_matrix = variants.suc_dist_calc.occu_suc(dfg, 100)

    TM=np.zeros((len(crop_id),len(crop_id)))

    for i in range(len(crop_id)):
        for j in range(len(crop_id)):
            if (dfg_matrix['suc']==(crop_id[i],crop_id[j])).sum()!=0:
                TM[i,j]=int(dfg_matrix[dfg_matrix['suc']==(crop_id[i],crop_id[j])]['freq'])
    TM/=TM.sum(axis=1)[:,None]
    return TM

def prediction(cdllist, TM ,BestX=3, Pi=-2, crop_id=crop_id):
    '''
    Best x prediction of crop rotation with transition matrix

    inputs:
    cdllist: List of cropping history data (list)
    TM: Transition matrix (np.array)
    BestX: Number of most probable prediction considered (int)
    Pi: Index of the last year in the cropping history (int)
    crop_id: Crop id list (list)

    outputs:
    predictBestX: Best x prediction of crop rotation (list)
    '''
    SVP=[] #x test(state vector prediction)
    for i in cdllist:
        SVP.append(crop_id[int(np.array(i)[Pi])])
    SVP=np.array(SVP)
    iSVP=[np.where(np.array(crop_id)==c)[0][0] for c in SVP]
    predictBestX=[np.array(crop_id)[np.argsort(TM[i])[-BestX:][::-1]] for i in iSVP]
    return predictBestX

def assessment(cdllist, predictBestX,BestX=3,Ei=-1, crop_id=crop_id):
    '''
    Accuracy assessment of the prediction

    inputs:
    cdllist: List of cropping history data (list)
    predictBestX: Crop roataion prediction (list)
    BestX: Number of most probable prediction considered (int)
    Ei: Index of the predicted year (int)
    crop_id: Crop id list (list)

    outputs:
    None
    '''
    SVE=[] #y test(state vector evaluation)
    for i in cdllist:
        SVE.append(crop_id[int(np.array(i)[Ei])])
    SVE=np.array(SVE)

    AC=np.array([SVE[x] in predictBestX[x] for x in range(SVE.shape[0])])

    print(f'Predicting: {cdllist[0].index[Ei]}')    
    print(f'True positive found in top {BestX} prediction: ',AC.sum())
    print('Recall: ', AC.sum()/SVE.shape[0])
    print('Precision: ', (AC.sum()/SVE.shape[0])/(BestX))
    print('True positive:\n', np.unique(SVE[AC], return_counts=True))
    print('Prediction:\n',np.unique(predictBestX,return_counts=True))
    print('---------------------------------------------------------------')