from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import geopandas as gpd
import pandas as pd
from pathlib import Path


dataset_folder = Path('datasets/')
waste_dataset_folder = Path('datasets/waste_data')
new_waste_dataset_folder = Path('datasets/waste_data/new')
geojson_dataset_folder = Path('datasets/geojson')

# Import your data
data_2015 = gpd.read_file(waste_dataset_folder / '2015.csv')
data_2016 = gpd.read_file(waste_dataset_folder / '2016.csv')
data_2017 = gpd.read_file(waste_dataset_folder / '2017.csv')
data_2018 = gpd.read_file(waste_dataset_folder / '2018.csv')
data_2019 = gpd.read_file(waste_dataset_folder / '2019.csv')
data_2020 = gpd.read_file(waste_dataset_folder / '2020.csv')
data_2021 = gpd.read_file(waste_dataset_folder / '2021.csv')
data_2022 = gpd.read_file(waste_dataset_folder / '2022.csv')

# TENTATIVE (Cleaned from Google Colab)
new_data_2015 = gpd.read_file(new_waste_dataset_folder / '2015.csv')
new_data_2016 = gpd.read_file(new_waste_dataset_folder / '2016.csv')
new_data_2017 = gpd.read_file(new_waste_dataset_folder / '2017.csv')
new_data_2018 = gpd.read_file(new_waste_dataset_folder / '2018.csv')
new_data_2019 = gpd.read_file(new_waste_dataset_folder / '2019.csv')
new_data_2020 = gpd.read_file(new_waste_dataset_folder / '2020.csv')
new_data_2021 = gpd.read_file(new_waste_dataset_folder / '2021.csv')
new_data_2022 = gpd.read_file(new_waste_dataset_folder / '2022.csv')

amenity_gdf = gpd.read_file(dataset_folder / 'ph_educ_by_amenity.geojson', driver='GeoJSON')
operatorty_gdf = gpd.read_file(dataset_folder / 'ph_educ_by_operatorty.geojson', driver='GeoJSON')

datasets_by_year = {
    2015: new_data_2015,
    2016: new_data_2016,
    2017: new_data_2017,
    2018: new_data_2018,
    2019: new_data_2019,
    2020: new_data_2020,
    2021: new_data_2021,
    2022: new_data_2022,
}

slider_marks = {year: {'label': str(year)} for year in range(2015, 2023)}

# --------------------------------------
# Choropleth - Data
# (Kindly download shp files from this link: https://drive.google.com/drive/folders/1jbTFtNb8MRWi8B9MSl6VXKAChHfKug8O?usp=sharing)

ph_gdf = gpd.read_file('datasets/gadm/phl_admbnda_adm1_psa_namria_20231106.shp')

data_years = range(2015, 2023)
geojson_data = {}
for year in data_years:
    geojson_data[year] = gpd.read_file(geojson_dataset_folder / f'{year}_gdf.geojson', driver='GeoJSON')

# --------------------------------------

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

# --------------------------------------

# Initializing your Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# You can make variables for your components / sections
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="#")),
    ],
    brand="DASHBOARD",
    brand_href="#",
    color="black",
    dark=True,
)

waste_columns = [
    'Wastes with Cyanide', 'Acid Wastes', 'Alkali Wastes', 'Wastes with Inorganic Chemicals', 'Reactive Chemical Wastes',
    'Inks/Dyes/Pigments/Paint/Latex/Adhesives/Organic Sludge', 'Waste Organic Solvents', 'Organic Wastes', 'Oil', 'Containers', 'Stabilized Wastes', 'Organic Chemicals', 'Miscellaneous Wastes', 'Total Hazardous Wastes', 'Total Treated Hazardous Wastes'
]

faci_columns = [
    'Materials Recovery Facility', 'Sanitary Landfill', 'Registered TSD Facilities'
]

# Choropleth - Dropdown
dropdown_options = [
    {'label': 'Hazardous Waste Per Capita', 'value': 'Hazardous Waste Per Capita'},
    {'label': 'Total Disposal Facilities', 'value': 'Total Disposal Facilities'},
    {'label': 'Total Hazardous Wastes', 'value': 'Total Hazardous Wastes'}
]

# Region - Dropdown

region_options = [{'label': region, 'value': region} for region in new_data_2015['Region'].unique()]

