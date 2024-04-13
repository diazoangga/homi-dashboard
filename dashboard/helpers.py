import pandas as pd
import plotly.express as px
import numpy as np
import json
from config import app_config
import plotly.graph_objs as go

import sys
sys.path.append('../')
from backend.data_analysis import DataAnalysis

working_dir = './data/'
data = DataAnalysis(working_dir)

# Define the GeoJSON data globally
geojson_data = None
current_selected_region = None

# Read GeoJSON file for the selected region
def read_geojson(selected_region):
    global geojson_data
    global current_selected_region

    if current_selected_region != selected_region or geojson_data is None:
        geojson_file_path = f'geo_json/regions/{selected_region}_postcode_sectors.geojson'
        with open(geojson_file_path, 'r') as geojson_file:
            geojson_data = json.load(geojson_file)
        current_selected_region = selected_region

    return geojson_data

def update_map(selected_year, selected_region):
    # Load the CSV file based on the selected year
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    key_min = np.percentile(data.avg_price, 5)
    key_max = np.percentile(data.avg_price, 95)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Create choropleth map
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='avg_price',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        range_color=[key_min, key_max],
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'avg_price': 'Average Price £'},
        title=f'Average price by postcode sector for {selected_region} in {selected_year}',
        hover_data={'volume': True},
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Legend Title'), orientation='h', x=1, y=1.02),
    )

    return fig

def update_montly_transaction_bar_plot(selected_year,selected_region, start_date, end_date, data=data):

    analyzed_data = data.count_transactions_per_month()

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Month',
        y='Total Transactions',
        title=f'Total Monthly Transactions from {start_date} to {end_date}',
        barmode='stack',  # Set the barmode to 'stack' for stacked bars
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Transactions',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_hourly_transaction_bar_plot(selected_year,selected_region, start_date, end_date, data=data):

    analyzed_data = data.count_transactions_per_hour()

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Hour',
        y='Total Transactions',
        title=f'Total Hourly Transactions from {start_date} to {end_date}'
    )

    fig.update_layout(
        xaxis_title='Hour',
        yaxis_title='Total Transactions',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_revenue_per_month_bar_plot(selected_year, data=data):
    analyzed_data = data.count_revenue_per_month()

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Month',
        y='Total Revenue',
        title=f'Total Revenue per Month in The Year of {selected_year}'
    )

    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Total Revenue',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_sold_product_bar_plot(selected_year, data=data):
    analyzed_data = data.count_sold_products()
    total_sum = analyzed_data['Total Sold'].sum()
    analyzed_data['Cumulative'] = analyzed_data['Total Sold'].cumsum()/total_sum

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Product',
        y='Total Sold',
        title=f'Sold Product in The Year of {selected_year}'
    )

    fig.add_trace(go.Scatter(
        x=analyzed_data['Product'],
        y=analyzed_data['Cumulative'],
        mode='lines+markers',
        name='Cumulative',
        yaxis='y2'
    ))

    fig.update_layout(
        xaxis_title='Product',
        yaxis_title='Total Sold',
        yaxis2=dict(title='Cumulative', overlaying='y', side='right', showgrid=False),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1),
        xaxis=dict(
            tickfont=dict(color='white', size=8),
            tickangle=45
        )
    )

    return fig

def update_revenue_product_bar_plot(selected_year, data=data):
    analyzed_data = data.count_revenue_per_product()
    total_sum = analyzed_data['Total Revenue Product'].sum()
    analyzed_data['Cumulative'] = analyzed_data['Total Revenue Product'].cumsum()/total_sum

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Product',
        y='Total Revenue Product',
        title=f'Sold Product in The Year of {selected_year}'
    )

    fig.add_trace(go.Scatter(
        x=analyzed_data['Product'],
        y=analyzed_data['Cumulative'],
        mode='lines+markers',
        name='Cumulative',
        yaxis='y2'
    ))

    fig.update_layout(
        xaxis_title='Product',
        yaxis_title='Total Sold',
        yaxis2=dict(title='Cumulative', overlaying='y', side='right', showgrid=False),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1),
        xaxis=dict(
            tickfont=dict(color='white', size=8),
            tickangle=45
        )
    )

    return fig

def update_num_transaction(selected_year, selected_region, start_date, end_date, data=data):
    sum_transaction = data.count_sum_transaction()
    sum_transaction_text = "{:,.0f}".format(sum_transaction)
    return sum_transaction_text

def update_sum_revenue(selected_year, selected_region, start_date, end_date, data=data):   
    sum_sales = data.count_sum_revenue()
    sum_sales_text = "Rp {:,.0f}".format(sum_sales)
    return sum_sales_text

# def update_sum_profit(selected_year, selected_region, start_date, end_date, data=data):

def update_sum_sold_products(selected_year, selected_region, start_date, end_date, data=data):
    sum_sold_products = data.count_sum_sold_products()
    sum_sold_products_text = "{:,.0f}".format(sum_sold_products)
    return sum_sold_products_text

def update_ratio_product_transaction(selected_year, data=data):
    ratio_product_transaction = data.count_ratio_product_transaction()
    ratio_product_transaction_text = "{:,.2f}".format(ratio_product_transaction)
    return ratio_product_transaction_text

