#Imports
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal
from datetime import datetime
from geopy.geocoders import Nominatim

#filters
def IIRff(data, oder, cf):
    """
    Butterworth Zero Phase Lowpass filter.

    inputs:
    data: input data (np.array)
    oder: polynomial order (int)
    cf: 0-1 normalized cutoff frequency (float)

    returns:
    y: filtered data (np.array)
    """
    b, a = signal.butter(oder, cf, btype='low')
    y = signal.filtfilt(b, a, data)

    return y

def WEfilter(ts,d=2,lambda_v = 1):
    """
    Whittaker filter for time series smoothing
    """
    m = len(ts)
    E = np.eye(m)
    D = np.diff(E,d, axis=0)
    C = np.linalg.cholesky(E + lambda_v * D.T @ D)
    z = np.linalg.solve(C.T, np.linalg.solve(C, ts))
    return z

#MACD stage detection
def macd_cal(df, var, a = 5, b = 10, c = 5):
    """
    Calculate MACD and MACD divergence
    
    inputs:
    df: input data (pd.DataFrame)
    var: column name (str)
    a: EMA window a (int)
    b: EMA window b (int)
    c: EMA window c (int)

    returns:
    macd: MACD (pd.Series)
    macd_div: MACD divergence (pd.Series)
    """
    ema_a = df[var].ewm(span=a, min_periods=a, adjust=False).mean()
    ema_b = df[var].ewm(span=b, min_periods=b, adjust=False).mean()

    macd = ema_a - ema_b
    signal = macd.ewm(span=c, min_periods=c, adjust=False).mean()

    macd_div = macd - signal
    return macd, macd_div

