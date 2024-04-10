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

data_years = range(2015, 2023)
geojson_data = {}
for year in data_years:
    geojson_data[year] = gpd.read_file(geojson_dataset_folder / f'{year}_gdf.geojson', driver='GeoJSON')

# --------------------------------------

# Initializing your Dash application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# You can make variables for your components / sections
navbar = dbc.NavbarSimple(
    # children=[
    #     dbc.NavItem(dbc.NavLink("Home", href="#")),
    # ],
    brand="DATA101 DASHBOARD",
    brand_href="#",
    color="black",
    dark=True,
)

# Choropleth - Dropdown
dropdown_options = [
    {'label': 'Total Hazardous Wastes', 'value': 'Total Hazardous Wastes'},
    {'label': 'Hazardous Waste Per Capita', 'value': 'Hazardous Waste Per Capita'},
    {'label': 'Total Disposal Facilities', 'value': 'Total Disposal Facilities'}
]

# Region - Dropdown

region_options = [{'label': region, 'value': region} for region in new_data_2015['Region'].unique()]

# --------------------------------------

app.layout = html.Div(children=[
    navbar, # Left Image
    html.Div(children=[
        # Left Sidebar
        # html.Div(children=[
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        # ], className="left"),

        # # Right Sidebar
        # html.Div(children=[
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        #     html.Div(html.Img(src='/assets/garbage.png')),
        # ], className="right"),

        # Visualizations
        dbc.Container(children=[
            dbc.Row(children=[
                html.H1("PHILIPPINES' WASTE MANAGEMENT", className="text-center",
                        style={
                        'textAlign': 'center',
                        'color': 'black',
                        'fontFamily': 'Roboto, sans-serif',
                        'fontWeight': 'bold',
                        'fontSize': '100px',
                        'marginBottom':'30px'
                    }),
                html.P("In the heart of Southeast Asia, the Philippines grapples with significant waste management challenges. With over 7,000 islands and a population exceeding 100 million, effective waste management is crucial. Our dashboard, focused on Philippines' Waste Management, aims to provide insight into the current state of affairs. We'll highlight the generated waste and facilities of the regions in the country. Join us as we delve into the practicalities of waste management in the Philippines, striving for a cleaner, more sustainable future.")],
                style={'margin': '50px'}),

            # Time Slider & Region Dropdown ----------------------------
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
            ],style={
                'position': 'sticky',
                'top': '0',
                'zIndex': '1020',
                'background': '#f8f9fa',  # Light grey background
                'boxShadow': '0px 2px 2px lightgrey',  # Adds shadow to the bottom of the row
                'paddingTop': '10px',  
                'paddingBottom': '10px', 
                'marginBottom': '50px'
            }),

            # Key Cards -------------------------------
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="waste-generated", className="card-text text-center", style={'fontSize': '40px'}),
                            html.P("Total Waste Generated (ton)", className="card-title text-center", style={'fontSize': '20px'}),
                        ])
                    ], color="danger", inverse=True)
                ], width=4),
                dbc.Col(children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="waste-facilities", className="card-text text-center", style={'fontSize': '40px'}),
                            html.P("Waste Disposal Facilities", className="card-title text-center", style={'fontSize': '20px'}),
                        ])
                    ], color="success", inverse=True)
                ], width=4),
                dbc.Col(children=[
                    dbc.Card([
                        dbc.CardBody([
                            html.H4(id="average-population-density", className="card-text text-center", style={'fontSize': '40px'}),
                            html.P("Average Population Density", className="card-title text-center", style={'fontSize': '20px'}),
                        ])
                    ], color="primary", inverse=True)
                ], width=4)
            ],
                style={'margin': '30px'}),

            # Line Graph -------------------------------
            dbc.Row([
                dbc.Col([
                    html.H2(id="line-title", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'Roboto, sans-serif', 'fontWeight': 'bold', 'marginTop': '20px'}),
                    dcc.Graph(id='line-graph-hazardous-wastes', style={'height': '400px'}),
                    html.P("Explore the dynamic landscape of hazardous waste management in the region you've selected through the Total Hazardous Wastes line chart. This visual representation tracks the trends in hazardous waste generation over time, providing valuable insights into the nation's environmental policies and practices. The x-axis denotes the years, offering a chronological view, while the y-axis quantifies the total hazardous waste generated, allowing for a clear understanding of the scale of waste management challenges. The chart's distinct blue color (#48C3FC) ensures easy readability and interpretation of the data. By delving into this chart, stakeholders can uncover patterns, identify areas for improvement, and make informed decisions towards a more sustainable future for the Philippines.")
                    ])
            ], style={'margin': '30px'}),

            # Choropleth Map & Stacked Area Chart--------------------------
            dbc.Row([
                dbc.Col([
                    html.H2(id="chor-title", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'Roboto, sans-serif', 'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='column-select-dropdown',
                        options=dropdown_options,
                        value=dropdown_options[0]['value'],
                        style={'marginBottom': '10px'}  # Default value
                    ),
                    dcc.Graph(id='choropleth-map'),
                    html.P("Explore the spatial distribution of hazardous waste management across the Philippines with our interactive Choropleth Map. This powerful visualization provides a comprehensive overview of the total amount of hazardous waste, and waste per capita per region, alongside key metrics such as the number of illegal dumpsites, Material Recovery Facilities (MRF), sanitary landfills, and registered Treatment, Storage, and Disposal (TSD) facilities. With the ability to toggle between Total Hazardous Wastes, Total Hazardous Wastes per Capita, and Total Waste Disposal Facilities using a dropdown menu, alongside a time slider for historical analysis, users can gain valuable insights into the spatial patterns and trends of waste management practices throughout the Philippines.", style={'marginTop': '30px'})
                    ]),
                dbc.Col([
                    html.H2(id="area-title", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'Roboto, sans-serif', 'fontWeight': 'bold'}),
                    dbc.Row([
                        # dbc.Col(dcc.Graph(id='stacked-bar-chart'), width=6),
                        dbc.Col(dcc.Graph(id='area-chart')),
                    html.P("Gain insights into the treatment efficacy of hazardous waste over the years in our Stacked Area Chart. This visualization compares the ratio of total treated hazardous waste to total generated hazardous waste, spanning from 2015 to 2022. By examining the stacked areas, users can discern trends and similarities in treatment effectiveness over time, enabling informed decision-making for sustainable waste management practices.", style={'marginTop': '30px'})])
                ])
            ],
                style={'margin': '30px'}),



            # Pie Chart -------------------------------
            dbc.Row([
                html.H2(id="pie-title", style={'textAlign': 'center', 'color': 'black', 'fontFamily': 'Roboto, sans-serif', 'fontWeight': 'bold', 'marginTop': '20px'}),
                dcc.Graph(id='waste-types-pie-chart'),
                html.P("Explore the composition of hazardous waste by region through our informative Pie Chart. Each segment of the chart represents a different type of hazardous waste, categorized by color for easy identification. From wastes containing cyanide to organic chemicals, and miscellaneous wastes, this visualization provides a clear depiction of the part-to-whole relationship within each region. Delve into the chart to understand the distribution of various hazardous waste types across different regions, empowering stakeholders to make informed decisions for effective waste management strategies.")
            ], style={'marginBottom': '30px'})

        ])
        ],
        style={
            'position': 'relative',
            'padding': '0',
            'margin': '0',
    }),
    
])


