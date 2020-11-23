from controls import city_df, airport_df, routes_df, airlines_df
from main import main
import numpy as np
import plotly.graph_objects as go

start_airport = "John F Kennedy International Airport"
destination_airport = "Los Angeles International Airport"

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

start_city = 'New York'
start_city_image = "image/"
start_city_image += start_city
start_city_image += '.jpg'
print(start_city)
print(start_city_image)
t = city_df[city_df['City']==start_city]['Population'].to_string()[5:]
print(t)




# data = px.data.gapminder()
# df_2007 = data[data['year']==2007]
# df_2007 = df_2007.sort_values(['continent', 'country'])
#
# bubble_size = []
#
# for index, row in df_2007.iterrows():
#     bubble_size.append(math.sqrt(row['pop']))
#
# df_2007['size'] = bubble_size
# continent_names = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
# continent_data = {continent:df_2007.query("continent == '%s'" %continent)
#                               for continent in continent_names}
#
# fig = go.Figure()
#
# for continent_name, continent in continent_data.items():
#     fig.add_trace(go.Scatter(
#         x=continent['gdpPercap'],
#         y=continent['lifeExp'],
#         name=continent_name,
#         text=df_2007['continent'],
#         hovertemplate=
#         "<b>%{text}</b><br><br>" +
#         "GDP per Capita: %{x:$,.0f}<br>" +
#         "Life Expectation: %{y:.0%}<br>" +
#         "Population: %{marker.size:,}" +
#         "<extra></extra>",
#         marker_size=continent['size'],
#         ))
#
# fig.update_traces(
#     mode='markers',
#     marker={'sizemode':'area',
#             'sizeref':10})
#
# fig.update_layout(
#     xaxis={
#         'title':'GDP per capita',
#         'type':'log'},
#     yaxis={'title':'Life Expectancy (years)'})
#
# fig.show()

# [path, distance] = main(start_airport, destination_airport)
# # # lon = [10, 20, 30]
# # lat = [10, 20, 30]
# # print('lat',lat)
# lon = []
# lat = []
# for p in path:
#     lon.append(airport_df[airport_df['Name'] == p]['Longitude'])
#     lat.append(airport_df[airport_df['Name'] == p]['Latitude'])
# longitude = []
# for sublist in lon:
#     for item in sublist:
#         longitude.append(item)
# latitude = []
# for sublist in lat:
#     for item in sublist:
#         latitude.append(item)
# print(longitude)
# print(latitude)
#
# fig = go.Figure(go.Scattermapbox(
#     mode="markers+lines",
#     lon=longitude,
#     lat=latitude,
#     marker={'size': 10}))
#
# fig.update_layout(
#     margin ={'l':0,'t':0,'b':0,'r':0},
#     mapbox = {
#         'center': {'lon': 10, 'lat': 10},
#         'style': "stamen-terrain",
#         'center': {'lon': -20, 'lat': -20},
#         'zoom': 1})
#
# fig.show()

# TRACE = True
#
# plot_airport = airport_df.loc[airport_df["Name"].isin([start_airport, destination_airport])]
# fig = px.scatter_mapbox(plot_airport, lat="Latitude", lon="Longitude", hover_name="City",
#                         hover_data=["City", "Name"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
# fig.show()

# fig = px.scatter_mapbox(airport_df, lat="Latitude", lon="Longitude", hover_name="City", hover_data=["City", "Name"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()
#
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
#
# app = dash.Dash()
# app.layout = html.Div([
#     dcc.Graph(figure=fig)
# ])
#
# app.run_server(debug=True, use_reloader=False)  # Turn off reloader if inside Jupyter
#
