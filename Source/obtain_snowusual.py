df = pd.read_csv('C:/Users/Vito/Documents/Seed_to_harvest_process_monitoring/Source/Data/Idaho/masklayers/weather.csv')
df['year']=pd.to_datetime(df['DATE']).dt.year
df['doy']=pd.to_datetime(df['DATE']).dt.dayofyear