# -------------------------------------
# Key Cards - Callback/Function

@callback(
    Output('waste-generated', 'children'),
    Output('waste-facilities', 'children'),
    Output('average-population-density', 'children'),
    [Input('my-slider', 'value'),
     Input('region-select-dropdown', 'value')] 
)

def update_metrics(selected_year, selected_region):
    df_selected_year = datasets_by_year[selected_year]
    filtered_df = df_selected_year[df_selected_year['Region'] == selected_region]

    filtered_df['Total Hazardous Wastes'] = pd.to_numeric(filtered_df['Total Hazardous Wastes'], errors='coerce')
    filtered_df['Illegal Dumpsites'] = pd.to_numeric(filtered_df['Illegal Dumpsites'])
    filtered_df['Materials Recovery Facility'] = pd.to_numeric(filtered_df['Materials Recovery Facility'])
    filtered_df['Sanitary Landfill'] = pd.to_numeric(filtered_df['Sanitary Landfill'])
    filtered_df['Registered TSD Facilities'] = pd.to_numeric(filtered_df['Registered TSD Facilities'])
    filtered_df['Population'] = pd.to_numeric(filtered_df['Population'], errors='coerce')

    total_waste = filtered_df['Total Hazardous Wastes'].sum()
    waste_facilities = filtered_df[['Illegal Dumpsites', 'Materials Recovery Facility', 'Sanitary Landfill', 'Registered TSD Facilities']].sum().sum()
    average_population_density = filtered_df['Population'].mean()

    # Using str.format()
    # Adding comma between numbers
    try:
        total_waste_numeric = float(total_waste)
        tw = '{:,.2f}'.format(total_waste_numeric)
    except ValueError:
        tw = "Invalid value"

    try:
        waste_facilities_numeric = float(waste_facilities)
        wf = ('{:,.0f}'.format(waste_facilities_numeric))
    except ValueError:
        wf = "Invalid value"

    try:
        apd_numeric = float(average_population_density)
        apd = ('{:,.0f}'.format(apd_numeric))
    except ValueError:
        apd = "Invalid value"

    # Format the results as strings
    return f"{tw}", f"{wf}", f"{apd}"

