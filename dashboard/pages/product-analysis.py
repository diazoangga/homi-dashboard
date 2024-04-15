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
            html.Div("Select month:", className="dropdown-label"),
            width=1,
        ),
        dbc.Col(
            dcc.Dropdown(
                id='month-dropdown',
                options=[
                    {'label': month.split(', ')[0], 'value': month.split(', ')[1]}
                    for month in app_config['months']
                ],
                value=1,  # Default selected region
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
                    html.Div([
                        html.H6(children='Num. of Sold Products',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='prod-analysis-sum-sold-products',
                              style={'textAlign': 'center'}
                        )
                    ],
                    style={'background-color': '#607d8b',
                           'border-radius': '5px',
                           'margin': '25px',
                           'padding': '15px',
                           'box-shadow': '2px 2px 2px #607d8b'}
                    )               
                ),
                dbc.Col(
                    html.Div([
                        html.H6(children='Sold Product - Transaction Ratio',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='prod-analysis-ratio-product-transaction',
                              style={'textAlign': 'center'}
                        )
                    ],
                    style={'background-color': '#607d8b',
                           'border-radius': '5px',
                           'margin': '25px',
                           'padding': '15px',
                           'box-shadow': '2px 2px 2px #607d8b'}
                    )               
                ),

                dbc.Col(
                    html.Div([
                        html.H6(children='Revenue - Sold Product Ratio',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='prod-analysis-ratio-revenue-product',
                              style={'textAlign': 'center'}
                        )
                    ],
                    style={'background-color': '#607d8b',
                           'border-radius': '5px',
                           'margin': '25px',
                           'padding': '15px',
                           'box-shadow': '2px 2px 2px #607d8b'}
                    )               
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='prod-analysis-prod-category-pie-chart',
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

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='prod-analysis-sold-product-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=12
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='prod-analysis-revenue-product-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=12
                ),
                # dbc.Col(
                #     dcc.Graph(
                #         id='sold-product-bar-plot',
                #         style={'height': '60vh'}
                #     ),
                #     width=6
                # ),
            ]
        )
    ],
    fluid=True,
)

# Define callback to update the new plot based on selected year and region
@callback(
    Output('prod-analysis-prod-category-pie-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_product_category_pie_chart_callback(selected_year, selected_month):
    return update_product_category_pie_chart(selected_year, selected_month, yoy=False)

@callback(
    Output('prod-analysis-sold-product-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prod_analysis_sold_product_bar_plot_callback(selected_year,selected_month):
    return update_sold_product_bar_plot(selected_year,selected_month, yoy=False)

@callback(
    Output('prod-analysis-revenue-product-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prod_analysis_revenue_product_bar_plot_callback(selected_year,selected_month):
    return update_revenue_product_bar_plot(selected_year,selected_month, yoy=False)

@callback(
    Output('prod-analysis-sum-sold-products', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prod_analysis_sum_sold_products_callback(selected_year,selected_month):
    return update_sum_sold_products(selected_year,selected_month, yoy=False)

@callback(
    Output('prod-analysis-ratio-product-transaction', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prod_analysis_ratio_product_transaction_callback(selected_year,selected_month):
    return update_ratio_product_transaction(selected_year,selected_month, yoy=False)

@callback(
    Output('prod-analysis-ratio-revenue-product', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_prod_analysis_ratio_revenue_product_callback(selected_year,selected_month):
    return update_ratio_revenue_product(selected_year,selected_month, yoy=False)