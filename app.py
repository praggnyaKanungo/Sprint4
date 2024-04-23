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
df = pd.read_csv("data/co2_per_capita.csv")
data = pd.read_csv("data/co2_per_capita.csv")

# I will start by initializing the Dash app
app = dash.Dash(__name__)  # This is for creating a Dash application
server = app.server
app.title = "CO2 Emissions Per Capita Analysis"
# This is my block for the App layout
# this is for defining the HTML layout using Dash HTML components
app.layout = html.Div([
    # This is the header for the title of the dashboard
    html.H1("CO2 Emissions Per Capita Over Time and Distribution", style={'text-align': 'center'}),
    
    # This is the paragraph for the dashboard's introductory text (in this i am just explaining what i've done for this sprint!)
    html.P("This dashboard helps users see the huge increase in CO2 levels. With further development of this dashboard, "
           "there will be different modes such as the following: 'worldview' where you see a line graph with all the "
           "different countries and their CO2 emissions throughout the years (the years are customizable with a slider) "
           "and also a Histogram for the distribution of CO2 emission per capita data (regardless of country or year) on "
           "the worldview mode to show the users numerically what the CO2 emissions per capita data tends to be (more "
           "frequent measurements vs least frequent measurements) so they can see how frequently high CO2 emissions per "
           "capita are recorded; then 'single country view' where you can see a country of your choice's individual CO2 "
           "emissions data over the years (the years are customizable with a slider) in a line graph with some written "
           "basic information about the country on the right, along with a box and whiskers plot that shows the "
           "distribution of the CO2 Emissions per capita data of this country; then 'multiple country view' where users "
           "can select multiple countries and view their CO2 emissions per capita over the year (the years are customizable) "
           "on a line graph, and on the side the dashboard will display the country with the lowest CO2 emissions in a year "
           "and the country with the highest CO2 emission per capita in a year, and also there will be a Violin plot to "
           "compare the distributions of CO2 Emissions per capita data for different countries (the same countries that will "
           "be displayed on the line graph in multiple country view); finally, there will also be a 'year view' where users "
           "can pick a year and see all the country CO2 emissions per capita for that year displayed in a bar graph. "
           "This current version of this dashboard has implemented the graphs for Single Country View Mode!",
           style={'margin': '10px 20px', 'textAlign': 'justify'}),
    
    # This is a sub-header for the single country mode description
    html.H2("Single Country View Mode", style={'text-align': 'center'}),
    
    # This is just a paragraph explaining the single country mode
   html.P("This mode is one of four modes! In this mode, the user can properly analyze the CO2 Emissions Per Capita Data "
           "of a selected country with the help of a line graph and a box and whiskers plot. The user can choose the "
           "country using the dropdown and the range of years using the slider.",
           style={'textAlign': 'center', 'margin-bottom': '20px'}),
    
    # Here i am doing a container Div for dropdown and rangeslider
    html.Div([
        # First Div is for the country dropdown
        html.Div([
            # Here is the dropdown component for selecting the country
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in data['country'].unique()],
                value='USA',  # I've just made the USA the default value for dropdown
                style={'width': '48%', 'display': 'inline-block'}
            )
        ], style={'display': 'inline-block', 'width': '48%'}),
        
        #This div is for the year rangeslider
        html.Div([
            # This is the rangeSlider component for selecting the year range
            dcc.RangeSlider(
                id='year-slider',
                min=data['year'].min(),
                max=data['year'].max(),
                step=1,
                marks={str(year): str(year) for year in range(data['year'].min(), data['year'].max()+1, 10)},
                value=[data['year'].min(), data['year'].max()],
            )
        ], style={'display': 'inline-block', 'width': '48%', 'paddingLeft': '20px'})  # Here I am jsut carefully styling for RangeSlider wrapper
    ], style={'padding': '10px', 'display': 'flex', 'justify-content': 'space-between'}),
    
    # Here is the container Div for graphs
    html.Div([
        # Here my first div for the line graph
        html.Div([
            dcc.Graph(id='line-graph'),  # I am trying to make a line graph
        ], style={'flex': '1', 'paddingRight': '5px'}),  # This is just the style for line graph container
        
        # Here is my second div for the box plot
        html.Div([
            dcc.Graph(id='box-plot'),  # I am trying to make a box plot
        ], style={'flex': '1', 'paddingLeft': '5px'})  # This is just for the style for box plot container
    ], style={'display': 'flex', 'justify-content': 'space-around'})
], style={'textAlign': 'center', 'width': '100%'})  #Just adding some style component for the main div
# From here onwards I am writing the callback function to update the graphs based on the dropdown and slider inputs
@app.callback(
    [Output('line-graph', 'figure'),  # For the Output for the line graph
     Output('box-plot', 'figure')],  # For the Output for the box plot
    [Input('country-dropdown', 'value'),  #For the Input from the country dropdown
     Input('year-slider', 'value')]  # For the Input from the year RangeSlider
)
def update_graphs(selected_country, year_range):
    # I am first filtering the data based on the selected country and year range
    filtered_data = data[(data['country'] == selected_country) &
                         (data['year'] >= year_range[0]) &
                         (data['year'] <= year_range[1])]
    
    # Then I am obviously creating the line graph with the filtered data
    line_fig = px.line(
        filtered_data, 
        x="year", 
        y="co2_per_capita", 
        title=f"CO2 Emissions Per Capita in {selected_country}"
    )
    # I will now be updating the layout of the line graph
    line_fig.update_layout(
        xaxis_title="Year",
        yaxis_title="CO2 Emissions Per Capita",
        margin={'l': 40, 'b': 40, 't': 40, 'r': 20},  # This is just some extra code to adjust margins to avoid cutoff
        height=400  # Just makiing sure the height matches box plot
    )
    # I will not create the box plot with my filtered data
    box_fig = px.box(
        filtered_data, 
        y="co2_per_capita", 
        title=f"Distribution of CO2 Emissions Per Capita in {selected_country}"
    )
    # Now i am updating update the layout of the box plot
    box_fig.update_layout(
        yaxis_title="CO2 Emissions Per Capita",
        margin={'l': 40, 'b': 40, 't': 40, 'r': 20},  # This is just some extra code to adjust margins to avoid cutoff
        height=400  # Just makiing sure the height matches box plot
    )
    # Now, finally I am returniong both figures
    return line_fig, box_fig
# YAY!!! Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