# ---------------------------------------------
# Line Graph - Callback/Function

@app.callback(
    Output('line-graph-hazardous-wastes', 'figure'),
    Output('line-title', 'children'),
    [Input('region-select-dropdown', 'value')]
)
def update_line_graph(selected_region):

    target_region = selected_region

    yearly_data_for_region = []

    for year, df in datasets_by_year.items():
        total_waste = df.loc[df['Region'] == target_region, 'Total Hazardous Wastes'].sum()
        yearly_data_for_region.append((year, total_waste))

    # Convert the list to a DataFrame for easier plotting
    region_df = pd.DataFrame(yearly_data_for_region, columns=['Year', 'Total Hazardous Wastes'])

    region_df['Total Hazardous Wastes'] = pd.to_numeric(region_df['Total Hazardous Wastes'])

    fig = px.line(region_df, x='Year', y='Total Hazardous Wastes')

    lineTitle = f'Total Hazardous Wastes for {selected_region}'

    return fig, lineTitle

# -------------------------------------
# Choropleth - Callback/Function
@callback(
    Output('choropleth-map', 'figure'),
    Output('chor-title', 'children'),
    [Input('column-select-dropdown', 'value'),
     Input('my-slider', 'value')]  # Add the slider as an input
)
def update_map(selected_column, selected_year):
    gdf_selected_year = geojson_data[selected_year]

    gdf_selected_year.fillna('N/A', inplace=True)

    # Mapping from column names to color scales
    color_scales_mapping = {
        'Hazardous Waste Per Capita': px.colors.sequential.Blues,
        'Total Hazardous Wastes': px.colors.sequential.Oranges,
        'Total Disposal Facilities': px.colors.sequential.Greens,
    }

    hover_data_mapping = {
        "Hazardous Waste Per Capita": ["Region", "Hazardous Waste Per Capita"],
        "Total Hazardous Wastes": ["Region", "Total Hazardous Wastes"],
        "Total Disposal Facilities": ["Region", "Illegal Dumpsites", "Materials Recovery Facility", "Sanitary Landfill", "Registered TSD Facilities"]
    }

    hover_data = hover_data_mapping[selected_column]
    color_scale = color_scales_mapping[selected_column]

    fig = px.choropleth_mapbox(gdf_selected_year,
                               geojson=gdf_selected_year.geometry.__geo_interface__,
                               locations=gdf_selected_year.index,
                               color=selected_column,
                               hover_data=hover_data,
                               center={"lat": 12.8797, "lon": 121.7740},
                               mapbox_style="carto-positron",
                               zoom=4,
                               color_continuous_scale=color_scale
                               )
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})

    fig.update_layout(coloraxis_colorbar_title_text='')


    chorTitle = f'{selected_column} for {selected_year}'

    return fig, chorTitle

