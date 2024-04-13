#%%
# Term Project: Visualization of Auto Insurance Churn dataset
# Name: Brian Kim
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np

external_stylesheets=['https://codepen.io/chriddyp/pen/BWLwgP.css']

# Initialize the Dash app
my_app = dash.Dash('Term_Project', external_stylesheets=external_stylesheets)
server = my_app.server


df = pd.read_csv("/Users/brian/Downloads/GWU/2024 Spring/Visualization_of_complex_data/Term Project/Term Dataset/autoinsurance_churn.csv")
# print(df.info())
# print(df.head(5))
# print(df.describe())
print(df.columns)

#%%
''' Data Preprocessing
'''
# Count Null
df.isna().sum()

#%%
# data checking
# print(df['county'].unique())

#%%
# ===============
# Phase 3
# ===============

my_app.layout = html.Div([
    html.H2('Auto Insurance Customer Churn', style={'textAlign':'center'}),
    dcc.Tabs(id='term', children=[
        dcc.Tab(label='Overview', value='l1'),
        dcc.Tab(label='Demographics Insights', value='l2'),
        dcc.Tab(label='Churn Analysis', value='l3'),
        dcc.Tab(label='Geographic Analysis', value='l4'),
    ]),
    html.Div(id='layout')
])

# ====================
# Question 1 layout
# ====================