# --------------------------------------
app.layout = html.Div(children=[
    navbar, # and add them to the layout

    dbc.Container(children=[
        dbc.Row(children=[
            html.H1("Philippine Waste Management"),
        ],
            style={'margin': '30px'}),
        dbc.Row([
            dbc.Col([
                html.Label("Select a Year:"),
                dcc.Slider(
                    id='my-slider',
                    min=2015,
                    max=2022,
                    step=1,
                    value=2015,
                    marks={year: {'label': str(year)} for year in range(2015, 2023)}
                ),
            ], width=9),
            dbc.Col([
                html.Label("Select a Region:"),
                dcc.Dropdown(
                    id='region-select-dropdown',
                    options=region_options,
                    value=region_options[0]['value']  # Default to first region
                ),
            ], width=3),
        ], style={'margin': '30px'}), 
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H1(id="waste-generated", className="card-text", style={'text-align': 'center', 'font-weight': 'bold'}),
                        html.P("Waste Generated (KG)", className="card-title", style={'text-align': 'center'})
                    ])
                ], color="danger", inverse=True)
            ], width=4),
            dbc.Col(children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H1(id="waste-facilities", className="card-text", style={'text-align': 'center', 'font-weight': 'bold'}),
                        html.P("Waste Disposal Facilities", className="card-title", style={'text-align': 'center'})
                    ])
                ], color="success", inverse=True)
            ], width=4),
            dbc.Col(children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H1(id="average-population-density", className="card-text", style={'text-align': 'center', 'font-weight': 'bold'}),
                        html.P("Average Population Density", className="card-title", style={'text-align': 'center'})
                    ])
                ], color="primary", inverse=True)
            ], width=4)
        ],
            style={'margin': '30px'}),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id='column-select-dropdown',
                    options=dropdown_options,
                    value=dropdown_options[0]['value']  # Default value
                ),
                dcc.Graph(id='choropleth-map'),
            ])
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='stacked-bar-chart'), width=6),
            dbc.Col(dcc.Graph(id='area-chart'), width=6)
        ],
            style={'margin': '30px'})

    ])
])

# -------------------------------------
# Waste Generated - Callback/Function
@callback(
    Output('waste-generated', 'children'),
    [Input('my-slider', 'value'), 
     Input('region-select-dropdown', 'value')]
)
def update_waste_generated(selected_year, selected_region):
    dataset = pd.read_csv(new_waste_dataset_folder / f'{selected_year}.csv')
    waste_filtered = [col for col in waste_columns if col in dataset.columns]
    dataset[waste_filtered] = dataset[waste_filtered].apply(pd.to_numeric, errors='coerce')

    if selected_region:
        region_data = dataset.loc[dataset['Region'] == selected_region]
        waste_generated = region_data[waste_filtered].sum().sum()
    else:
        waste_generated = dataset.iloc[2:, :][waste_filtered].sum().sum()
    
    if waste_generated == 0:
        formatted_waste_generated = "No Data"
    else:
        formatted_waste_generated = "{:,}".format(int(waste_generated))
    
    return formatted_waste_generated

# -------------------------------------
# Waste Facilities - Callback/Function
@callback(
    Output('waste-facilities', 'children'),
    [Input('my-slider', 'value'), 
     Input('region-select-dropdown', 'value')]
)
def update_waste_facilities(selected_year, selected_region):

    dataset = pd.read_csv(new_waste_dataset_folder / f'{selected_year}.csv')    
    faci_filtered = [col for col in faci_columns if col in dataset.columns]
    dataset[faci_filtered] = dataset[faci_filtered].apply(pd.to_numeric, errors='coerce')

    if selected_region:
        region_data = dataset.loc[dataset['Region'] == selected_region]
        waste_facilities = region_data[faci_filtered].sum().sum()
    else:
        waste_facilities = dataset.iloc[2:, :][faci_filtered].sum().sum()

    if waste_facilities == 0:
        formatted_waste_facilities = "No Data"
    else:
        formatted_waste_facilities = "{:,}".format(int(waste_facilities))
    
    return formatted_waste_facilities

# -------------------------------------
# average population density - Callback/Function
@callback(
    Output('average-population-density', 'children'),
    [Input('my-slider', 'value'), 
     Input('region-select-dropdown', 'value')]
)
def update_average_population_density(selected_year, selected_region):
    dataset = pd.read_csv(new_waste_dataset_folder / f'{selected_year}.csv')
    population_column_index = 22 # 23 regions

    if selected_region:
        region_data = dataset.loc[dataset['Region'] == selected_region]
        total_population = region_data.iloc[:, population_column_index].sum()  
        population_equivalent = total_population
    else:
        total_population = dataset.iloc[2:, population_column_index].sum()  
        population_equivalent = total_population / 17

    formatted_population_equivalent = "{:,}".format(int(population_equivalent))
    
    return formatted_population_equivalent

