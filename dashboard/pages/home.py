import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from helpers import *
from config import app_config


dash.register_page(__name__, path='/')

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
                value=2024,  # Default selected year
            ),
            width=2,
        ),
    ],
    className = "dropdown-row"
),

        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.H6(children='Total Revenue',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='sum-revenue',
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
                        html.H6(children='Num. of Transaction',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='num-transaction',
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
                        html.H6(children='Num. of Sold Products',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='sum-sold-products',
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

                        html.P(id='ratio-product-transaction',
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
                        html.H6(children='Revenue - Transaction Ratio',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'}
                        ),

                        html.P(id='ratio-revenue-transaction',
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

                        html.P(id='ratio-revenue-product',
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


                # dbc.Col(
                #     dcc.Graph(id='sum-revenue',
                #               style={'height':'10vh'}
                #     ),
                #     width=2                
                # ),
                # dbc.Col(
                #     dcc.Graph(id='sum-profit',
                #               style={'height':'10vh'}
                #     ),
                #     width=2                
                # ),
                # dbc.Col(
                #     dcc.Graph(id='sum-sold-products',
                #               style={'height':'10vh'}
                #     ),
                #     width=2                
                # )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='revenue-per-month-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id='revenue-per-day-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='transaction-hourly-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),

                dbc.Col(
                    dcc.Graph(
                        id='product-trans-revenue-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
            ],
            className="mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='sold-product-bar-plot',
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
                        id='revenue-product-bar-plot',
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

# # Define callback to update the choropleth map based on selected year and region
# @callback(
#     Output('avg-price-map', 'figure'),
#     [Input('year-dropdown', 'value'),
#      Input('region-dropdown', 'value')]
# )
# def update_map_callback(selected_year, selected_region):
#     return update_map(selected_year, selected_region)

# Define callback to update the bar plot based on selected region

@callback(
    Output('transaction-hourly-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_hourly_transaction_bar_plot_callback(selected_year,selected_month):
    return update_hourly_transaction_bar_plot(selected_year,selected_month)

@callback(
    Output('sold-product-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_sold_product_bar_plot_callback(selected_year,selected_month):
    return update_sold_product_bar_plot(selected_year,selected_month)

@callback(
    Output('revenue-product-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')],
     
)
def update_revenue_product_bar_plot_callback(selected_year,selected_month):
    return update_revenue_product_bar_plot(selected_year,selected_month)

@callback(
    Output('revenue-per-month-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_revenue_per_month_bar_plot_callback(selected_year,selected_month):
    return update_revenue_per_month_bar_plot(selected_year,selected_month)

@callback(
    Output('revenue-per-day-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_revenue_per_day_bar_plot_callback(selected_year,selected_month):
    return update_revenue_per_day_bar_plot(selected_year,selected_month)

@callback(
    Output('product-trans-revenue-bar-plot', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')],
     
)
def update_product_trans_revenue_bar_plot_callback(selected_year,selected_month):
    return update_product_trans_revenue_bar_plot(selected_year,selected_month)

@callback(
    Output('num-transaction', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_num_transaction_callback(selected_year,selected_month):
    return update_num_transaction(selected_year,selected_month)

@callback(
    Output('sum-revenue', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_sum_revenue_callback(selected_year,selected_month):
    return update_sum_revenue(selected_year,selected_month)

# @callback(
#     Output('sum-profit', 'figure'),
#     [Input('year-dropdown', 'value'),
#      Input('month-dropdown', 'value'),
#      Input('my-date-picker-range', 'start_date'),
#      Input('my-date-picker-range', 'end_date')]
# )
# def update_sum_profit_callback(selected_year, selected_region, start_date, end_date):
#     return update_sum_profit(selected_year, selected_region, start_date, end_date)

@callback(
    Output('sum-sold-products', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_sum_sold_products_callback(selected_year,selected_month):
    return update_sum_sold_products(selected_year,selected_month)

@callback(
    Output('ratio-product-transaction', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_ratio_product_transaction_callback(selected_year,selected_month):
    return update_ratio_product_transaction(selected_year,selected_month)

@callback(
    Output('ratio-revenue-transaction', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_ratio_revenue_transaction_callback(selected_year,selected_month):
    return update_ratio_revenue_transaction(selected_year,selected_month)

@callback(
    Output('ratio-revenue-product', 'children'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_ratio_revenue_product_callback(selected_year,selected_month):
    return update_ratio_revenue_product(selected_year,selected_month)