def macd_stages(df, yt, var, start_season, end_season, a = 5, b = 10, c = 5, macd_div_threshold = 0, macd_threshold = 0, min_VI = 0.01, emg_max_VI = 0.5, sen_max_VI = 0.9, sma_n=7):
    """
    Stage detection using MACD
    
    inputs:
    df: input data (pd.DataFrame)
    yt: year (str)
    var: column name (str)
    start_season: start of growing season (datetime)
    end_season: end of growing season (datetime)
    a: EMA window a (int)
    b: EMA window b (int)
    c: EMA window c (int)
    macd_div_threshold: MACD divergence threshold (float)
    macd_threshold: MACD threshold (float)
    min_VI: minimum VI (float)
    emg_max_VI: maximum VI for emergence (float)
    sen_max_VI: maximum VI for senescence (float)
    sma_n: window for simple moving average (int)

    returns:
    emg: emergence (datetime)
    mat: maturity (datetime)
    sen: senescence (datetime)
    dor: dormancy (datetime)
    macd: MACD (pd.Series)
    macd_div: MACD divergence (pd.Series)
    valid: validity of the estimation (int)
    """
    macd, macd_div = macd_cal(df, var, a, b, c)

    ssd, esd = start_season.dayofyear, end_season.dayofyear
    up_cddoy = []

    
    #sma for vi test
    sma = df[var].rolling(window=sma_n, center=True).mean().reset_index(drop=True)
    zc=np.diff(np.sign(macd_div)).nonzero()[0]
    for i in zc:
        if (macd_div[i] < macd_div_threshold)&(macd_div[i+1] > macd_div_threshold)&(i+1 > ssd)&(i+1 < esd):
            if (df[var][i+1] > min_VI)&(df[var][i+1] < emg_max_VI):
                if (i+1+sma_n) < len(sma):
                    if (sma[i+1+sma_n] > sma[i+1]):
                        up_cddoy.append(i+1)

    if len(up_cddoy)==0:#no potential emergence
        return 0, 0, 0, 0, macd, macd_div, 0
    
    # Emergence
    up_momentum=[]
    for i in range(len(up_cddoy)-1):
        up_momentum.append(macd[up_cddoy[i]:up_cddoy[i+1]][macd[up_cddoy[i]:up_cddoy[i+1]]>0].sum())

    if len(np.diff(np.sign(macd[up_cddoy[-1]:]))<0)!=0:
        range_last=np.where(np.diff(np.sign(macd[up_cddoy[-1]:]))<0)[0]
        if range_last.size>0:
            up_momentum.append(macd[up_cddoy[-1]:up_cddoy[-1]+range_last[0]][macd[up_cddoy[-1]:up_cddoy[-1]+range_last[0]]>0].sum())
    if len(up_momentum)!=0:
        emg = up_cddoy[up_momentum.index(max(up_momentum))]
    else:
        emg = up_cddoy[0]

    # Maturity
    w=5
    sma = df[var].rolling(window=w, center=True).mean().reset_index(drop=True)
    sma_forward=np.array(sma[:-w].reset_index(drop=True)-sma[w:].reset_index(drop=True))
    sma_up=(sma_forward[:-w]<0)&(sma_forward[w:]>0)
    up_period = np.nonzero(sma_up)[0]+w
    up_period = up_period[macd[up_period]>0]
    if len(up_period[up_period > emg])>0:
        mat = up_period[(up_period > emg)][0]
    else:
        w=3
        sma = df[var].rolling(window=w, center=True).mean().reset_index(drop=True)
        sma_forward=np.array(sma[:-w].reset_index(drop=True)-sma[w:].reset_index(drop=True))
        sma_up=(sma_forward[:-w]<0)&(sma_forward[w:]>0)
        up_period = np.nonzero(sma_up)[0]+w
        up_period = up_period[macd[up_period]>0]
        if len(up_period[up_period > emg])>0:
            mat = up_period[up_period > emg][0]
        else:
            w=5
            sma_forward=np.array(df[var][:-w].reset_index(drop=True)-df[var][w:].reset_index(drop=True))
            sma_up=(sma_forward[:-w]<0)&(sma_forward[w:]>0)
            up_period = np.nonzero(sma_up)[0]+w
            up_period = up_period[macd[up_period]>0]
            if len(up_period[up_period > emg])>0:
                mat = up_period[up_period > emg][0]
            else:
                w=3
                sma_forward=np.array(df[var][:-w].reset_index(drop=True)-df[var][w:].reset_index(drop=True))
                sma_up=(sma_forward[:-w]<0)&(sma_forward[w:]>0)
                up_period = np.nonzero(sma_up)[0]+w
                up_period = up_period[macd[up_period]>0]
                if len(up_period[up_period > emg])>0:
                    mat = up_period[up_period > emg][0]
                else:
                    return 0, 0, 0, 0, macd, macd_div, 0


    # Senescence
    zc2=np.diff(np.sign(macd)).nonzero()[0]

    dw_cddoy = []

    for i in zc2:
        if (macd[i] > macd_threshold)&(macd[i+1] < macd_threshold)&(i+1 > ssd)&(i+1 < esd):
            if (df[var][i+1] > min_VI)&(df[var][i+1] < sen_max_VI):
                #if (sma[i+1+sma_n] < sma[i+1]):
                dw_cddoy.append(i+1)

    if len(dw_cddoy)==0:
        return 0, 0, 0, 0, macd, macd_div, 0

    dw_momentum=[]
    for i in range(len(dw_cddoy)-1):
        dw_momentum.append(macd[dw_cddoy[i]:dw_cddoy[i+1]][macd[dw_cddoy[i]:dw_cddoy[i+1]]<0].sum())
    
    range_last=np.where(np.diff(np.sign(macd[dw_cddoy[-1]:]))>0)[0]
    if range_last.size>0:
        dw_momentum.append(macd[dw_cddoy[-1]:dw_cddoy[-1]+range_last[0]][macd[dw_cddoy[-1]:dw_cddoy[-1]+range_last[0]]>0].sum())
        valid_sen = np.array(dw_momentum)[[np.array(dw_cddoy)>mat][0]]
    else:
        dw_momentum.append(macd[dw_cddoy[-1]:esd][macd[dw_cddoy[-1]:esd]>0].sum())
        valid_sen = np.array(dw_momentum)[[(np.array(dw_cddoy)>mat)][0]]
    if valid_sen.size>0:
        sen = dw_cddoy[dw_momentum.index(min(valid_sen))]
    else:
        sen = dw_cddoy[dw_momentum.index(min(dw_momentum))]#maybe can change to percentage threshold ~85% of max value

    # Dormancy
    w=5
    sma = df[var].rolling(window=w, center=True).mean().reset_index(drop=True)
    sma_forward=np.array(sma[:-w].reset_index(drop=True)-sma[w:].reset_index(drop=True))
    sma_dr=(sma_forward[:-w]>0)&(sma_forward[w:]<0)
    dw_period = np.nonzero(sma_dr)[0]+w
    dw_period = dw_period[macd[dw_period]<0]
    if len(dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)])>0:
        dor = dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)][0]
    else:
        w=3
        sma = df[var].rolling(window=w, center=True).mean().reset_index(drop=True)
        sma_forward=np.array(sma[:-w].reset_index(drop=True)-sma[w:].reset_index(drop=True))
        sma_dr=(sma_forward[:-w]>0)&(sma_forward[w:]<0)
        dw_period = np.nonzero(sma_dr)[0]+w
        dw_period = dw_period[macd[dw_period]<0]
        if len(dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)])>0:
            dor = dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)][0]
        else:
            w=5
            sma_forward=np.array(df[var][:-w].reset_index(drop=True)-df[var][w:].reset_index(drop=True))
            sma_dr=(sma_forward[:-w]>0)&(sma_forward[w:]<0)
            dw_period = np.nonzero(sma_dr)[0]+w
            dw_period = dw_period[macd[dw_period]<0]
            if len(dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)])>0:
                dor = dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)][0]
            else:
                w=3
                sma_forward=np.array(df[var][:-w].reset_index(drop=True)-df[var][w:].reset_index(drop=True))
                sma_dr=(sma_forward[:-w]>0)&(sma_forward[w:]<0)
                dw_period = np.nonzero(sma_dr)[0]+w
                dw_period = dw_period[macd[dw_period]<0]
                if len(dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)])>0:
                    dor = dw_period[(dw_period > sen)&(dw_period<esd)&(df[var][dw_period] < 0.5)][0]
                else:
                    dor = esd-1

    if (min([emg, mat, sen, dor]) != emg) or (max([emg, mat, sen, dor]) != dor) or (min([mat, sen, dor]) != mat) or (max([emg, mat, sen]) != sen):
        print('Error: emergence, maturity, senescence, dormancy not in order')
        return pd.to_datetime(yt+f'{emg}', format="%Y%j"), pd.to_datetime(yt+f'{mat+1}', format="%Y%j"), pd.to_datetime(yt+f'{sen}', format="%Y%j"), pd.to_datetime(yt+f'{dor+1}', format="%Y%j"), macd, macd_div, 0
    else:
        return pd.to_datetime(yt+f'{emg}', format="%Y%j"), pd.to_datetime(yt+f'{mat+1}', format="%Y%j"), pd.to_datetime(yt+f'{sen}', format="%Y%j"), pd.to_datetime(yt+f'{dor+1}', format="%Y%j"), macd, macd_div, 1
