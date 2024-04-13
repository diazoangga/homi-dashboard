import pandas as pd
import os

working_dir = './data/'

class DataAnalysis:
    TRANS_SELECTED_COL = [
        'No Nota',
        'Waktu Order',
        'Produk',
        'Penjualan',
        'Metode Pembayaran'
    ]

    PROD_SELECTED_COL = [
        'Nama Produk',
        'Kategori',
        'Satuan #1',
        'Harga Beli Satuan #1',
        'Harga Jual Satuan #1',
        'SKU Satuan #1'
    ]
    def __init__(self, working_dir):
        super().__init__()
        self.import_files(working_dir)

    def import_files(self, working_dir):

        trans_file_paths = [working_dir+file for file in os.listdir(working_dir) if file.startswith('detil_penjualan')]
        
        # Create an empty list to store individual DataFrames
        dfs = []
        skiprows = 12

        # print(file_paths)
        
        # Iterate over each file path
        for file_path in trans_file_paths:
            print(file_path)
            # Read Excel file into a DataFrame
            df_transaction = pd.read_excel(file_path, skiprows=skiprows)
            # Append DataFrame to the list
            dfs.append(df_transaction)

            
        
        # Concatenate all DataFrames into one DataFrame
        df_transaction = pd.concat(dfs, ignore_index=True)
        df_transaction = df_transaction[self.TRANS_SELECTED_COL]

        df_transaction['Waktu Order'] = pd.to_datetime(df_transaction['Waktu Order'])

        df_transaction['Hour'] = df_transaction['Waktu Order'].dt.hour

        df_transaction['Day'] = df_transaction['Waktu Order'].dt.day
        df_transaction['Month'] = df_transaction['Waktu Order'].dt.month
        df_transaction['Year'] = df_transaction['Waktu Order'].dt.year

        df_transaction['Date'] = df_transaction['Waktu Order'].dt.date

        df_transaction.sort_values(by='Date', inplace=True)

        # df_transaction.to_csv('./output.csv', index=True)

        self.df_transaction = df_transaction


        ##======================================##

        prod_file_path = [working_dir+file for file in os.listdir(working_dir) if file.startswith('laporan_produk')]
        
        # Create an empty list to store individual DataFrames
        dfs = []
        skiprows = 0

        # print(file_paths)
        
        # Iterate over each file path
        for file_path in prod_file_path:
            # Read Excel file into a DataFrame
            df = pd.read_excel(file_path, skiprows=skiprows)
            # Append DataFrame to the list
            dfs.append(df)

        if len(dfs) > 1:
            df_product = pd.concat(dfs, ignore_index=True)
        else:
            df_product = dfs[0]
        
        df_product = df_product[self.PROD_SELECTED_COL]
        df_product = df_product.rename(columns={
            'Nama Produk': 'Produk'
        })
        self.df_product = df_product

        self.df_split_transaction = self.df_transaction.assign(Produk=self.df_transaction['Produk'].str.split(',')).explode('Produk')
        # print(len(self.df_split_transaction['Produk']))
        self.df_transaction_products = pd.merge(self.df_split_transaction, self.df_product, on='Produk', how='left')


        # print(self.df_transaction_products)

        # self.df_transaction_products.to_excel('./transaction_products.xlsx', index=True)

    def count_transactions_per_hour(self):
        hourly_counts = self.df_transaction.groupby('Hour').size().reset_index(name='Total Transactions')
        return hourly_counts

    def count_transactions_per_month(self):
        transactions_per_month = self.df_transaction.groupby('Month').size().reset_index(name='Total Transactions')
        return transactions_per_month
    
    def count_revenue_per_month(self):
        revenue_per_month = self.df_transaction.groupby('Month')['Penjualan'].sum().reset_index(name='Total Revenue')
        # print(revenue_per_month)
        # print(revenue_per_month)
        return revenue_per_month
    
    def count_sold_products(self):
        products = self.df_transaction['Produk'].str.split(',', expand=True).stack()

        # Count the occurrences of each product
        product_counts = products.value_counts().reset_index(name='Total Sold')

        # Rename the columns for clarity
        product_counts.columns = ['Product', 'Total Sold']

        return product_counts
    
    def count_revenue_per_product(self):
        self.revenue_per_product = self.df_transaction_products.groupby('Produk')['Harga Jual Satuan #1'].sum().reset_index(name='Total Revenue Product')
        self.revenue_per_product = self.revenue_per_product.sort_values(by='Total Revenue Product', ascending=False)
        self.revenue_per_product.columns = ['Product', 'Total Revenue Product']
        return self.revenue_per_product

    
    def count_mean_sold_products_weekly(self):
        # Convert 'Waktu Order' to datetime if it's not already in datetime format

        # Extract week number, day name, and product
        df_transaction = self.df_transaction
        df_transaction['Week_Number'] = df_transaction['Waktu Order'].dt.isocalendar().week
        df_transaction['Day_Name'] = df_transaction['Waktu Order'].dt.day_name()
        df_transaction['Product'] = df_transaction['Produk'].str.split(',')
        # print(self.df_transaction)

        # Explode 'Product' column to have each product in a separate row
        df_transaction = df_transaction.explode('Product')

        # Group by product, week, and day, then calculate the mean of transactions per day
        mean_transactions_per_day = df_transaction.groupby(['Product', 'Week_Number', 'Day_Name'])['No Nota'].count().groupby(['Product', 'Week_Number']).size().reset_index()

        # print("Mean Transactions Per Day for Each Product Per Week:")
        return mean_transactions_per_day
    
    def count_product_category(self):
        self.df_product_category = self.df_transaction_products.groupby('Kategori')['Penjualan'].sum().reset_index(name='Total Revenue per Category')
        self.df_product_category = self.df_product_category.sort_values(by='Total Revenue per Category', ascending=False)
        self.df_product_category.columns = ['Category', 'Total Revenue per Category']
        return self.df_product_category
    
    def count_sales_per_month(self):
        sales_per_month = self.df_transaction.groupby('Month')['Penjualan'].sum().reset_index(name="Total Sales")
        return sales_per_month
    
    def count_sum_transaction(self):
        self.sum_transaction = len(self.df_transaction)
        return self.sum_transaction
    
    def count_sum_sold_products(self):
        self.sum_sold_products = len(self.df_transaction_products)
        return self.sum_sold_products
    
    def count_ratio_product_transaction(self):
        self.ratio_product_transaction = self.sum_sold_products/self.sum_transaction
        return self.ratio_product_transaction
    
    def count_ratio_revenue_transaction(self):
        self.ratio_revenue_transaction = self.sum_sales/self.sum_transaction
        return self.ratio_revenue_transaction
    
    def count_ratio_revenue_product(self):
        self.ratio_revenue_product = self.sum_sales/self.sum_sold_products
        return self.ratio_revenue_product
    
    def count_sum_revenue(self):
        self.sum_sales = self.df_transaction['Penjualan'].sum()
        return self.sum_sales
    
    def count_sum_profit(self):
        sum_sales = self.count_sum_revenue()
        sum_hpp = self.df_transaction['Tagihan'].sum()
        return sum_sales
    
    

    def calculate_bonus(self, target_year, target_month):
        KELAS1 = 2000000
        KELAS2 = 3000000
        KELAS3 = 4000000
        KELAS4 = 5000000

        start_year = target_year - 1 if target_month == 1 else target_year
        start_month = 12 if target_month == 1 else target_month - 1
        start_date = pd.to_datetime(f"{start_year}-{start_month}-25")
        end_date = pd.to_datetime(f"{target_year}-{target_month}-24")
        filtered_df = self.df_transaction[['No Nota', 'Waktu Order', 'Date', 'Penjualan']]
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])
        # print(start_date)
        filtered_df = filtered_df.loc[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)].reset_index()
        # print(filtered_df)

        total_sales = filtered_df['Penjualan'].sum()
        days_diff = (end_date - start_date).days + 1

        avg_sales = total_sales/days_diff

        # print("avg sales from", start_date.strftime("%Y-%m-%d"), "is ", avg_sales)

        if avg_sales < KELAS1:
            bonus = 0
        elif avg_sales >= KELAS1 and avg_sales <= KELAS2:
            bonus = 0.02*total_sales
        elif avg_sales > KELAS2 and avg_sales <= KELAS3:
            bonus = 0.03*total_sales
        elif avg_sales > KELAS3 and avg_sales <= KELAS4:
            bonus = 0.04*total_sales
        else:
            bonus= 0.05*total_sales
        
        # print('bonus: ', bonus)
        return bonus
    
    def analysis(self):
        self.df_transaction_per_hour = self.count_transactions_per_hour()
        self.df_transaction_per_month = self.count_transactions_per_month()
        self.df_product_counts = self.count_sold_products()
        self.df_mean_transactions_per_day = self.count_mean_sold_products_weekly()
        self.df_sales_per_month = self.count_sales_per_month()

        return {
            'transaction_per_hour': self.df_transaction_per_hour,
            'transaction_per_month': self.df_transaction_per_month,
            'product_counts': self.df_product_counts,
            'avg_transaction_per_day': self.df_mean_transactions_per_day,
            'sales_per_month': self.df_sales_per_month
        }

# if __name__ == "__main__":    
#     df = DataAnalysis(working_dir)

#     df_transaction_per_hour = df.count_transactions_per_hour()
#     df_transaction_per_month = df.count_transactions_per_month()
#     df_product_counts = df.count_sold_products()
#     df_mean_transactions_per_day = df.count_mean_sold_products_weekly()
#     df_sales_per_month = df.count_sales_per_month()
#     df.calculate_bonus(2024, 2)

#     excel_writer = pd.ExcelWriter('./test.xlsx', engine='xlsxwriter')

#     df_transaction_per_hour.to_excel(excel_writer, index=False, sheet_name='transaction_per_hour')
#     df_transaction_per_month.to_excel(excel_writer, index=False, sheet_name='transaction_per_month')
#     df_product_counts.to_excel(excel_writer, index=False, sheet_name='product_counts')
#     df_mean_transactions_per_day.to_excel(excel_writer, index=False, sheet_name='mean_transactions_per_day')
#     df_sales_per_month.to_excel(excel_writer, index=False, sheet_name='sales_per_month')

#     excel_writer.close()

