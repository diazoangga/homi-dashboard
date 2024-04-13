import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash
from helpers import *
from config import app_config

dash.register_page(__name__, name="Product Analysis", path='/product-analysis')

layout = dbc.Container(
    [
               dbc.Row(
    [
        dbc.Col(
            html.Div("Select region:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='region-dropdown',
                options=[
                    {'label': region, 'value': region}
                    for region in app_config['regions']
                ],
                value='South East',  # Default selected region
            ),
            width=2
        ),
        dbc.Col(
            html.Div("Select year:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='year-dropdown',
                options=[{"label": i, "value": i} for i in app_config['years']],
                value='2023',  # Default selected year
            ),
            width=2,
        ),
    ],
    className = "mb-4 dropdown-row"
),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='prod-category-pie-chart',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                # dbc.Col(
                #     dcc.Graph(
                #         id='price-change-map',
                #         style={'height': '60vh'}
                #     ),
                #     width=6
                # ),
            ], 
            className="mb-4",
        ),
    ],
    fluid=True,
)

# Define callback to update the new plot based on selected year and region
@callback(
    Output('prod-category-pie-chart', 'figure'),
    Input('year-dropdown', 'value')
)
def update_product_category_pie_chart_callback(selected_year):
    return update_product_category_pie_chart(selected_year)