l1_layout = html.Div([
    html.Img(src='/assets/cover.png',
             style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Br(),

]
)

# question1_layout = html.Div([
#     html.H5('Select country'),
#     dcc.Dropdown(
#         id='country-dropdown',
#         options=[{'label': country_name, 'value': country_name} for country_name in country],
#         multi=True,
#         placeholder='Select Country...'
#     ),
#     dcc.Graph(id='covid-graph')
# ], style={'width': '30%'})
#
# # Callback for updating the Covid graph
# @my_app.callback(Output('covid-graph', 'figure'),
#                  [Input('country-dropdown', 'value')])
# def update_graph(selected_countries):
#     if not selected_countries:
#         return px.line()
#
#     fig = px.line(df3[selected_countries], x=df4.year_2, y=selected_countries)
#
#     fig.update_layout(
#         width=1000,
#         xaxis_title="Date",
#         yaxis_title="Confirmed Covid19 Cases",
#         xaxis=dict(
#             tickmode='auto',
#             nticks=20,
#             tickformat="%Y-%b"
#         )
#     )
#
#     return fig







# ====================
# Question 2 layout
# ====================
#%%
'''Data Preprocessing'''
# County - Remove null value
df2 = df.dropna(subset=['county'])
county = df2['county'].unique().tolist()
#
# # Average Income by county
grouped_income = df2.groupby('county')['income'].mean().round(2).reset_index()
print(grouped_income)

# Mapping Churn data
df2['churn_label'] = df2['Churn'].map({1: 'Churn', 0: 'Not Churn'})

#%%
'''Layout2'''
l2_layout = html.Div([
    html.H3('The age distribution of customers'),
    html.H4('Select the county in Texas'),
    dcc.Dropdown(
        id='selected_counties',
        options=[{'label': county_name, 'value': county_name} for county_name in county],
        multi=True,
        placeholder='Select County...'
    ),
    dcc.Graph(id='graph1'),
    html.H4('Bin'),
    dcc.Slider(id="bin_value", min=1, max=100, step=1, value=50,
               marks={i: str(i) for i in range(1, 101, 10)}),
    html.Br(),
    html.Br(),
    html.H3('The average income of customers by county'),
    dcc.Graph(id='graph2'),
])

# Callback to update both graphs based on selected counties and bin size
@my_app.callback(
    [Output('graph1', 'figure'),
     Output('graph2', 'figure')],
    [Input('bin_value', 'value'),
     Input('selected_counties', 'value')]
)
def update_graph(bin_value, selected_counties):
    # Apply county filter for both graphs
    if selected_counties:
        filtered_df = df2[df2['county'].isin(selected_counties)]
    else:
        filtered_df = df2

    fig1 = px.histogram(filtered_df, x='age_in_years', nbins=bin_value, title='Age Distribution')
    fig1.update_layout(xaxis_title='Age', yaxis_title='Count')

    grouped_income = filtered_df.groupby('county')['income'].mean().reset_index()
    fig2 = px.bar(grouped_income, x='county', y='income', title='Average Income by County')
    fig2.update_layout(xaxis_title='County', yaxis_title='Average Income', width=1000)

    return fig1, fig2

# # Age and Income Distribution Layout
# l2_layout = html.Div([
#     html.H3('The age distribution of customers'),
#     dcc.Graph(id='graph1'),
#     html.H4('Bin'),
#     dcc.Slider(id="bin_value", min=1, max=100, step=1, value=50,
#                marks={1: '1', 10: '10', 20: '20', 30: '30', 40: '40', 50: '50', 60: '60', 70: '70', 80: '80', 90: '90',
#                       100: '100'}),
#     html.Br(),
#     html.Br(),
#     html.H3('The average income of customers by county'),
#     html.H4('Select the county in Texas'),
#     dcc.Dropdown(
#         id='selected_counties',
#         options=[{'label': county_name, 'value': county_name} for county_name in county],
#         multi=True,
#         placeholder='Select County...'
#     ),
#     dcc.Graph(id='graph2'),
#
# ])
#
#
# @my_app.callback(
#     [Output(component_id='graph1', component_property='figure'),
#      Output(component_id='graph2', component_property='figure')],
#     [Input(component_id='bin_value', component_property='value'),
#      Input(component_id='selected_counties', component_property='value')]
# )
# def update_graph(bin_value, selected_counties):
#     fig1 = px.histogram(df2, x='age_in_years', nbins=bin_value, title='Age Distribution')
#
#     if selected_counties:
#         filtered_df = df2[df2['county'].isin(selected_counties)]
#         grouped_income = filtered_df.groupby('county')['income'].mean().reset_index()
#         fig2 = px.bar(grouped_income, x='county', y='income', title='Average Income by County')
#     else:
#         fig2 = px.bar(x=[], y=[], title='Select counties to view average income')
#
#     fig1.update_layout(xaxis_title='Age', yaxis_title='Count')
#     fig2.update_layout(xaxis_title='County', yaxis_title='Average Income', width=1000)
#
#     return fig1, fig2

#
# l2_layout = html.Div(children=[
#     html.H3(children='Age distribution and Income boxplot', style={'textAlign':'center'}),
#
#     html.Div(children=[
#         dcc.Graph(
#             id='age-histogram',
#             style={'width': '49%', 'display': 'inline-block'}
#         ),
#         dcc.Graph(
#             id='income-boxplot',
#             style={'width': '49%', 'display': 'inline-block'}
#         )
#     ])
# ])
#
#
# # Callback for updating both the histogram and the box plot
# @my_app.callback(
#     [Output('age-histogram', 'figure'),
#      Output('income-boxplot', 'figure')],
#     [Input('age-histogram', 'id'),
#      Input('income-boxplot', 'id')
#      ]  # Dummy input for initialization
# )
# def update_graphs(_):
#     # Age histogram
#     fig1 = px.histogram(df2, x='age_in_years', title='Age Distribution')
#
#     # Income box plot by churn status
#     fig2 = px.box(df2, x='churn_label', y='income', color='churn_label',
#                   labels={'churn_label': 'Churn Status', 'income': 'Income'},
#                   title='Income Distribution by Churn Status')
#     fig2.update_layout(showlegend=False)
#
#     return fig1, fig2




# ====================
# Question 3 layout
# ====================
'''Data Preprocessing'''
#%%
import pandas as pd

df = pd.read_csv("/Users/brian/Downloads/GWU/2024 Spring/Visualization_of_complex_data/Term Project/Term Dataset/autoinsurance_churn.csv")

# # Mapping data
# df['home_owner'] = df['home_owner'].map({1: 'Owner', 0: 'Not_Owner'})
# df['has_children'] = df['has_children'].map({1: 'Has_children', 0: 'Not_has_children'})

#%%
# print(df['has_children'].head(50))
# print(df['marital_status'].head(50))
# print(df.head(10))

#%%

'''Layout3'''
l3_layout = html.Div([
    html.H3("Select the legend:"),
    dcc.Dropdown(
        id='legend-dropdown',
        options=[
            {'label': 'marital_status', 'value': 'marital_status'},
            {'label': 'home_owner', 'value': 'home_owner'},
            {'label': 'has_children', 'value': 'has_children'}
        ],
        value='marital_status'  # Default value
    ),
    html.Div(id='pie-chart')
])

@my_app.callback(
    Output('pie-chart', 'children'),
    [Input('legend-dropdown', 'value')]
)

def update_pie_chart(legend):
    df_copy = df.copy()
    if legend == 'home_owner':
        df_copy['home_owner'] = df_copy['home_owner'].map({1: 'Owner', 0: 'Not Owner'})
    elif legend == 'has_children':
        df_copy['has_children'] = df_copy['has_children'].map({1: 'Has Children', 0: 'No Children'})
    fig = px.pie(df_copy, values='Churn', names=legend, title=f'Pie Chart of Churn rate by {legend.capitalize()}')

    return dcc.Graph(figure=fig)



# def update_pie_chart(legend):
#     # df_grouped = df.groupby(legend)[predictor].sum().reset_index()
#     fig = px.pie(df, values=df['Churn'], names=legend, title=f'Pie Chart of Churn rate by {legend.capitalize()}')
#     # fig.update_layout(labels = {df['home_owner'].map({1: 'Owner', 0: 'Not_Owner'}),
#     #                            df['has_children'].map({1: 'Has_children', 0: 'Not_has_children'})})
#     return dcc.Graph(figure=fig)



# l3_layout = html.Div([
#     html.H3('Churn Rates by Customer Attributes'),
#     dcc.Tabs(id="tabs", value='tab-1', children=[
#         dcc.Tab(label='Marital Status', value='tab-1'),
#         dcc.Tab(label='Has Children', value='tab-2'),
#         dcc.Tab(label='Home Owner', value='tab-3'),
#     ]),
#     dcc.Graph(id='churn_graph'),
# ])
#
# # Callback to update the graph based on the selected tab
# @my_app.callback(
#     Output('churn_graph', 'figure'),
#     [Input('tabs', 'value')]
# )
# def update_graph(selected_tab):
#     if selected_tab == 'tab-1':
#         # Churn rates by Marital Status
#         grouped_df = df2.groupby('marital_status')['churn_rate'].mean().reset_index()
#         fig = px.bar(grouped_df, x='marital_status', y='churn_rate', title='Churn Rates by Marital Status')
#     elif selected_tab == 'tab-2':
#         # Churn rates by Has Children
#         grouped_df = df2.groupby('has_children')['churn_rate'].mean().reset_index()
#         fig = px.bar(grouped_df, x='has_children', y='churn_rate', title='Churn Rates by Has Children')
#     else:
#         # Churn rates by Home Owner
#         grouped_df = df2.groupby('home_owner')['churn_rate'].mean().reset_index()
#         fig = px.bar(grouped_df, x='home_owner', y='churn_rate', title='Churn Rates by Home Owner')
#
#     fig.update_layout(xaxis_title='Category', yaxis_title='Churn Rate')
#     fig.update_traces(marker_color='blue', marker_line_color='black',
#                       marker_line_width=1.5, opacity=0.6)
#     fig.update_traces(hovertemplate='Category: %{x}<br>Churn Rate: %{y:.2f}')
#
#     return fig







# ====================
# Question 4 layout
# ====================

import json

#%%

# Layout for a geographic map
import json

with open('/Users/brian/Downloads/GWU/2024 Spring/Visualization_of_complex_data/Term Project/texas_county2.geojson') as f:
    county_geojson = json.load(f)

print(county_geojson['features'][0]['properties'].keys())


#%%
'''Data Preprocessing'''
import pandas as pd

# Map data matching
df = pd.read_csv("/Users/brian/Downloads/GWU/2024 Spring/Visualization_of_complex_data/Term Project/Term Dataset/autoinsurance_churn.csv")
county_info_df = pd.read_csv('/Users/brian/Downloads/GWU/2024 Spring/Visualization_of_complex_data/Term Project/texas_county2.csv')
df3 = df.dropna(subset=['county'])
df3 = pd.merge(df, county_info_df[['name', 'geoid']], left_on='county', right_on='name', how='left')
county = df3['county'].unique().tolist()

#%%
# Churn data mapping
df3['churn_label'] = df3['Churn'].map({1: 'Churn', 0: 'Not Churn'})
county_churn_totals = df3.groupby('county')['Churn'].sum().reset_index()
county_churn_totals = county_churn_totals.rename(columns={'Churn': 'churn_count'})
unique_geoid = df3[['county', 'geoid']].drop_duplicates()
county_churn_totals2 = county_churn_totals.merge(unique_geoid, on='county', how='left')


#%%
fig = px.choropleth(
    county_churn_totals2,
    geojson=county_geojson,
    locations='geoid',
    color='churn_count',
    hover_data={'county': True},
    color_continuous_scale="Reds",
    scope="usa",
    title="Customer Churn Counts by County in Texas",
    labels={'churn_count': 'Churn Count'},
    featureidkey="properties.geoid"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Layout4 - In this case, the First plotting and then creating layout
l4_layout = html.Div([
    html.H3('Customer Churn Counts by County in Texas'),
    dcc.Graph(figure=fig)  # Using the figure directly here
])



# import plotly.express as px
#
# l4_layout = html.Div([
#     dcc.Graph(id='geo-map')
# ])
#
#
# # Callback
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('county-selector', 'value')]
# )
#
# def plot_choropleth():
#     fig = px.choropleth(
#         county_churn_totals2,
#         geojson=county_geojson,
#         locations='geoid',
#         color='churn_count',
#         color_continuous_scale="Reds",
#         scope="usa",
#         title="Customer Churn Counts by County in Texas",
#         labels={'churn_count': 'Churn Count'},
#         featureidkey="properties.geoid"
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(width=1000, height=600)
#     fig.update_geos(
#         visible=False,
#         lonaxis_range=[-106.65, -93.51],  # Texas longitude bounds
#         lataxis_range=[25.84, 36.5]       # Texas latitude bounds
#     )
#
#     fig.show()




# l4_layout = html.Div([
#     html.H3('Customer Churn Counts by County in Texas'),
#     html.H4('Select the county'),
#     dcc.RadioItems(
#         id='county-selector',
#         options=[{'label': county, 'value': county} for county in county_churn_totals2['county'].unique()],
#         value=county_churn_totals2['county'].unique()[0]
#     ),
#     dcc.Graph(id='geo-map')
# ])
#
#
# # Callback
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('county-selector', 'value')]
# )
# def update_map(selected_county):
#     filtered_data = county_churn_totals2[county_churn_totals2['county'] == selected_county]
#     filtered_data['geoid'] = filtered_data['geoid'].astype(str)
#
#     fig = px.choropleth(
#         filtered_data,
#         geojson=county_geojson,
#         locations='geoid',
#         color='churn_count',
#         color_continuous_scale="Reds",
#         scope="usa",
#         title=f"Customer Churn Counts in {selected_county}, Texas",
#         labels={'churn_count': 'Churn Count'},
#         featureidkey="properties.geoid"
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(width=1000, height=1000)
#     fig.update_geos(projection_type="mercator")
#
#     fig.update_geos(
#         visible=False,
#         lonaxis_range=[-106.65, -93.51],  # Texas longitude bounds
#         lataxis_range=[25.84, 36.5]  # Texas latitude bounds
#     )
#
#     return fig
#
#


