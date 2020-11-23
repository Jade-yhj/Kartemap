# Import dataframe and functions
from controls import city_df, airport_df, routes_df, airlines_df
from main import main

# Import packages
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State

# PLot airport_df
# fig = px.scatter_mapbox(airport_df, lat="Latitude", lon="Longitude", hover_name="City", hover_data=["City", "Name"],
#                         color_discrete_sequence=["fuchsia"], zoom=3, height=300)
# fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig = go.Figure(go.Scattermapbox(
    mode="markers+lines",
    marker={'size': 10}))

fig.update_layout(
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox={
        'center': {'lon': 10, 'lat': 10},
        'style': "open-street-map",
        'center': {'lon': -20, 'lat': -20},
        'zoom': 1})

# Setup app with stylesheets
# app = dash.Dash()
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])

# Create map template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=40, r=40, b=30, t=50),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=20), orientation="h"),
    title="Map",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=3,
    ),
)

# Create controls
controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("Start City"),
                dcc.Dropdown(
                    options=[{"label": col, "value": col} for col in city_df['City']],
                    value="Choose a start city",
                    id="start-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Destination City"),
                dcc.Dropdown(
                    value="Choose a destination city",
                    id="destination-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Start Airport"),
                dcc.Dropdown(
                    value="Choose a start airport",
                    id="start-airport",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Destination Airport"),
                dcc.Dropdown(
                    value="Choose a destination airport",
                    id="destination-airport",
                ),
            ]
        ),
        dbc.Button("Submit", id = "submit", outline=True, color="primary", className="mr-1"),
    ],
    body=True,
)

# Create layout
app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.H3("Kartemap - An Airport Network Analysis Application",
                        style = {"margin-bottom": "Opx"})
            )
        ),
        dbc.Row(
            [
                dbc.Col(controls, md=2),
                dbc.Col(dcc.Graph(id="map", figure=fig), md=10),
            ],
            align="center",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(id = 'start-city-image', src = None, top=True),
                            dbc.CardBody(
                                [
                                    html.H4(id="start-city-title",className="card-title"),
                                    html.P(id="start-city-population",className="card-text"),
                                ]
                            ),
                        ]
                    ),
                    md = 5
                ),
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardImg(id = 'destination-city-image',src = None, top=True),
                            dbc.CardBody(
                                [
                                    html.H4(id="destination-city-title",className="card-title"),
                                    html.P(id="destination-city-population",className="card-text"),
                                ]
                            ),
                        ]
                    ),
                    md = 5
                ),
            ],
            align="center",
        ),
        html.P(id="output"),
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)

# Set up callback
# Change destination cities options based on selected start city
@app.callback(
    Output('destination-city', 'options'),
    [Input('start-city', 'value')])
def set_destination_cities_options(start_city):
    return [{'label': i, 'value': i} for i in city_df['City'] if i != start_city]

@app.callback(
    Output('start-airport', 'options'),
    [Input('start-city', 'value')])
def set_start_airport_options(start_city):
    start_airport = airport_df.loc[airport_df['City'] == start_city]
    return [{'label': i, 'value': i} for i in start_airport['Name']]

@app.callback(
    Output('destination-airport', 'options'),
    [Input('destination-city', 'value')])
def set_start_airport_options(destination_city):
    destination_airport = airport_df.loc[airport_df['City'] == destination_city]
    return [{'label': i, 'value': i} for i in destination_airport['Name']]

@app.callback(
    Output('map', 'figure'),
    [Input('submit','n_clicks')],
    state=[State('start-airport','value'),State('destination-airport','value')])
def make_map(num_clicks, start_airport, destination_airport):
    if start_airport is None or destination_airport is None:
        raise PreventUpdate
    else:
        [path, distance] = main(start_airport, destination_airport)
        lon = []
        lat = []
        for p in path:
            lon.append(airport_df[airport_df['Name'] == p]['Longitude'])
            lat.append(airport_df[airport_df['Name'] == p]['Latitude'])
        longitude = []
        for sublist in lon:
            for item in sublist:
                longitude.append(item)
        latitude = []
        for sublist in lat:
            for item in sublist:
                latitude.append(item)

        fig = go.Figure(go.Scattermapbox(
            mode="markers+lines",
            lon=longitude,
            lat=latitude,
            text=path,
            marker = {'size': 10},
            # hovertemplate =
            # "%{text}<br>" +
            # "longitude: %{lon}<br>" +
            # "latitude: %{lat}<br>"
            ))
        fig.update_layout(
            margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
            mapbox={
                'center': {'lon': 10, 'lat': 10},
                'style': "open-street-map",
                'center': {'lon': -20, 'lat': -20},
                'zoom': 1})
        return fig

@app.callback(
    Output('output', 'children'),
    [Input('submit','n_clicks')],
    state=[State('start-airport','value'),State('destination-airport','value')])
def output_text(num_clicks, start_airport, destination_airport):
    if start_airport is None or destination_airport is None:
        raise PreventUpdate
    else:
        [path, distance] = main(start_airport, destination_airport)
        return f"The shortest distance between {start_airport} and {destination_airport} is {distance} km."

@app.callback(
    [
     Output('start-city-image', 'src'),
     Output('start-city-title', 'children'),
     Output('start-city-population', 'children'),
     Output('destination-city-image', 'src'),
     Output('destination-city-title', 'children'),
     Output('destination-city-population', 'children'),
    ],
    [Input('submit','n_clicks')],
    state=[State('start-city','value'),State('destination-city','value')])
def output_card(num_clicks, start_city, destination_city):
    if start_city is None or destination_city is None or num_clicks is None:
        raise PreventUpdate
    else:
        start_city_image = "image/"
        start_city_image += start_city
        start_city_image += '.png'
        start_base64 = base64.b64encode(open(start_city_image, 'rb').read()).decode('ascii')
        start_src='data:image/png;base64,{}'.format(start_base64)
        destination_city_image = "image/"
        destination_city_image += destination_city
        destination_city_image += '.png'
        destination_base64 = base64.b64encode(open(destination_city_image, 'rb').read()).decode('ascii')
        destination_src = 'data:image/png;base64,{}'.format(destination_base64)
        start_city_population = f"Population:{city_df[city_df['City'] == start_city]['Population'].to_string()[5:]}"
        destination_city_population = f"Population:{city_df[city_df['City'] == destination_city]['Population'].to_string()[5:]}"
        return  start_src, start_city, start_city_population,destination_src,destination_city,destination_city_population

# Main
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_ui=False, dev_tools_props_check=False)