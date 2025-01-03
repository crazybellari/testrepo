# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[html.H1("SpaceX Launch Records Dashboard",
                                        style={'textAlign': 'center', 'color' : '#503D36',
                                                'font-size' : 30}),
                                                

                                               
                             #TASK 1: Add a Launch Site Drop-down Input Component                    
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                ],
                                value='ALL',
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),
                                html.Br(),

                                # Add pie chart to show successful launches
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a Range Slider to Select Payload
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                value=[min_payload, max_payload]),
                                
                                # Add scatter chart to show payload vs launch outcome
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2: Add a callback function to render success-pie-chart based on selected site dropdown
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site_dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',
        names='Launch Site',
        title='Total Success Launches by Launch Site')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==entered_site]
        filtered_df = filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count',
        names='class',
        title='Total Success Launches for Site "{entered_site}"')
        return fig


# TASK 4: Add a callback function to render the success-payload-scatter-chart scatter plot
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
             [Input(component_id='site_dropdown',component_property='value'),
             Input(component_id='payload-slider',component_property='value')])
def get_payload_chart (entered_site, entered_payload):
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])],
                x="Payload Mass (kg)",
                y="Class",
                color="Booster Version Category",
                hover_data=['Launch Site'],
                title='Correlation Between Payload and Mission Outcomes for All Sites')
                return fig
    else:
        df = spacex_df[spacex_df['Launch Site']==str(entered_site)]
        fig = px.scatter(df[df['Payload Mass (kg)'].between(payload_mass[0], payload_mass[1])],
                x="Payload Mass (kg)",
                y="Class",
                color="Booster Version Category",
                hover_data=['Launch Site'],
                title='Correlation Between Payload and Mission Outcomes for Site "{entered_site}"')
                return fig

# Run the app
if __name__ == '__main__':
    app.run_server()