# l4_layout = html.Div([
#     html.H3('Customer Churn Counts by County in Texas'),
#     dcc.Graph(id='geo-map')
# ])
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('input-geo', 'state')]
# )
# def update_map(_):
#     county_churn_totals2['geoid'] = county_churn_totals2['geoid'].astype(str)
#     fig = px.choropleth(
#         county_churn_totals2,
#         geojson=county_geojson,
#         locations='geoid',
#         color='churn_count',
#         color_continuous_scale="Reds",
#         scope="usa",
#         title="Customer Churn Counts by County in Texas",
#         labels={'churn_count': 'Churn Count'},
#         featureidkey="properties.geoid"
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(width=1000, height=1000)
#     fig.update_geos(projection_type="mercator")
#
#     fig.update_geos(
#         visible=False,
#         lonaxis_range=[-106.65, -93.51],  # Texas longitude bounds
#         lataxis_range=[25.84, 36.5]       # Texas latitude bounds
#     )
#
#     return fig




#
# l4_layout = html.Div([
#     html.H3('Customer Churn Counts by County in Texas'),
#     dcc.Graph(id='geo-map')
# ])
#
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('geo-map', 'id')]
# )
# def update_map(_):
#     # Make sure the 'geoid' column is of type string for matching
#     # county_churn_totals2['geoid'] = county_churn_totals2['geoid'].astype(str)
#
#     # Create the choropleth map
#     fig = px.choropleth(
#         county_churn_totals2,
#         geojson=county_geojson,
#         locations='geoid',
#         color='churn_count',
#         color_continuous_scale="Reds",
#         scope="usa",
#         title="Customer Churn Counts by County in Texas",
#         labels={'churn_count': 'Churn Count'}
#     )
#     fig.update_geos(fitbounds="locations", visible=False)
#     fig.update_layout(width=1000, height=1000)
#     fig.update_geos(projection_type="mercator")
#
#     # Setting the geographical bounds to Texas
#     fig.update_geos(
#         visible=False,
#         lonaxis_range=[-106.65, -93.51],  # Texas longitude bounds
#         lataxis_range=[25.84, 36.5]       # Texas latitude bounds
#     )
#
#     return fig





