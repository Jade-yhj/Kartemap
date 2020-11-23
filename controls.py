import pandas as pd
import numpy as np
from helper import compute_distance_in_kilometers, compute_distance_in_miles

CITY_DATA = 'data\\city.csv'
AIRPORT_DATA = 'data\\airport.csv'
AIRLINES_DATA = 'data\\airlines.csv'
ROUTES_DATA = 'data\\routes.csv'

TRACE = False
# load dataframe for cities
#
if TRACE:
    print('CITIES')
city_df = pd.read_csv(CITY_DATA, header=None)
city_df.columns = ['City', 'Population']
city_df['City'] = ['New York' if i == 'New York City' else i for i in city_df['City']]

if TRACE:
    print(city_df.shape)
    print(city_df)

# load dataframe for airports
#
if TRACE:
    print('AIRPORTS')
airport_df = pd.read_csv(AIRPORT_DATA, header=None)
airport_df.columns = ['Airport_id', 'Name', 'City', 'Country', 'IATA', 'ICAO', 'Latitude',
                      'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database time zone',
                      'type', 'Source']
if TRACE:
    print(1, airport_df.shape)

airport_df['Airport_id'] = pd.to_numeric(airport_df['Airport_id'])
airport_df.drop(airport_df[airport_df['Airport_id'] == r'\N'].index, inplace=True)
if TRACE:
    print(2, airport_df.shape)

city_names = list(city_df['City'])
print(city_names)
airport_df = airport_df[airport_df['City'].isin(city_names)]
if TRACE:
    print(3, airport_df.shape)
    print(airport_df)

# load dataframe for routes

if TRACE:
    print('ROUTES')
routes_df = pd.read_csv(ROUTES_DATA, header=None)
routes_df.columns = ['Airline', 'Airline_id', 'Source airport', 'Source_airport_id',
                     'Destination airport', 'Destination_airport_id', 'Codeshare', 'Stops',
                     'Equipment']
if TRACE:
    print(1, routes_df.shape)

routes_df.drop(routes_df[routes_df['Airline_id'] == r'\N'].index, inplace=True)
routes_df.drop(routes_df[routes_df['Source_airport_id'] == r'\N'].index, inplace=True)
routes_df.drop(routes_df[routes_df['Destination_airport_id'] == r'\N'].index, inplace=True)
if TRACE:
    print(2, routes_df.shape)

routes_df.drop(routes_df[routes_df['Stops'] != 0].index, inplace=True)
if TRACE:
    print(3, routes_df.shape)

routes_df['Airline_id'] = pd.to_numeric(routes_df['Airline_id'])
routes_df['Source_airport_id'] = pd.to_numeric(routes_df['Source_airport_id'])
routes_df['Destination_airport_id'] = pd.to_numeric(routes_df['Destination_airport_id'])

airport_ids = list(airport_df['Airport_id'])
routes_df = routes_df[routes_df['Source_airport_id'].isin(airport_ids)]
routes_df = routes_df[routes_df['Destination_airport_id'].isin(airport_ids)]

if TRACE:
    print(4, routes_df.shape)
    print(routes_df)

# load dataframe for airlines
#
# if TRACE:
    print('AIRLINES')
airlines_df = pd.read_csv(AIRLINES_DATA, header=None)
airlines_df.columns = ['Airline_id', 'Name', 'Alias', 'IATA', 'ICAO', 'Callsign',
                       'Country', 'Active']
if TRACE:
    print(1, airlines_df.shape)
airlines_df.drop(airlines_df[airlines_df['Airline_id'] == r'\N'].index, inplace=True)
airlines_df['Airline_id'] = pd.to_numeric(airlines_df['Airline_id'])
if TRACE:
    print(2, airlines_df.shape)
airlines_df.drop(airlines_df[airlines_df['Active'] != 'Y'].index, inplace=True)
if TRACE:
    print(3, airlines_df.shape)
airlines_df.drop(airlines_df[airlines_df['Country'] != 'United States'].index, inplace=True)
if TRACE:
    print(3, airlines_df.shape)
    print(airlines_df)

# Create network data from route and airport data
if TRACE:
    print('NETWORKS')
df = pd.merge(left = routes_df, right = airport_df, how = 'left', left_on = 'Source_airport_id', right_on = 'Airport_id')
if TRACE:
    print(1, df.shape)
    print(df.columns)
df = df.drop(['Airline', 'Airline_id','Source airport', 'Source_airport_id', 'Codeshare', 'Stops',
         'Destination airport','Equipment','Airport_id', 'City', 'Country', 'Altitude', 'IATA', 'ICAO', 'Timezone', 'DST', 'Tz database time zone',
         'type', 'Source'],axis = 1)
if TRACE:
    print(2, df.shape)
    print(df.columns)
df.columns = ['Destination_airport_id', 'Start_airport', 'Start_latitude', 'Start_longitude']
if TRACE:
    print(3, df.shape)
    print(df.columns)
df = pd.merge(left = df, right = airport_df, how = 'left', left_on = 'Destination_airport_id', right_on = 'Airport_id')
if TRACE:
    print(4, df.shape)
    print(df.columns)
df = df.drop(['Destination_airport_id','Airport_id', 'City', 'Country', 'Altitude', 'IATA', 'ICAO', 'Timezone', 'DST', 'Tz database time zone',
         'type', 'Source'],axis = 1)
if TRACE:
    print(5, df.shape)
    print(df.columns)
df.columns = ['Start_airport', 'Start_latitude', 'Start_longitude',
              'Destination_airport','Destination_latitude','Destination_longitude']
if TRACE:
    print(6, df.shape)
    print(df.columns)
df['distance'] = np.nan
for i in range(len(df)):
    distance = compute_distance_in_kilometers(df.loc[i, 'Start_longitude'],df.loc[i, 'Start_latitude'],
                                              df.loc[i, 'Destination_longitude'],df.loc[i, 'Destination_latitude'])
    df.loc[i,"distance"] = distance
if TRACE:
    print(7, df.shape)
    print(df.columns)
df = df.drop(['Start_latitude', 'Start_longitude',
              'Destination_longitude','Destination_latitude',],axis = 1)
if TRACE:
    print(8, df.shape)
    print(df.columns)
df['distance'] = pd.to_numeric(df['distance'])
df.to_csv("network.csv", index=False, header = 0)

# Only include airport that have network
airport_names = list(np.append(df['Start_airport'],df['Destination_airport']))
airport_df = airport_df[airport_df['Name'].isin(airport_names)]

if __name__ == "__main__":
    pass