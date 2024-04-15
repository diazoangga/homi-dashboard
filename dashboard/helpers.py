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

def update_montly_transaction_bar_plot(selected_year,selected_month, data=data):
    data.yoy_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_transactions_per_month()

    # Create stacked bar plot
    fig = px.bar(
        analyzed_data,
        x='Month',
        y='Total Transactions',
        title=f'Total Monthly Transactions YoY - {selected_month}/{selected_year}',
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

def update_hourly_transaction_bar_plot(selected_year,selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_transactions_per_hour()

    # Create stacked bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=analyzed_data['Hour'],
        y=analyzed_data['Total Transactions'],
        marker_color='#90a4ae',
    ))

    fig.update_layout(
        title=f'Total Hourly Transactions YoY - {selected_month}/{selected_year}',
        xaxis_title='Hour',
        yaxis_title='Total Transactions',
        yaxis2=dict(title='Volume',overlaying='y',showgrid=False, side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_revenue_per_month_bar_plot(selected_year, selected_month, data=data):
    data.yoy_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_revenue_per_month()
    transaction_per_month = data.count_transactions_per_month()

    # Create stacked bar plot
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=analyzed_data['Month-Year'],
        y=analyzed_data['Total Revenue'],
        marker_color='#90a4ae',
    ))

    fig.add_trace(go.Scatter(
        x=transaction_per_month['Month-Year'],
        y=transaction_per_month['Total Transactions'],
        # mode='lines+markers',
        name='Transaction',
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'Total Revenue per Month YoY - {selected_month}/{selected_year}',
        xaxis_title='Date',
        yaxis_title='Total Revenue',
        yaxis2=dict(title='Total Transaction',
                    rangemode='tozero',
                    overlaying='y',
                    showgrid=False, 
                    side='right'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_revenue_per_day_bar_plot(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_revenue_per_day()
    transaction_per_day = data.count_transaction_per_day()

    # Create stacked bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=analyzed_data['Day Name'],
        y=analyzed_data['Total Revenue'],
        marker_color='#90a4ae',
    ))

    fig.add_trace(go.Scatter(
        x=transaction_per_day['Day Name'],
        y=transaction_per_day['Total Transaction'],
        # mode='lines+markers',
        name='Transaction',
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'Total Revenue per Week YoY - {selected_month}/{selected_year}',
        xaxis_title='Day',
        yaxis_title='Total Revenue',
        yaxis2=dict(title='Total Transaction',
                    rangemode='tozero',
                    overlaying='y', 
                    side='right', 
                    showgrid=False),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1)
    )

    return fig

def update_sold_product_bar_plot(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_sold_products()
    total_sum = analyzed_data['Total Sold'].sum()
    analyzed_data['Cumulative'] = analyzed_data['Total Sold'].cumsum()/total_sum

    # Create stacked bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=analyzed_data['Product'],
        y=analyzed_data['Total Sold'],
        marker_color='#90a4ae',
    ))

    fig.add_trace(go.Scatter(
        x=analyzed_data['Product'],
        y=analyzed_data['Cumulative'],
        mode='lines+markers',
        name='Cumulative',
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'Total Sold Product YoY - {selected_month}/{selected_year}' if yoy==True else f'Sold Product in {selected_month}/{selected_year}',
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

def update_revenue_product_bar_plot(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_revenue_per_product()
    total_sum = analyzed_data['Total Revenue Product'].sum()
    analyzed_data['Cumulative'] = analyzed_data['Total Revenue Product'].cumsum()/total_sum

    # Create stacked bar plot
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=analyzed_data['Product'],
        y=analyzed_data['Total Revenue Product'],
        marker_color='#90a4ae',
    ))

    fig.add_trace(go.Scatter(
        x=analyzed_data['Product'],
        y=analyzed_data['Cumulative'],
        mode='lines+markers',
        name='Cumulative',
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'Total Revenue Product YoY - {selected_month}/{selected_year}' if yoy==True else f'Revenue Product in {selected_month}/{selected_year}',
        xaxis_title='Product',
        yaxis_title='Total Revenue Product',
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

def update_product_trans_revenue_bar_plot(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    # Group by year and month, and calculate the sum of sales, sold products, and transactions for each group
    # analyzed_data = data.df_transaction_products.groupby(['Year', 'Month'])['Produk'].size().reset_index(name='total_prodcuts')
    # analyzed_data['total_sales'] = data.df_transaction.groupby(['Year', 'Month'])['Penjualan'].sum().reset_index(name='total_sales')
    # analyzed_data['total_transactions'] = data.df_transaction.groupby(['Year', 'Month']).size().reset_index(name='total_transactions')
    analyzed_data = data.df_transaction.groupby(['Year', 'Month']).agg(
        total_sales=('Penjualan', 'sum'),
        total_transactions=('Penjualan', 'size')
    ).reset_index()
    grouped_sold_products = data.df_transaction_products.groupby(['Year', 'Month']).agg(
        total_sold_products=('Produk', 'size')
    ).reset_index()

    analyzed_data = pd.merge(analyzed_data, grouped_sold_products, on=['Year', 'Month'], how='left')


    # print(analyzed_data)
    # Calculate the ratio of sales/transaction and sold products/transaction for each month
    analyzed_data['Sales/Transaction'] = analyzed_data['total_sales'] / analyzed_data['total_transactions']
    analyzed_data['Sold Products/Transaction'] = analyzed_data['total_sold_products'] / analyzed_data['total_transactions']
    analyzed_data['Month-Year'] = analyzed_data['Month'].astype(str) + '/' + analyzed_data['Year'].astype(str)

    # Create stacked bar plot
    fig = px.line(
        analyzed_data,
        x=analyzed_data['Month-Year'],
        y='Sales/Transaction',
        color_discrete_sequence=['green'],
        title=f'Ratio Sales/Transaction and Sold Product/Transaction\nYoY - {selected_month}/{selected_year}' if yoy==True else f'Ratio Sales/Transaction and Sold Product/Transaction\nin {selected_month}/{selected_year}'
    )

    fig.add_trace(go.Scatter(
        x=analyzed_data['Month-Year'],
        y=analyzed_data['Sold Products/Transaction'],
        mode='lines+markers',
        yaxis='y2'
    ))

    fig.update_layout(
        xaxis_title='Month',
        yaxis=dict(title='Sales/Transaction', side='left', rangemode='tozero'),
        yaxis2=dict(title='Sold Product/Transaction', overlaying='y', side='right', showgrid=False, rangemode='tozero'),
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        legend=dict(title=dict(text='Property Type'), orientation='h', yanchor="bottom", y=1.02,xanchor="right",x=1),
        xaxis=dict(
            tickfont=dict(color='white', size=12),
            tickangle=45
        )
    )

    return fig

def update_customer_transaction_bar_plot(start_date, end_date, data=data):
    data.date_filtering_data(start_date, end_date)
    total_count, grouped_data = data.count_customer_transaction()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grouped_data['Sales Group'],
        y=grouped_data['Percentage'],
        hoverinfo='y',
        marker_color='#90a4ae',
    ))

    fig.update_layout(
        legend_title_text=f"# of Transaction: ${total_count}",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.01)
    )

    fig.update_layout(
        title='Number of Transactions by Sales Group',
        xaxis_title='Sales Group',
        yaxis_title='Percentage of Transactions (%)',
        plot_bgcolor='#343a40',
        paper_bgcolor='#343a40',
        font_color='white',
        showlegend=False
    )

    return fig
    
def update_num_transaction(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    sum_transaction = data.count_sum_transaction()
    sum_transaction_text = "{:,.0f}".format(sum_transaction)
    return sum_transaction_text

def update_sum_revenue(selected_year, selected_month, data=data, yoy=True): 
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    sum_sales = data.count_sum_revenue()
    sum_sales_text = "Rp {:,.0f}".format(sum_sales)
    return sum_sales_text

# def update_sum_profit(selected_year, selected_region, start_date, end_date, data=data):

def update_sum_sold_products(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    sum_sold_products = data.count_sum_sold_products()
    sum_sold_products_text = "{:,.0f}".format(sum_sold_products)
    return sum_sold_products_text

def update_ratio_product_transaction(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    ratio_product_transaction = data.count_ratio_product_transaction()
    ratio_product_transaction_text = "{:,.2f}".format(ratio_product_transaction)
    return ratio_product_transaction_text

def update_ratio_revenue_transaction(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    ratio_revenue_transaction = data.count_ratio_revenue_transaction()
    ratio_revenue_transaction_text = "Rp {:,.2f}".format(ratio_revenue_transaction)
    return ratio_revenue_transaction_text

def update_ratio_revenue_product(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    ratio_revenue_product = data.count_ratio_revenue_product()
    ratio_revenue_product_text = "Rp {:,.2f}".format(ratio_revenue_product)
    return ratio_revenue_product_text

def update_product_category_pie_chart(selected_year, selected_month, data=data, yoy=True):
    if yoy == True:
        data.yoy_filtering_data(selected_year, selected_month)
    else:
        data.month_filtering_data(selected_year, selected_month)
    analyzed_data = data.count_product_category()
    fig = px.pie(analyzed_data, values='Total Revenue per Category', names='Category')

    fig.update_layout(
        title='Total Revenue per Category',
        font=dict(color='white', size=14),  # Change font color and size
        plot_bgcolor='#343a40',  # Change plot background color
        paper_bgcolor='#343a40',
    )
    return fig