def get_location_info(latlon):
    latitude, longitude = latlon[1], latlon[0]
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    
    country = address.get('country', '')
    county = address.get('county', '')
    if 'state' in address:
        state = address.get('state', '')
        return county, state, country
    elif 'state_district' in address:
        province = address.get('state_district', '')
        return county, province, country   
#log df generation
def itwritein(lst, vara):
    """
    Append vara to lst 4 times
    
    inputs:
    lst: list (list)
    vara: write in object (any)

    returns:
    lst: list (list)
    """
    lst.append(vara[0])
    lst.append(vara[1])
    lst.append(vara[2])
    lst.append(vara[3])
    return lst

def eventtime_MACD(ndvits, seasondf, sitecdl, siteid, siteloc, start_year=None, end_year=None, smooth='ALL'):
    '''
    Apply MACD stage detection annually

    inputs:
    ndvits: ndvi time series with timestamp index (pd.DataFrame)
    seasondf: start_season and end_season with timestamp index (pd.DataFrame)
    sitecdl: crop type (pd.DataFrame)
    siteid: site ID (int)
    siteloc: WGS84 lon lat (str)
    start_year: start year (int)
    end_year: end year (int)
    smooth: smoothing method (str) default 'ALL'

    returns:
    lg: log (pd.DataFrame)
    Warning_log: log of cases that encountered errors ([Site ID, year, Crop]) (list)
    '''
    ndvits=ndvits.interpolate(method='linear',axis=0)
    county, state, country = get_location_info(siteloc)
    Warning_log=[]
    crop_id=[ 'Unidentify','Corn','Cotton','Rice','Sorghum','Soybeans','Sunflower','','','','Peanuts','Tobacco','Sweet Corn','Pop or Orn Corn','Mint','','','','','','','Barley','Durum Wheat','Spring Wheat','Winter Wheat','Other Small Grains','Dbl Crop WinWht/Soybeans','Rye','Oats','Millet','Speltz','Canola','Flaxseed','Safflower','Rape Seed','Mustard','Alfalfa','Other Hay/Non Alfalfa','Camelina','Buckwheat','','Sugarbeets','Dry Beans','Potatoes','Other Crops','Sugarcane','Sweet Potatoes','Misc Vegs & Fruits','Watermelons','Onions','Cucumbers','Chick Peas','Lentils','Peas','Tomatoes','Caneberries','Hops','Herbs','Clover/Wildflowers','Sod/Grass Seed','Switchgrass','Fallow/Idle Cropland','Pasture/Grass','Forest','Shrubland','Barren','Cherries','Peaches','Apples','Grapes','Christmas Trees','Other Tree Crops','Citrus','Pecans','Almonds','Walnuts','Pears','','','','Clouds/No Data','Developed','Water','','','','Wetlands','Nonag/Undefined','','','','Aquaculture','','','','','','','','','','','','','','','','','','','Open Water','Perennial Ice/Snow','','','','','','','','','Developed/Open Space','Developed/Low Intensity','Developed/Med Intensity','Developed/High Intensity','','','','','','','Barren','','','','','','','','','','Deciduous Forest','Evergreen Forest','Mixed Forest','','','','','','','','','Shrubland','','','','','','','','','','','','','','','','','','','','','','','','Grassland/Pasture','','','','','','','','','','','','','','Woody Wetlands','','','','','Herbaceous Wetlands','','','','','','','','','Pistachios','Triticale','Carrots','Asparagus','Garlic','Cantaloupes','Prunes','Olives','Oranges','Honeydew Melons','Broccoli','Avocados','Peppers','Pomegranates','Nectarines','Greens','Plums','Strawberries','Squash','Apricots','Vetch','Dbl Crop WinWht/Corn','Dbl Crop Oats/Corn','Lettuce','Dbl Crop Triticale/Corn','Pumpkins','Dbl Crop Lettuce/Durum Wht','Dbl Crop Lettuce/Cantaloupe','Dbl Crop Lettuce/Cotton','Dbl Crop Lettuce/Barley','Dbl Crop Durum Wht/Sorghum','Dbl Crop Barley/Sorghum','Dbl Crop WinWht/Sorghum','Dbl Crop Barley/Corn','Dbl Crop WinWht/Cotton','Dbl Crop Soybeans/Cotton','Dbl Crop Soybeans/Oats','Dbl Crop Corn/Soybeans','Blueberries','Cabbage','Cauliflower','Celery','Radishes','Turnips','Eggplants','Gourds','Cranberries','','','','Dbl Crop Barley/Soybeans']
    if start_year==None:
        start_year=ndvits.index.year.min()
    if end_year==None:
        end_year=ndvits.index.year.max()  
    lst1, lst2, lst3, lst4, lst5, lst6, lst7, lst8, lst9, lst10, lst11,lst12, lst13=[], [], [], [], [], [], [], [], [], [], [],[],[]
    lg=pd.DataFrame()
    
    def process_macd(df, yt, flt, start_season, end_season, siteid, sitecdl):

        #resetting var
        emg, mat, sen, dor, mask= 0, 0, 0, 0, 0
        if not isinstance(df, pd.DataFrame):
            df = pd.DataFrame({flt: df})
        emg, mat, sen, dor, _, _, mask = macd_stages(df, yt, flt, start_season, end_season)

        if mask == 1:
            s1dL.append(emg)
            s2dL.append(mat)
            s3dL.append(sen)
            s4dL.append(dor)
        else:
            fltL.append([flt,yt,siteid, sitecdl])
    def getVIrange(List, ndvits=ndvits):
        temp=ndvits.loc[List]['mean']
        mx, mn = temp.max(), temp.min()
        return [mn, mx]
    def VIlikeliness(allList, ndvits=ndvits):
        dormin=ndvits.loc[allList[3]]['mean'].idxmin()
        senmax=ndvits.loc[[ts for ts in allList[2] if ts <dormin]]['mean'].idxmax()
        matmax=ndvits.loc[[ts for ts in allList[1] if ts <senmax]]['mean'].idxmax()
        emgmin=ndvits.loc[[ts for ts in allList[0] if ts <matmax]]['mean'].idxmin()
        return [emgmin, matmax, senmax, dormin]
    
    for y in np.arange(start_year, end_year+1, 1):
        yt=f'{y}'
        start_season = seasondf.loc[int(yt)]['start_season']
        end_season = seasondf.loc[int(yt)]['end_season']
        #list for storing stages
        s1dL, s2dL, s4dL, s3dL, fltL = [], [], [], [], []
        
        #smoothing
        if smooth == 'ALL':
            IIR_smoothed = IIRff(ndvits.loc[yt]['mean'], 3, 0.05)
            sg_smoothed = signal.savgol_filter(ndvits.loc[yt]['mean'], window_length=31, polyorder=2)
            we_smoothed = WEfilter(ndvits.loc[yt]['mean'],3,1000)
            process_macd(IIR_smoothed, yt, 'BZP', start_season, end_season, siteid, sitecdl)
            process_macd(sg_smoothed, yt, 'SG', start_season, end_season, siteid, sitecdl)
            process_macd(we_smoothed, yt, 'WE', start_season, end_season, siteid, sitecdl)
        elif smooth == 'None':
            process_macd(ndvits.loc[yt]['mean'], yt, 'mean', start_season, end_season, siteid, sitecdl)
        else:
            if 'BZP' in smooth:
                IIR_smoothed = IIRff(ndvits.loc[yt]['mean'], 3, 0.05)
                process_macd(IIR_smoothed, yt, 'BZP', start_season, end_season, siteid, sitecdl)
            if 'SG' in smooth:
                sg_smoothed = signal.savgol_filter(ndvits.loc[yt]['mean'], window_length=31, polyorder=2)
                process_macd(sg_smoothed, yt, 'SG', start_season, end_season, siteid, sitecdl)
            if 'WE' in smooth:
                we_smoothed = WEfilter(ndvits.loc[yt]['mean'],3,1000)
                process_macd(we_smoothed, yt, 'WE', start_season, end_season, siteid, sitecdl)

        caseid=f'{siteid:04}'+'_'+yt
        
        # Write to list
        if len(s1dL) != 0:
            lst1=itwritein(lst1, [s1dL,s2dL,s3dL,s4dL])
            lst10=itwritein(lst10, VIlikeliness([s1dL,s2dL,s3dL,s4dL]))
            lst2=itwritein(lst2, ['Emergence', 'Maturity', 'Senescence', 'Dormancy'])
            lst3=itwritein(lst3, [caseid, caseid, caseid, caseid])
            lst4=itwritein(lst4, [siteid, siteid, siteid, siteid])
            lst5=itwritein(lst5, [county, county, county, county])
            lst6=itwritein(lst6, [state, state, state, state])
            lst7=itwritein(lst7, [country, country, country, country])
            lst8=itwritein(lst8, [getVIrange(s1dL),getVIrange(s2dL),getVIrange(s3dL),getVIrange(s4dL)])
            lst9=itwritein(lst9, [len(s1dL), len(s2dL), len(s3dL), len(s4dL)])
            #lst11=itwritein(lst11, [sitecdl.loc[y][0], sitecdl.loc[y][0], sitecdl.loc[y][0], sitecdl.loc[y][0]])
            lst12=itwritein(lst12, [crop_id[int(sitecdl.loc[y][0])], crop_id[int(sitecdl.loc[y][0])],crop_id[int(sitecdl.loc[y][0])],crop_id[int(sitecdl.loc[y][0])]])
            lst13=itwritein(lst13, [siteloc, siteloc, siteloc, siteloc])
        else:
            Warning_log.append([siteid, yt, sitecdl])
    lg['Activity']=lst2
    lg['Timestamp']=lst10
    lg['Time_uncertainty']=lst1
    lg['CaseID']=lst3
    #lg['CropID']=lst11
    lg['Crop']=lst12
    lg['SiteID']=lst4
    lg['WGS84_lon_lat']=lst13
    lg['County']=lst5
    lg['State']=lst6
    lg['Country']=lst7
    lg['NDVI_range']=lst8
    lg['num_valid_est']=lst9

    return lg, Warning_log

