# import plotly.graph_objects as go
#
# lon = [10, 20, 30]
# lat = [10, 20,30]
#
# fig = go.Figure(go.Scattermapbox(
#     mode = "markers+lines",
#     lon = lon,
#     lat = lat,
#     marker = {'size': 10}))
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



import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
import base64

app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])

start_city = 'New York'
start_city_image = "image/"
start_city_image += start_city
start_city_image += '.png'
start_base64 = base64.b64encode(open(start_city_image, 'rb').read()).decode('ascii')
start_src='data:image/png;base64,{}'.format(start_base64)


app.layout = dbc.Card(
    [
        dbc.CardBody(html.P("This has a bottom image", className="card-text")),
        dbc.CardImg(src=start_src, bottom=True),
    ],
    style={"width": "18rem"},
)


if __name__ == "__main__":
    app.run_server(debug=True)

#
# time.sleep(5)  # Delay for 5 seconds.
#
# global_df = pd.DataFrame({'value1': [1, 2, 3, 4],
#                           'value2': [10, 11, 12, 14]})
#
# # app = JupyterDash(__name__)
# app = JupyterDash(external_stylesheets=[dbc.themes.SLATE])
#
# df = pd.DataFrame({'Value 1': [1, 2, 3],
#                    'Value 2': [10, 11, 12],
#                    'Value 3': [14, 12, 9]})
#
# df.set_index('Value 1', inplace=True)
#
# app.layout = html.Div([
#     # The memory store reverts to the default on every page refresh
#     dcc.Store(id='memory'),
#     # The local store will take the initial data
#     # only the first time the page is loaded
#     # and keep it until it is cleared.
#     # Same as the local store but will lose the data
#     # when the browser/tab closes.
#     html.Table([
#         html.Thead([
#             html.Tr(html.Th('Click to launch figure:')),
#             html.Tr([
#                 html.Th(html.Button('Figures', id='memory-button')),
#             ]),
#         ]),
#     ]),
#     dcc.Loading(id="loading-icon",
#                 # 'graph', 'cube', 'circle', 'dot', or 'default'
#                 type='cube',
#                 children=[html.Div(dcc.Graph(id='click_graph'))])
# ])
#
#
# # Create two callbacks for every store.
# # add a click to the appropriate store.
# @app.callback(Output('memory', 'data'),
#               [Input('memory-button', 'n_clicks')],
#               [State('memory', 'data')])
# def on_click(n_clicks, data):
#     if n_clicks is None:
#         # prevent the None callbacks is important with the store component.
#         # you don't want to update the store for nothing.
#         raise PreventUpdate
#
#     # Give a default data dict with 0 clicks if there's no data.
#     data = data or {'clicks': 0}
#     data['clicks'] = data['clicks'] + 1
#     if data['clicks'] > 3: data['clicks'] = 0
#
#     return data
#
#
# # output the stored clicks in the table cell.
# @app.callback(Output('click_graph', 'figure'),
#               # Since we use the data prop in an output,
#               # we cannot get the initial data on load with the data prop.
#               # To counter this, you can use the modified_timestamp
#               # as Input and the data as State.
#               # This limitation is due to the initial None callbacks
#               # https://github.com/plotly/dash-renderer/pull/81
#               [Input('memory', 'modified_timestamp')],
#               [State('memory', 'data')])
# def on_data(ts, data):
#     if ts is None:
#         # raise PreventUpdate
#         fig = go.Figure()
#         fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
#                           yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(0,0,0,0)')),
#                           xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(0,0,0,0)')))
#         return (fig)
#     data = data or {}
#     0
#     # plotly
#     y = 'Value 2'
#     y2 = 'Value 3'
#
#     fig = go.Figure()
#     fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
#                       yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(0,0,0,0)')),
#                       xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='rgba(0,0,0,0)')))
#
#     if data.get('clicks', 0) == 1:
#         fig = go.Figure(go.Scatter(name=y, x=df.index, y=df[y], mode='lines'))
#         fig.add_traces(go.Scatter(name=y, x=df.index, y=df[y2], mode='lines'))
#         fig.update_layout(template='plotly_dark',
#                           title='Plot number ' + str(data.get('clicks', 0)))
#
#         # delay only after first click
#         time.sleep(2)
#
#     if data.get('clicks', 0) == 2:
#         fig = go.Figure((go.Scatter(name=y, x=df.index, y=df[y], mode='lines')))
#         fig.add_traces(go.Scatter(name=y, x=df.index, y=df[y2], mode='lines'))
#         fig.update_layout(template='seaborn',
#                           title='Plot number ' + str(data.get('clicks', 0)))
#
#     if data.get('clicks', 0) == 3:
#         fig = go.Figure((go.Scatter(name=y, x=df.index, y=df[y], mode='lines')))
#         fig.add_traces(go.Scatter(name=y, x=df.index, y=df[y2], mode='lines'))
#         fig.update_layout(template='plotly_white',
#                           title='Plot number ' + str(data.get('clicks', 0)))
#
#     # Aesthetics
#     fig.update_layout(margin={'t': 30, 'b': 0, 'r': 50, 'l': 50, 'pad': 0},
#                       hovermode='x',
#                       legend=dict(x=1, y=0.85),
#                       uirevision='constant')
#
#     # delay for every figure
#     time.sleep(2)
#     return fig
#
#
# app.run_server(mode='external', port=8070, dev_tools_ui=True,
#                dev_tools_hot_reload=True, threaded=True)