#Praggnya Kanungo
#DS 4003
#Sprint 4

# First I need to import necessary libraries
import dash  # This is obviously the Dash framework for creating web applications
from dash import dcc, html  # Here I am importing the components for interactive components and HTML layout
from dash.dependencies import Input, Output  # This is what i am importing for my callbacks
import plotly.express as px  # Because i am depending on graphs and i am importing plotly for creating the plotly graphs
import pandas as pd  # This is in case I need to manipulate some data for the graph

# First iam just making a data_path for loading my data
# here I am defining the path to the data file
# I am reading the data into a pandas DataFrame
data = pd.read_csv("data/co2_per_capita.csv")

# I will start by initializing the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.title = "CO2 Emissions Per Capita Analysis"
# This is my block for the App layout
# this is for defining the HTML layout using Dash HTML components

# Load the data


# Define initial layout with all potential components
app.layout = html.Div([
    html.H1("CO2 Emissions Per Capita Dashboard", style={'text-align': 'center'}),

    dcc.RadioItems(
        id='mode-selector',
        options=[
            {'label': 'Worldview', 'value': 'worldview'},
            {'label': 'Single Country View', 'value': 'single_country'},
            {'label': 'Multiple Country View', 'value': 'multiple_country'},
            {'label': 'Year View', 'value': 'year_view'}
        ],
        value='worldview',
        labelStyle={'display': 'inline-block', 'margin-right': '20px'}
    ),

    html.Div(id='mode-display'),  # Container for dynamic content

    # Include all components with correct IDs in initial layout
    dcc.Graph(id='worldview-line-graph', style={'display': 'none'}),
    dcc.Graph(id='worldview-histogram', style={'display': 'none'}),
    dcc.Graph(id='line-graph', style={'display': 'none'}),
    dcc.Graph(id='box-plot', style={'display': 'none'}),
    dcc.Graph(id='multi-country-line-graph', style={'display': 'none'}),
    dcc.Graph(id='multi-country-violin-graph', style={'display': 'none'}),
    dcc.Graph(id='year-bar-graph', style={'display': 'none'})
])

# Callback to update mode-display based on selected mode
@app.callback(
    Output('mode-display', 'children'),
    [Input('mode-selector', 'value')]
)
def update_mode(mode):
    if mode == 'worldview':
        return html.Div([
            dcc.RangeSlider(
                id='worldview-year-slider',
                min=data['year'].min(),
                max=data['year'].max(),
                value=[data['year'].min(), data['year'].max()],
                marks={str(year): str(year) for year in range(data['year'].min(), data['year'].max() + 1, 10)},
                step=1
            ),
            dcc.Graph(id='worldview-line-graph'),
            dcc.Graph(id='worldview-histogram')
        ])
    elif mode == 'single_country':
        return html.Div([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in data['country'].unique()],
                value='USA'  # Default country
            ),
            dcc.RangeSlider(
                id='year-slider',
                min=data['year'].min(),
                max=data['year'].max(),
                value=[data['year'].min(), data['year'].max()],
                marks={str(year): str(year) for year in range(data['year'].min(), data['year'].max() + 1, 10)},
                step=1
            ),
            dcc.Graph(id='line-graph'),
            dcc.Graph(id='box-plot')
        ])
    elif mode == 'multiple_country':
        return html.Div([
            dcc.Dropdown(
                id='multiple-country-dropdown',
                multi=True,
                options=[{'label': country, 'value': country} for country in data['country'].unique()],
                value=['USA', 'China']  # Default selected values
            ),
            dcc.RangeSlider(
                id='multiple-year-slider',
                min=data['year'].min(),
                max=data['year'].max(),
                value=[data['year'].min(), data['year'].max()],
                marks={str(year): str(year) for year in range(data['year'].min(), data['year'].max() + 1, 10)},
                step=1
            ),
            dcc.Graph(id='multi-country-line-graph'),
            dcc.Graph(id='multi-country-violin-graph')
        ])
    elif mode == 'year_view':
        return html.Div([
            dcc.Slider(
                id='single-year-slider',
                min=data['year'].min(),
                max=data['year'].max(),
                value=data['year'].max(),
                marks={str(year): str(year) for year in range(data['year'].min(), data['year'].max() + 1, 10)},
                step=1
            ),
            dcc.Graph(id='year-bar-graph')
        ])

# Callback to update graphs based on slider inputs for Worldview
@app.callback(
    [Output('worldview-line-graph', 'figure'),
     Output('worldview-histogram', 'figure')],
    [Input('worldview-year-slider', 'value')]
)
def update_worldview_graphs(year_range):
    filtered_data = data[(data['year'] >= year_range[0]) & (data['year'] <= year_range[1])]
    line_fig = px.line(
        filtered_data, 
        x="year", 
        y="co2_per_capita", 
        color='country',
        title="Global CO2 Emissions Per Capita Over Time"
    )
    histogram_fig = px.histogram(
        filtered_data,
        x="co2_per_capita",
        nbins=50,
        title="Distribution of Global CO2 Emissions Per Capita"
    )
    return line_fig, histogram_fig

# Callback for Single Country View
@app.callback(
    [Output('line-graph', 'figure'),
     Output('box-plot', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('year-slider', 'value')]
)
def update_single_country_graphs(selected_country, year_range):
    filtered_data = data[(data['country'] == selected_country) &
                         (data['year'] >= year_range[0]) &
                         (data['year'] <= year_range[1])]
    line_fig = px.line(
        filtered_data,
        x="year",
        y="co2_per_capita",
        title=f"CO2 Emissions Per Capita in {selected_country}"
    )
    box_fig = px.box(
        filtered_data,
        y="co2_per_capita",
        title=f"Distribution of CO2 Emissions Per Capita in {selected_country}"
    )
    return line_fig, box_fig

# Callback for Multiple Country View
@app.callback(
    [Output('multi-country-line-graph', 'figure'),
     Output('multi-country-violin-graph', 'figure')],
    [Input('multiple-country-dropdown', 'value'),
     Input('multiple-year-slider', 'value')]
)
def update_multi_country_graphs(selected_countries, year_range):
    filtered_data = data[(data['country'].isin(selected_countries)) &
                         (data['year'] >= year_range[0]) &
                         (data['year'] <= year_range[1])]
    line_fig = px.line(
        filtered_data,
        x="year",
        y="co2_per_capita",
        color='country',
        title="CO2 Emissions Per Capita Over Time for Selected Countries"
    )
    violin_fig = px.violin(
        filtered_data,
        y="co2_per_capita",
        box=True,
        color='country',
        title="Distribution of CO2 Emissions Per Capita for Selected Countries"
    )
    return line_fig, violin_fig

# Callback for Year View
@app.callback(
    Output('year-bar-graph', 'figure'),
    [Input('single-year-slider', 'value')]
)
def update_year_graph(selected_year):
    filtered_data = data[data['year'] == selected_year]
    return px.bar(
        filtered_data,
        x="country",
        y="co2_per_capita",
        title=f"CO2 Emissions Per Capita in {selected_year}"
    )

if __name__ == '__main__':
    app.run_server(debug=True)
