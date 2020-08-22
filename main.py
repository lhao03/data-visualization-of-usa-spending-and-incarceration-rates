import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash 
import dash_core_components as dcc
import dash_html_components as html 
from dash.dependencies import Input, Output
from states import state_codes, states_names

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets) 

# import data
df = pd.read_csv("2004-2017_usa_spending.csv")

def make_mappings():
    list_of_labels_vals = []
    list_of_labels_vals.append({"label": "USA", "value": "USA"})
    for i in range(0, len(state_codes)):
        label_dict = {"label": states_names[i]}
        label_dict["value"] = state_codes[i]
        list_of_labels_vals.append(label_dict)
    return list_of_labels_vals

# app layout - components 
app.layout = html.Div([
    html.H1("State General Expenditures, Per Capita in Dollars", style={'text-align':'center', 'font-family': 'sans-serif'}),
    
    # div holding slider 
    html.Div([
        # slider for usa map
        dcc.Slider(id='slct_year', min=2005, max=2017, step=None, marks={
        2005: '2005',
        2006: '2006',
        2007: '2007',
        2008: '2008',
        2009: '2009',
        2010: '2010',
        2011: '2011', 
        2012: '2012',
        2013: '2013',
        2014: '2014',
        2015: '2015',
        2016: '2016',
        2017: '2017'
    }, value=2005),
    
    # drop down for usa map   
        dcc.Dropdown(id='slct_fndng', options=[
        {"label": "Total Spending", "value": "total"},
        {"label": "Elementary and Secondary Education", "value": "elementary_and_secondary_edu"},
        {"label": "Higher Education", "value": "higher_edu"},
        {"label": "Public Welfare", "value": "public_welfare"},
        {"label": "Health and Hospital", "value": "health_and_hospitals"},
        {"label": "Highways", "value": "highways"},
        {"label": "Police", "value": "police"},
        {"label": "Other", "value": "all_other"},
        {"label": "Population", "value": "population_thousands"}], multi=False,
        value="total", style={'width': "70%"}),
         dcc.Graph(id='usa_map', figure={}) 
        
    ], style={
        # 'width': '48%', 
        # 'display': 'inline-block'
        }),

    # div holding graphs that are state specific 
    html.Div([
        dcc.Dropdown(id='slct_state', options=make_mappings()),

        dcc.Graph(id='state_figure', figure={},)], 
        style={
            'width': '95%',
            #  'align': 'right',
              'display': 'inline-block'
    }),
], style={'background-color': '#A4BFEB', 'columnCount': 2})

# connect using the callbacks
@app.callback(
    [Output(component_id='usa_map', component_property='figure'),
    Output(component_id='state_figure', component_property='figure')],
    [Input(component_id='slct_year', component_property='value'),
    Input(component_id='slct_fndng', component_property='value'),
    Input(component_id='slct_state', component_property='value')]
)
def update_graph(year, funding):
    # option_slctd refers to value

    df_copy = df.copy()
    df_year = df_copy[df_copy["year"] == year]

    # year by year     
    fig_usa = px.choropleth(
        data_frame=df_year, 
        locationmode='USA-states',
        locations='status_code',
        scope='usa',
        color=funding,
        color_continuous_scale="Viridis"
    )

    # specific state or compare all of the states by average
    fig_state= make_subplots(rows=3, cols=1,
    subplot_titles=("Plot 1", "Plot 2", "Plot 3", "Plot 4"))

    fig_state.append_trace(go.Scatter(
    x=[3, 4, 5],
    y=[1000, 1100, 1200],
    ), row=1, col=1)

    fig_state.append_trace(go.Scatter(
    x=[2, 3, 4],
    y=[100, 110, 120],
    ), row=2, col=1)

    fig_state.append_trace(go.Scatter(
    x=[0, 1, 2],
    y=[10, 11, 12]
    ), row=3, col=1)

    return [fig_usa, fig_state] # the outputs

# run the app 
if __name__ == "__main__":
    app.run_server(debug=True)