# -------------------------------------
# Choropleth - Callback/Function
@callback(
    Output('choropleth-map', 'figure'),
    [Input('column-select-dropdown', 'value'),
     Input('my-slider', 'value')]  # Add the slider as an input
) 
def update_map(selected_column, selected_year):
    gdf_selected_year = geojson_data[selected_year]

    if selected_column == "Hazardous Waste Per Capita":
        hover_data = ["Region", "Hazardous Waste Per Capita"]
    elif selected_column == "Total Hazardous Wastes":
        hover_data = ["Region", "Total Hazardous Wastes"]
    elif selected_column == "Total Disposal Facilities":
        hover_data = ["Region", "Illegal Dumpsites", "Materials Recovery Facility", "Sanitary Landfill", "Registered TSD Facilities"]

    fig = px.choropleth_mapbox(gdf_selected_year,
                               geojson=gdf_selected_year.geometry.__geo_interface__,
                               locations=gdf_selected_year.index,
                               color=selected_column,
                               hover_data=hover_data,
                               center={"lat": 12.8797, "lon": 121.7740}, 
                               mapbox_style="carto-positron",
                               zoom=4)
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    return fig

# -------------------------------------
# Stacked Bar/Area Chart - Callback/Function
@callback(
    [Output('stacked-bar-chart', 'figure'),
     Output('area-chart', 'figure')],
    [Input('region-select-dropdown', 'value')]
)
def update_charts(selected_region):
    # Stacked Bar Chart

    # Treated DF
    target_region = selected_region

    yearly_data_for_region = []

    for year, df in datasets_by_year.items():
        treated_waste = df.loc[df['Region'] == target_region, 'Total Treated Hazardous Wastes'].sum()
        yearly_data_for_region.append((year, treated_waste))

    treated_df = pd.DataFrame(yearly_data_for_region, columns=['Year', 'Total Treated Hazardous Wastes'])

    # Hazardous DF
    target_region = 'Philippines'

    yearly_data_for_region = []

    for year, df in datasets_by_year.items():
        hazardous_waste = df.loc[df['Region'] == target_region, 'Total Hazardous Wastes'].sum()
        yearly_data_for_region.append(( hazardous_waste))

    hazardous_df = pd.DataFrame(yearly_data_for_region, columns=[ 'Total Hazardous Wastes'])

    #Concatinate treated and total hazardous waste
    wastes_combined = pd.concat([treated_df, hazardous_df], axis = 1)

    # Name columns
    wastes_combined.columns = ['Year', 'Total Treated Hazardous Wastes', 'Total Hazardous Wastes']

    #Convert to appropriate data types
    wastes_combined['Total Treated Hazardous Wastes'] = pd.to_numeric(wastes_combined['Total Treated Hazardous Wastes'])
    wastes_combined['Total Hazardous Wastes'] = pd.to_numeric(wastes_combined['Total Hazardous Wastes'])

    # Generate the stacked bar chart for all years
    fig_bar = px.bar(wastes_combined, 
                     x='Year', 
                     y=['Total Treated Hazardous Wastes', 'Total Hazardous Wastes'],
                     title="Waste Management Overview",
                     labels={"value": "Volume", "variable": "Waste Type"},
                     barmode='group')

    # Generate the area chart for all years
    fig_area = px.area(wastes_combined, 
                       x='Year', 
                       y=['Total Treated Hazardous Wastes', 'Total Hazardous Wastes'],
                       title="Waste Management Trends",
                       labels={"value": "Volume", "variable": "Waste Type"})

    return fig_bar, fig_area

# -------------------------------------
# Pie Chart - Callback/Function

@callback(
    Output('pie-chart', 'figure'),
    [Input('region-select-dropdown', 'value'),
     Input('my-slider', 'value')])

def update_pie_chart(target_region = 'Philippines', target_year = 2015):
    df = datasets_by_year[target_year]
    filtered_df = df.loc[df['Region'] == target_region]
    waste_types_df = filtered_df[['Wastes with Cyanide', 'Acid Wastes', 'Alkali Wastes', 'Wastes with Inorganic Chemicals', 'Reactive Chemical Wastes', 'Inks/Dyes/Pigments/Paint/Latex/Adhesives/Organic Sludge', 'Waste Organic Solvents', 'Organic Wastes', 'Oil', 'Containers', 'Stabilized Wastes', 'Organic Chemicals', 'Miscellaneous Wastes']]
    waste_types_counts = waste_types_df.sum()

    waste_types_counts_df = pd.DataFrame({'Waste Type': waste_types_counts.index, 'Count': waste_types_counts.values})

    return px.pie(waste_types_counts_df, values='Count', names='Waste Type', title=f'Distribution of Treated Hazardous Waste Types in {target_region}, {target_year}')

if __name__ == '__main__':
    app.run(debug=True)