# -------------------------------------
# Stacked Bar/Area Chart - Callback/Function
@callback(

        # Output('stacked-bar-chart', 'figure'),
     Output('area-chart', 'figure'),
    Output('area-title', 'children'),
    [Input('region-select-dropdown', 'value')]
)
def update_charts(selected_region):

    # Treated DF
    target_region = selected_region

    yearly_data_for_region = []

    for year, df in datasets_by_year.items():
        treated_waste = df.loc[df['Region'] == target_region, 'Total Treated Hazardous Wastes'].sum()
        yearly_data_for_region.append((year, treated_waste))

    treated_df = pd.DataFrame(yearly_data_for_region, columns=['Year', 'Total Treated Hazardous Wastes'])

    # Hazardous DF

    yearly_data_for_region = []

    for year, df in datasets_by_year.items():
        hazardous_waste = df.loc[df['Region'] == target_region, 'Total Hazardous Wastes'].sum()
        yearly_data_for_region.append(( hazardous_waste))

    hazardous_df = pd.DataFrame(yearly_data_for_region, columns=[ 'Total Hazardous Wastes'])

    #Concatenate treated and total hazardous waste
    wastes_combined = pd.concat([treated_df, hazardous_df], axis = 1)

    wastes_combined.columns = ['Year', 'Total Treated Hazardous Wastes', 'Total Hazardous Wastes']

    wastes_combined['Total Treated Hazardous Wastes'] = pd.to_numeric(wastes_combined['Total Treated Hazardous Wastes'])
    wastes_combined['Total Hazardous Wastes'] = pd.to_numeric(wastes_combined['Total Hazardous Wastes'])

    # Stacked bar chart
    # fig_bar = px.bar(wastes_combined,
    #                  x='Year',
    #                  y=['Total Treated Hazardous Wastes', 'Total Hazardous Wastes'],
    #                  title="Waste Management Overview",
    #                  labels={"value": "Volume", "variable": "Waste Type"},
    #                  barmode='group')

    # Stacked area chart 
    fig_area = px.area(wastes_combined,
                       x='Year',
                       y=['Total Treated Hazardous Wastes', 'Total Hazardous Wastes'],
                       labels={"value": "Volume", "variable": "Waste Type"})

    # Horizontal legend
    fig_area.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.2,  # You might need to adjust this value to better suit your layout
            xanchor="center",
            x=0.5
        )
    )

    areaTitle = f"Waste Management Trends for {selected_region}"

    return fig_area, areaTitle #fig_bar,

# -----------------------------------------
# Pie Chart - Callback/Function

@app.callback(
    Output('waste-types-pie-chart', 'figure'),
    Output('pie-title', 'children'),
    [Input('my-slider', 'value'),
     Input('region-select-dropdown', 'value')]
)
def update_pie_chart(selected_year, selected_region):
    df_selected_year = datasets_by_year[selected_year]

    df_filtered = df_selected_year[df_selected_year['Region'] == selected_region]

    # extract only the waste columns 
    waste_columns = df_filtered.columns[
                    df_filtered.columns.get_loc('Wastes with Cyanide'):df_filtered.columns.get_loc('Miscellaneous Wastes')+1]

    # Convert the waste data columns to numeric
    df_filtered[waste_columns] = df_filtered[waste_columns].applymap(pd.to_numeric, errors='coerce')

    waste_data = df_filtered[waste_columns].sum()

    category_colors = {
        'Wastes with Cyanide': '#E69F00',  # Orange
        'Acid Wastes': '#56B4E9',  # Sky Blue
        'Alkali Wastes': '#009E73',  # Bluish Green
        'Wastes with Inorganic Chemicals': '#F0E442',  # Bright Yellow
        'Reactive Chemical Wastes': '#0072B2',  # Blue
        'Inks/Dyes/Pigments/Paint/Latex/Adhesives/Organic Sludge': '#D55E00',  # Vermilion
        'Waste Organic Solvents': '#CC79A7',  # Reddish Purple
        'Organic Wastes': '#999999',  # Grey
        'Oil': '#000000',  # Black
        'Containers': '#BBBBBB',  # Light Gray
        'Stabilized Wastes': '#000075',  # Dark Blue
        'Organic Chemicals': '#A9A9A9',  # Dark Gray
        'Miscellaneous Wastes': '#FBFCF8',  # White
    }


    # DataFrame for plotting
    plot_data = pd.DataFrame({'Waste Type': waste_data.index, 'Amount': waste_data.values})

    # Map colors
    plot_data['Color'] = plot_data['Waste Type'].map(category_colors)

    # default color for missing
    default_color = '#808080'  # Gray as default
    plot_data['Color'].fillna(default_color, inplace=True)

    fig = px.pie(
        plot_data,
        names='Waste Type',
        values='Amount',
        color='Waste Type',
        color_discrete_map=category_colors
    )

    fig.update_layout(legend_title_text='Waste Types')

    pieTitle = f'Types of Waste for {selected_region} in {selected_year}'

    return fig, pieTitle



if __name__ == '__main__':
    app.run(debug=True)