#plotting
def plot_macd(df, yt, flt, raw, start_season, end_season, s1dL, s2dL, s3dL, s4dL, fltL, valL):
    """
    Plotting MACD and detected stages

    inputs:
    df: NDVI time series (pd.DataFrame)
    yt: year (str)
    flt: filter used (str)
    raw: unfiltered NDVI time series (pd.Series)
    start_season: start of growing season (datetime)
    end_season: end of growing season (datetime)
    s1dL: emergence (list)
    s2dL: maturity (list)
    s3dL: senescence (list)
    s4dL: dormancy (list)
    fltL: filter used (list)
    valL: validity of the estimation (list)

    returns:
    None
    """
    #resetting var
    emg, mat, sen, dor, macd, macd_div, valid = 0, 0, 0, 0, 0, 0, 0
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame({flt: df})
    emg, mat, sen, dor, macd, macd_div, valid = macd_stages(df, yt, flt, start_season, end_season)
    fig, ax1=plt.subplots(figsize=(15,5))

    ax1.plot(raw, label='NDVI')
    ax1.plot(raw.index, df[flt], label=flt)
    ax2=ax1.twinx()
    ax2.plot(raw.index, macd, 'k.-', label='MACD')
    ax2.plot(raw.index, macd_div, 'r.-', label='MACD_div')

    ax2.set_ylim(-0.05, 0.1)
    ax1.set_ylabel('NDVI')
    ax2.set_ylabel('MACD')

    ax1.axvline(emg, color='g', label='emg')
    ax1.axvline(mat, color='r', label='mat') 
    ax1.axvline(sen, color='y', label='sen')
    ax1.axvline(dor, color='b', label='dor')
    ax1.axvline(x=start_season, color='c', linestyle='--', label='Last snow')
    ax1.axvline(x=end_season, color='c', linestyle='-.', label='First snow')
    ax1.legend()
    plt.grid()
    if valid == 1:
        ax1.set_title(yt+' MACD '+ flt+' This estimation is valid\n Emergence: '+str(emg)+' Maturity: '+str(mat)+' Senescence: '+str(sen)+' Dormancy: '+str(dor)+'\n Cultivation length: '+str(dor.dayofyear-emg.dayofyear)+' days')
        plt.show()
        s1dL.append(emg)
        s2dL.append(mat)
        s3dL.append(sen)
        s4dL.append(dor)
        fltL.append(flt)
        valL.append(valid)
    else:
        ax1.set_title(yt+' MACD '+ flt+' This estimation is not valid\n Emergence: '+str(emg)+' Maturity: '+str(mat)+' Senescence: '+str(sen)+' Dormancy: '+str(dor))
        plt.show()

