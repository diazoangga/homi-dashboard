import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash
from helpers import *
from config import app_config
from datetime import date

dash.register_page(__name__,name="Customer Analysis", path='/customer-analysis')

layout = dbc.Container(
    [
               dbc.Row(
    [
        dbc.Col(
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=date(2018, 8, 5),
                max_date_allowed=date(2025, 9, 19),
                start_date=date(2023, 3, 5),
                end_date=date(2023, 8, 25)
            )
        ),

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
    className = "dropdown-row"
),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id='customer-transaction-bar-plot',
                        style={'height': '60vh'}
                    ),
                    width=6
                ),
                # dbc.Col(
                #     dcc.Graph(
                #         id='volume-plot-map',
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

# Define callback to update the new plot based on selected year and month
@callback(
    Output('customer-transaction-bar-plot', 'figure'),
    [Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')]
)
def update_customer_transaction_bar_plot_callback(start_date, end_date):
    return update_customer_transaction_bar_plot(start_date, end_date)