# l4_layout = html.Div([
#     html.H3('Geographic Insights: Customer Locations by Churn Status'),
#     dcc.Graph(id='geo-map')
# ])
#
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('geo-map', 'id')]
# )
# def update_map(_):
#     fig = px.scatter_geo(df2, lat='latitude', lon='longitude', color='churn_label',
#                          color_discrete_map={"Churn": "red", "Not Churn": "green"},
#                          title="Customer Locations by Churn Status in Texas",
#                          scope='usa',
#                          hover_name='Churn', hover_data={'latitude': False, 'longitude': False})
#     fig.update_geos(fitbounds="locations", visible=False)
#     # fig.update_layout(width=1000, height=1000)
#
#     return fig





# l4_layout = html.Div([
#     html.H3('Geographic Insights: Customer Locations by Churn Status'),
#     dcc.Graph(id='geo-map')
# ])
#
# # Callback to update the map
# @my_app.callback(
#     Output('geo-map', 'figure'),
#     [Input('geo-map', 'id')]  # This input is just to initialize the map; adjust as needed
# )
# def update_map(_):
#     # Texas approximate geographic center coordinates
#     texas_center = {"lat": 31.9686, "lon": -99.9018}
#
#     fig = px.scatter_mapbox(df2, lat='latitude', lon='longitude', color='churn_label',
#                             color_discrete_map={"Churn": "red", "Not Churn": "green"},
#                             title="Customer Locations by Churn Status in Texas",
#                             hover_name='churn_label', hover_data={'latitude': False, 'longitude': False},
#                             zoom=5, center=texas_center)
#     fig.update_layout(mapbox_style="light", mapbox_accesstoken='Your_Mapbox_Access_Token_Here')
#     return fig


# ====================
# Layout callback
# ====================

@my_app.callback(
    Output(component_id='layout',component_property='children'),
    Input(component_id='term', component_property='value')
)

def update_layout(ques):
    if ques == 'l1':
        return l1_layout
    elif ques == 'l2':
        return l2_layout
    elif ques == 'l3':
        return l3_layout
    elif ques == 'l4':
        return l4_layout

#===================
# Phase 5
#===================

# if __name__ == '__main__':
#     my_app.run_server(debug=True, host='0.0.0.0', port=8080)
#
my_app.run_server(
    port=8020,
    host='0.0.0.0'
)

