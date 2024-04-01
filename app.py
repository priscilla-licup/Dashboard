from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import geopandas as gpd
import pandas as pd
from pathlib import Path

dataset_folder = Path('datasets/')

# Import your data
educ_sites = gpd.read_file(dataset_folder / 'hotosm_phl_education_facilities.shp')
amenity_gdf = gpd.read_file(dataset_folder / 'ph_educ_by_amenity.geojson', driver='GeoJSON')
operatorty_gdf = gpd.read_file(dataset_folder / 'ph_educ_by_operatorty.geojson', driver='GeoJSON')

# Best to set the name of the location as the index for choropleths
amenity_gdf_indexed = amenity_gdf.set_index('province')
operatorty_gdf_indexed = operatorty_gdf.set_index('province')

# Options
amenity_options = []
for i in amenity_gdf.columns[4:-1]:
    amenity_options.append({
        'label': i, 
        'value': i
    })

operator_options = []
for i in operatorty_gdf.columns[4:-1]:
    operator_options.append({
        'label': i, 
        'value': i
    })

px.set_mapbox_access_token(open(".mapbox_token").read())

# Initializing your Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# You can make variables for your components / sections
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="PH Educational Institutions",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div(children=[
    navbar, # and add them to the layout
    dbc.Container(children=[
        dbc.Row(children=[
            html.H1("Philippine Educational Institutions"),
            html.P("Education is important and it helps ...."),
            html.P("Second paragraph here.")
        ]),
        dbc.Row(children=[
            html.H2("Which province has more schools?"),
        ]),
        dbc.Row(children=[
           dbc.Col(children=[
               html.P("Choose a column to display"),
               dbc.RadioItems(['amenity', 'operator'], 'amenity', id='map-type', inline=True)
           ], width=6),
           dbc.Col(children=[
               html.P("Choose the value to be displayed on the choropleth:"),
               dcc.Dropdown(options=amenity_options, value=amenity_options[0]['value'], id="choropleth-select")
           ], width=6)
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dcc.Loading(id="map-loading", children=dcc.Graph(id="map-graph"))
            ], width=6),
            dbc.Col(children=[
                dcc.Loading(id="bar-loading", children=dcc.Graph(id="bar-list"))
            ], width=6)
        ])
    ])
])

@callback(
    Output('choropleth-select', 'options'),
    Output('choropleth-select', 'value'),
    Input('map-type', 'value')
)
def set_dropdown_select(selected_type):
    options = None
    if selected_type == 'amenity':
        options = amenity_options
    else:
        options = operator_options

    value = options[0]['value']

    return options, value

@callback(
    Output('map-graph', 'figure'),
    Output('bar-list', 'figure'),
    Input('choropleth-select', 'value'),
    Input('map-type', 'value')
)
def display_map(selected_value, selected_type):
    if 'amenity' == selected_type:
        geodf = amenity_gdf_indexed

    elif 'operator' == selected_type:
        geodf = operatorty_gdf_indexed

    map_fig = px.choropleth_mapbox(geodf,
                           geojson=geodf.geometry,
                           locations=geodf.index,
                           color=selected_value,
                           center={'lat': 12.099568, 'lon': 122.733168},
                           zoom=4, height=800)
    map_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    sorted_df = geodf.sort_values(by=selected_value)
    bar_fig = px.bar(sorted_df, x=selected_value, y=sorted_df.index, 
                 color_continuous_scale='teal', color=selected_value, template='plotly_white', 
                 height=800, title='Provincial Schools Bar Chart')
    
    return map_fig, bar_fig


if __name__ == '__main__':
    app.run(debug=True)