def plot_uncertain(raw, start_season, end_season, yt, s1dL, s2dL, s3dL, s4dL, fltL):
    """
    Plot range of MACD estimated stages with different filters

    inputs:
    raw: unfiltered NDVI time series (pd.Series)
    start_season: start of growing season (datetime)
    end_season: end of growing season (datetime)
    yt: year (str)
    s1dL: emergence (list)
    s2dL: maturity (list)
    s3dL: senescence (list)
    s4dL: dormancy (list)
    fltL: filter used (list)
    
    returns:
    None
    """
    
    if len(s1dL)>0:

        w = fltL
        fig, ax1 = plt.subplots(figsize=(7,5))
        ax1.plot(w, s1dL, 'o-', label='emergence')
        ax1.plot(w, s2dL, 'o-', label='maturity')
        ax1.plot(w, s4dL, 'o-', label='dormancy')
        ax1.plot(w, s3dL, 'o-', label='Senescence')
        ax1.legend()
        ax1.set_title(yt+' MACD estimated dates with different filters')
        ax2=ax1.twinx()
        ax2.plot(w, [d.dayofyear-e.dayofyear for d, e in zip(s4dL, s1dL)], 'k--', label='Cultivation length')
        ax2.legend()
        ax2.set_ylabel('Cultivation length (Days)')
        ax1.set_ylabel('Date')
        ax1.set_xlabel('Filters')
        plt.tight_layout()
        plt.show()

        plt.figure(figsize=(15,6))
        plt.plot(raw, label='NDVI')
        plt.axvspan(min(s1dL),max(s1dL), alpha=0.5, color='g', label='emg')
        plt.axvspan(min(s2dL),max(s2dL), alpha=0.5, color='r', label='mat')
        plt.axvspan(min(s4dL),max(s4dL), alpha=0.5, color='k', label='dor')
        plt.axvspan(min(s3dL),max(s3dL), alpha=0.5, color='y', label='sen')
        plt.axvline(x=start_season, color='c', linestyle='--', label='Last snow')
        plt.axvline(x=end_season, color='c', linestyle='-.', label='First snow')
        plt.ylabel('NDVI')
        plt.xlabel('Date')
        plt.grid()
        plt.legend()
        plt.title(yt+' MACD stage estimation')
        plt.tight_layout()
    else:
        print('No valid estimation this year')