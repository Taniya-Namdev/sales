# # Using multithreading
import os
import pandas as pd
import django
import sys
import threading
import time
import logging
from datetime import datetime
from django.db import transaction

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales.settings')
django.setup()

from upload_csv_file.models import Region, Country, Product, Order, Sales

# Set up logging
logger = logging.getLogger('import_csv')
logging.basicConfig(
    filename='import_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize sets and lists
region_set = set()
country_set = set()
product_set = set()
order_list = []
sales_list = []
sales_lock = threading.Lock()

def preload_data(df):
    global region_set, country_set, product_set

    for index, row in df.iterrows():
        region_name = row['Region']
        if region_name not in region_set:
            # if not Region.objects.filter(name=name).exists():
            Region.objects.create(name=region_name)
            region_set.add(region_name)
            logger.info(f"Region created or already exists: {region_name}")
            print(f"Region created or already exists: {region_name}")

        country_name = row['Country']
        if country_name not in country_set:
            if region_name in region_set:
                region = Region.objects.get(name=region_name)
                Country.objects.create(name=country_name, region=region) 
                country_set.add(country_name) 
                logger.info(f"Country created or already exists: {country_name}") 
                print(f"Country created or already exists: {country_name}") 

        product_tuple = (row['Item Type'], row['Unit Price'], row['Unit Cost'])
        if product_tuple not in product_set:
            Product.objects.create(item_type=row['Item Type'], unit_price=row['Unit Price'], unit_cost=row['Unit Cost'])
            product_set.add(product_tuple)
            logger.info(f"Product created or already exists: {row['Item Type']}")

def process_chunk(df_chunk):
    global order_list, sales_list

    with transaction.atomic():
        for index, row in df_chunk.iterrows():
            order_id = row['Order ID']
            if order_id not in order_list:
                order_date = pd.to_datetime(row['Order Date']).strftime('%Y-%m-%d')
                ship_date = pd.to_datetime(row['Ship Date']).strftime('%Y-%m-%d')
                Order.objects.create(order_id=order_id, order_date=order_date, ship_date=ship_date, order_priority=row['Order Priority'], 
                sales_channel=row['Sales Channel'])
                order_list.append(order_id)
                logger.info(f"Order created or already exists: {order_id}")

            with sales_lock:
                order = Order.objects.get(order_id=order_id)
                country = Country.objects.get(name=row['Country'])
                product = Product.objects.get(item_type=row['Item Type'], unit_price=row['Unit Price'], unit_cost=row['Unit Cost'])
                sales_list.append(Sales(
                    order=order,
                    country=country,
                    product=product,
                    units_sold=row['Units Sold'],
                    total_revenue=row['Total Revenue'],
                    total_cost=row['Total Cost'],
                    total_profit=row['Total Profit']
                ))
                logger.info(f"Sales data added for Order ID: {order_id}")

def run():
    start_time = datetime.now()
    logger.info(f"Start Time: {start_time}")

    # File path
    directory_path = os.path.join(os.getcwd(), 'files')
    csv_file = os.path.join(directory_path, 'sales.csv')
    df = pd.read_csv(csv_file)

    # Preload regions, countries, and products
    preload_data(df)

    # Process the entire file in chunks of 5000 rows
    chunk_size = 5000
    len_df=len(df)
    for start_idx in range(0, len_df, chunk_size):
        end_idx = min(start_idx + chunk_size, len_df)
        df_chunk = df.iloc[start_idx:end_idx]
        
        # Create 5 threads for each chunk of 5000 rows
        threads = []
        len_df_chunk = len(df_chunk)
        for i in range(0, len_df_chunk, 1000):
            df_sub_chunk = df_chunk.iloc[i:i + 1000]
            thread = threading.Thread(target=process_chunk, args=(df_sub_chunk,))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    # Bulk create sales data once after processing all chunks
    Sales.objects.bulk_create(sales_list, batch_size=5000)
    logger.info("Sales data bulk created successfully.")

    end_time = datetime.now()
    logger.info(f"End Time: {end_time}")

    # Calculate duration
    duration = end_time - start_time
    logger.info(f"Total Time Taken: {duration}")

if __name__ == '__main__':
    run()