def update_ratio_revenue_transaction(selected_year, data=data):
    ratio_revenue_transaction = data.count_ratio_revenue_transaction()
    ratio_revenue_transaction_text = "Rp {:,.2f}".format(ratio_revenue_transaction)
    return ratio_revenue_transaction_text

def update_ratio_revenue_product(selected_year, data=data):
    ratio_revenue_product = data.count_ratio_revenue_product()
    ratio_revenue_product_text = "Rp {:,.2f}".format(ratio_revenue_product)
    return ratio_revenue_product_text

def update_product_category_pie_chart(selected_year,data=data):
    analyzed_data = data.count_product_category()
    fig = px.pie(analyzed_data, values='Total Revenue per Category', names='Category')

    fig.update_layout(
        title='Total Revenue per Category',
        font=dict(color='white', size=14),  # Change font color and size
        plot_bgcolor='#343a40',  # Change plot background color
        paper_bgcolor='#343a40',
    )
    return fig


def update_price_change(selected_year, selected_region):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    key_min = np.percentile(data.delta, 5)
    key_max = np.percentile(data.delta, 98)

    # Create choropleth map
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title=f'Year-on-year average price change for {selected_region} in {selected_year}',
        range_color=(key_min,key_max),
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_price_change_boxplot(selected_year,selected_region):
    start_year = int(selected_year) - 2
    end_year = int(selected_year) + 1

    # Create an empty list to store DataFrames
    all_data = []

    for year in range(start_year, end_year):
        # Load the preprocessed csvs with price change data for each year
        csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{year}.csv'
        year_data = pd.read_csv(csv_file_path)

        # Append the DataFrame to the list
        all_data.append(year_data)

    # Concatenate all dfs in the list
    data = pd.concat(all_data, ignore_index=True)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    y_min = np.percentile(data.delta, 1)
    y_max = np.percentile(data.delta, 99)

    # Create box plot
    fig = px.box(
        data,
        x='year',
        y='delta',
        title=f'Year-on-year sector average price change for {selected_region} between {start_year} and {selected_year}',
        labels={'delta': 'Price Change (%)'},
        color='year',
        range_y=[y_min, y_max],
    )

    # Update layout
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Price Change (%)',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_fastest_growing_plot(selected_year, selected_region,slider_value):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Sort the data by the delta column in descending order
    data = data.sort_values('delta', ascending=False)

    # Select the top X rows as selected by slider
    top_10_data = data.head(slider_value)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Create choropleth map
    fig = px.choropleth_mapbox(
        top_10_data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title= f'Top {slider_value} fastest growing sectors in {selected_region} in {selected_year}'
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_fastest_declining_plot(selected_year, selected_region, slider_value):
    # Load the CSV file with price change data based on the selected year
    csv_file_path = f'processed_data/avg_price_delta/avg_price_delta_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Sort the data by the 'delta' column in descending order
    data = data.sort_values('delta', ascending=False)

    # Select the top 10 rows
    top_10_data = data.tail(slider_value)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Create choropleth map
    fig = px.choropleth_mapbox(
        top_10_data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='delta',
        color_continuous_scale='Viridis',
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'delta': 'Price Change (%)'},
        title= f'Top {slider_value} fastest declining sectors in {selected_region} in {selected_year}'
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_volume_plot(selected_year, selected_region):
    # Load data
    csv_file_path = f'processed_data/volume_by_year/region_total_volume_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    fig = px.bar(data,
                  x='month',
                  y='volume',
                  color='region',
                  markers=True,
                  title=f'Volume trend for all regions in {selected_year} by month')
    
    # Update layout
    fig.update_layout(
        xaxis_title='Month',
        yaxis_title='Volume',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white'
    )

    return fig

def update_volume_map(selected_year, selected_region):
    # Load the CSV file based on the selected year
    csv_file_path = f'processed_data/average_price_by_year/region_data_{selected_year}.csv'
    data = pd.read_csv(csv_file_path)

    # Filter the data to the selected region
    data = data[data['region'] == selected_region]

    # Check if geojson is loaded for the selected region, load if not
    read_geojson(selected_region)

    # Fetch the configuration for the selected region
    region_config = app_config['regions'][selected_region]

    key_min = np.percentile(data.volume, 1)
    key_max = np.percentile(data.volume, 99)

    # Create choropleth map
    fig = px.choropleth_mapbox(
        data,
        geojson=geojson_data,
        locations='postcode_sector',
        featureidkey='properties.name',
        color='volume',
        color_continuous_scale='Viridis',
        range_color= [key_min,key_max],
        mapbox_style='carto-positron',
        center=region_config['center'],
        zoom=region_config['zoom'],
        opacity=0.5,
        labels={'volume': 'Volume'},
        title=f'Volume by postcode sector for {selected_region} in {selected_year}',
        hover_data={'volume': True},
    )

    # Update layout attributes
    fig.update_layout(
        mapbox=dict(style='carto-positron'),
        paper_bgcolor='#343a40',
        plot_bgcolor='#343a40',
        font_color='white'
    )

    return fig