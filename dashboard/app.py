import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc
from backend.data_analysis import DataAnalysis

from dash.dependencies import Input, Output, State
import base64

# Create the dash app
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE, '/assets/custom.css'])

# Define the navigation bar
navbar =dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Main Dashboard", href="/")),
        dbc.NavItem(dbc.NavLink("Revenue Analysis", href="/revenue-analysis")),
        dbc.NavItem(dbc.NavLink("Product Analysis", href="/product-analysis")),
        dbc.NavItem(dbc.NavLink("Customer Analysis", href="/customer-analysis")),
    ],
    brand="HOMI Coffee and Space Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

upload = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Harry Allum | GitHub", href="https://github.com/harryallum/Dash-Property-Dashboard"), align="left"),
        ],
    ),
    className="footer",
    fluid=True,
)

# Overall layout
app.layout = html.Div([
    navbar,  # Include the navigation bar
    html.Div(id='output-data-upload'),
    upload,
    dash.page_container,
    footer,  # Include the footer
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            return html.Div([
                html.H5(filename),
                html.H6("CSV File Contents"),
                dcc.Markdown(decoded.decode('utf-8')),
            ])
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            return html.Div([
                html.H5(filename),
                html.H6("Excel File Contents"),
                html.Div(filename)
            ])
        else:
            return html.Div([
                'Unsupported file format'
            ])
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])


@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'))
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n) for c, n in
            zip(list_of_contents, list_of_names)]
        return children

# Run the dash app
if __name__ == '__main__':
    app.run_server(debug=True)
