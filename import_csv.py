# import os
# import pandas as pd
# from django.utils import timezone
# import django
# import sys
# import logging
# from datetime import datetime

# ## ---- This is Iterative Approach which takes lot of time to upload csv ----- ##


# # Set up Django environment
# sys.path.append('/home/admin/Sales/CSV_upload')  # Adjust this path
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CSV_upload.settings')  # Adjust this module
# django.setup()

# from upload_file.models import Region, Country, Product, Order, Sales

# # Set up logging
# logger = logging.getLogger('import_csv')
# logging.basicConfig(
#     filename='import_log.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def is_valid_date(date_string):
#     try:
#         date = pd.to_datetime(date_string, format='%m/%d/%Y', errors='raise')
#         # Check if the day and month are within valid ranges
#         if date.day > 31 or date.month > 12:
#             return False
#         return True
#     except ValueError:
#         return False

# def read_csv(file_path):
#     start_time = datetime.now()
#     logger.info(f"Start Time: {start_time}")
#     print(f"Start Time: {start_time}")

#     df = pd.read_csv(file_path, delimiter=',')
#     total_records = len(df)
#     logger.info(f"CSV file read successfully, total records: {total_records}")
#     print(f"CSV file read successfully, total records: {total_records}")

#     for index, row in df.iterrows():
#         logger.info(f"Processing row {index+1}/{total_records}")
#         print(f"Processing row {index+1}/{total_records}")

#         # Create or get Region
#         region, created = Region.objects.get_or_create(name=row['Region'])
#         logger.debug(f"Region: {region.name}, Created: {created}")
#         print(f"Region: {region.name}, Created: {created}")

#         # Create or get Country
#         country, created = Country.objects.get_or_create(name=row['Country'], region=region)
#         logger.debug(f"Country: {country.name}, Created: {created}")
#         print(f"Country: {country.name}, Created: {created}")

#         # Create or get Product
#         product, created = Product.objects.get_or_create(
#             item_type=row['Item Type'],
#             unit_price=row['Unit Price'],
#             unit_cost=row['Unit Cost']
#         )
#         logger.debug(f"Product: {product.item_type}, Created: {created}")
#         print(f"Product: {product.item_type}, Created: {created}")

#         # Ensure order_date is not null and valid
#         order_date_str = row['Order Date']
#         ship_date_str = row['Ship Date']
        
#         # Validate dates
#         if is_valid_date(order_date_str):
#             order_date = pd.to_datetime(order_date_str)
#         else:
#             order_date = timezone.now()
        
#         if is_valid_date(ship_date_str):
#             ship_date = pd.to_datetime(ship_date_str)
#         else:
#             ship_date = timezone.now()

#         # Print the parsed dates for debugging
#         print(f"Parsed Order_Date: {order_date}, Parsed Ship_Date: {ship_date}")
#         logger.debug(f"Parsed Order_Date: {order_date}, Parsed Ship_Date: {ship_date}")

#         # Create or get Order
#         order_defaults = {
#             'order_date': order_date,
#             'ship_date': ship_date,
#             'order_priority': row['Order Priority'],
#             'sales_channel': row['Sales Channel']
#         }
#         order, created = Order.objects.update_or_create(
#             order_id=row['Order ID'],
#             defaults=order_defaults
#         )
#         logger.debug(f"Order: {order.order_id}, Created: {created}")
#         print(f"Order: {order.order_id}, Created: {created}")

#         # Create Sale
#         sale = Sales.objects.create(
#             order=order,
#             country=country,
#             product=product,
#             units_sold=row['Units Sold'],
#             total_revenue=row['Total Revenue'],
#             total_cost=row['Total Cost'],
#             total_profit=row['Total Profit']
#         )
#         logger.debug(f"Sale created: {sale}")
#         print(f"Sale created: {sale}")

#         # Log progress
#         logger.info(f"Processed row {index+1}/{total_records}, {total_records-(index+1)} records left")
#         print(f"Processed row {index+1}/{total_records}, {total_records-(index+1)} records left")

#     end_time = datetime.now()
#     logger.info(f"End Time: {end_time}")
#     print(f"End Time: {end_time}")
    
#     duration = end_time - start_time
#     logger.info(f"Total Time Taken: {duration}")
#     print(f"Total Time Taken: {duration}")

#     logger.info("Data imported successfully.")
#     print("Data imported successfully.")

# def run():
#     # Define the directory containing the CSV files
#     directory_path = os.path.join(os.getcwd(), 'files/files')  # Adjusted for nested files folder
#     # Specify the name of the CSV file
#     csv_filename = 'sales.csv'
#     # Construct the full file path
#     file_path = os.path.join(directory_path, csv_filename)
    
#     print(f"Reading CSV file from: {file_path}")
#     # Read the CSV file
#     read_csv(file_path)

# if __name__ == '__main__':
#     run()



# ## ---- It is Bulk Create approach which takes less time ----- ##
# import os
# import pandas as pd
# import django
# import sys
# import logging
# from datetime import datetime
# from django.utils import timezone
# from django.db import transaction

# # Set up Django environment
# sys.path.append(os.getcwd())  # Ensure the correct path to your project
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CSV_upload.settings')  # Adjust this module if needed
# django.setup()

# from upload_file.models import Region, Country, Product, Order, Sales

# # Set up logging
# logger = logging.getLogger('import_csv')
# logging.basicConfig(
#     filename='import_log.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'  # Corrected logging format
# )

# def is_valid_date(date_string):
#     try:
#         date = pd.to_datetime(date_string, format='%m/%d/%Y', errors='raise')
#         if date.day > 31 or date.month > 12:
#             return False
#         return True
#     except ValueError:
#         return False

# def bulk_insert_sales(sales_data):
#     Sales.objects.bulk_create(sales_data, batch_size=5000)  # Increased batch size to 5000

# def read_csv(file_path):
#     start_time = datetime.now()
#     logger.info(f"Start Time: {start_time}")
#     print(f"Start Time: {start_time}")

#     df = pd.read_csv(file_path, delimiter=',')
#     total_records = len(df)
#     logger.info(f"CSV file read successfully, total records: {total_records}")
#     print(f"CSV file read successfully, total records: {total_records}")

#     sales_data = []
#     with transaction.atomic():
#         for index, row in df.iterrows():
#             logger.info(f"Processing row {index+1}/{total_records}")
#             print(f"Processing row {index+1}/{total_records}")

#             region, _ = Region.objects.get_or_create(name=row['Region'])
#             country, _ = Country.objects.get_or_create(name=row['Country'], region=region)
#             product, _ = Product.objects.get_or_create(item_type=row['Item Type'], unit_price=row['Unit Price'], unit_cost=row['Unit Cost'])

#             order_date_str = row['Order Date']
#             ship_date_str = row['Ship Date']
#             if is_valid_date(order_date_str):
#                 order_date = pd.to_datetime(order_date_str).strftime('%Y-%m-%d')
#             else:
#                 order_date = timezone.now().strftime('%Y-%m-%d')

#             if is_valid_date(ship_date_str):
#                 ship_date = pd.to_datetime(ship_date_str).strftime('%Y-%m-%d')
#             else:
#                 ship_date = timezone.now().strftime('%Y-%m-%d')

#             order, _ = Order.objects.get_or_create(order_id=row['Order ID'], defaults={'order_date': order_date, 'ship_date': ship_date, 'order_priority': row['Order Priority'], 'sales_channel': row['Sales Channel']})

#             sale = Sales(
#                 order=order,
#                 country=country,
#                 product=product,
#                 units_sold=row['Units Sold'],
#                 total_revenue=row['Total Revenue'],
#                 total_cost=row['Total Cost'],
#                 total_profit=row['Total Profit']
#             )
#             sales_data.append(sale)

#             if len(sales_data) >= 5000:  # Insert in batches of 5000
#                 bulk_insert_sales(sales_data)
#                 sales_data = []

#         # Insert remaining records
#         if sales_data:
#             bulk_insert_sales(sales_data)

#     end_time = datetime.now()
#     logger.info(f"End Time: {end_time}")
#     print(f"End Time: {end_time}")

#     duration = end_time - start_time
#     logger.info(f"Total Time Taken: {duration}")
#     print(f"Total Time Taken: {duration}")

#     logger.info("Data imported successfully.")
#     print("Data imported successfully.")

# def run():
#     directory_path = os.path.join(os.getcwd(), 'files', 'files')
#     csv_filename = 'sales.csv'
#     file_path = os.path.join(directory_path, csv_filename)

#     print(f"Reading CSV file from: {file_path}")
#     read_csv(file_path)

# if __name__ == '__main__':
#     run()


# ## ---- Raw SQL Approach it take much leeser time then above processes ----- ##
# import os
# import pandas as pd
# import django
# import sys
# import logging
# from datetime import datetime
# from django.utils import timezone
# from django.db import connection

# # Set up Django environment
# sys.path.append(os.getcwd())  # Ensure the correct path to your project
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CSV_upload.settings')  # Adjust this module if needed
# django.setup()

# from upload_file.models import Region, Country, Product, Order, Sales

# # Set up logging
# logger = logging.getLogger('import_csv')
# logging.basicConfig(
#     filename='import_log.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def is_valid_date(date_string):
#     try:
#         date = pd.to_datetime(date_string, format='%m/%d/%Y', errors='raise')
#         if date.day > 31 or date.month > 12:
#             return False
#         return True
#     except ValueError:
#         return False

# def read_csv(file_path):
#     start_time = datetime.now()
#     logger.info(f"Start Time: {start_time}")
#     print(f"Start Time: {start_time}")

#     df = pd.read_csv(file_path, delimiter=',')
#     total_records = len(df)
#     logger.info(f"CSV file read successfully, total records: {total_records}")
#     print(f"CSV file read successfully, total records: {total_records}")

#     with connection.cursor() as cursor:
#         for index, row in df.iterrows():
#             logger.info(f"Processing row {index+1}/{total_records}")
#             print(f"Processing row {index+1}/{total_records}")

#             # Handle Region
#             region_name = row['Region']
#             cursor.execute("SELECT id FROM upload_file_region WHERE name=%s", (region_name,))
#             region_id = cursor.fetchone()
#             if region_id is None:
#                 cursor.execute("INSERT INTO upload_file_region (name) VALUES (%s)", (region_name,))
#                 region_id = cursor.lastrowid
#             else:
#                 region_id = region_id[0]

#             # Handle Country
#             country_name = row['Country']
#             cursor.execute("SELECT id FROM upload_file_country WHERE name=%s", (country_name,))
#             country_id = cursor.fetchone()
#             if country_id is None:
#                 cursor.execute("INSERT INTO upload_file_country (name, region_id) VALUES (%s, %s)", (country_name, region_id))
#                 country_id = cursor.lastrowid
#             else:
#                 country_id = country_id[0]

#             # Handle Product
#             item_type = row['Item Type']
#             unit_price = row['Unit Price']
#             unit_cost = row['Unit Cost']
#             cursor.execute("SELECT id FROM upload_file_product WHERE item_type=%s AND unit_price=%s AND unit_cost=%s", 
#                            (item_type, unit_price, unit_cost))
#             product_id = cursor.fetchone()
#             if product_id is None:
#                 cursor.execute("INSERT INTO upload_file_product (item_type, unit_price, unit_cost) VALUES (%s, %s, %s)", 
#                                (item_type, unit_price, unit_cost))
#                 product_id = cursor.lastrowid
#             else:
#                 product_id = product_id[0]

#             # Handle Order
#             order_date_str = row['Order Date']
#             ship_date_str = row['Ship Date']
#             if is_valid_date(order_date_str):
#                 order_date = pd.to_datetime(order_date_str).strftime('%Y-%m-%d')
#             else:
#                 order_date = timezone.now().strftime('%Y-%m-%d')

#             if is_valid_date(ship_date_str):
#                 ship_date = pd.to_datetime(ship_date_str).strftime('%Y-%m-%d')
#             else:
#                 ship_date = timezone.now().strftime('%Y-%m-%d')

#             order_id_str = row['Order ID']
#             order_priority = row['Order Priority']
#             sales_channel = row['Sales Channel']
#             cursor.execute("SELECT id FROM upload_file_order WHERE order_id=%s", (order_id_str,))
#             order_id = cursor.fetchone()
#             if order_id is None:
#                 # Debugging: Print parameters before executing
#                 # print("Inserting order with params:", (order_id_str, order_date, ship_date, order_priority, sales_channel))
#                 cursor.execute("""INSERT INTO upload_file_order (order_id, order_date, ship_date, order_priority, sales_channel)
#                                   VALUES (%s, %s, %s, %s, %s)""",
#                                (order_id_str, order_date, ship_date, order_priority, sales_channel))
#                 order_id = cursor.lastrowid
#             else:
#                 order_id = order_id[0]

#             # Handle Sales
#             units_sold = row['Units Sold']
#             total_revenue = row['Total Revenue']
#             total_cost = row['Total Cost']
#             total_profit = row['Total Profit']
#             # Debugging: Print parameters before executing
#             # print("Inserting sales with params:", (order_id, country_id, product_id, units_sold, total_revenue, total_cost, total_profit))
#             cursor.execute("""INSERT INTO upload_file_sales (order_id, country_id, product_id, units_sold, total_revenue, total_cost, total_profit)
#                               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
#                            (order_id, country_id, product_id, units_sold, total_revenue, total_cost, total_profit))

#             logger.info(f"Processed row {index+1}/{total_records}, {total_records-(index+1)} records left")
#             print(f"Processed row {index+1}/{total_records}, {total_records-(index+1)} records left")

#     connection.commit()
#     connection.close()

#     end_time = datetime.now()
#     logger.info(f"End Time: {end_time}")
#     print(f"End Time: {end_time}")

#     duration = end_time - start_time
#     logger.info(f"Total Time Taken: {duration}")
#     print(f"Total Time Taken: {duration}")

#     logger.info("Data imported successfully.")
#     print("Data imported successfully.")

# def run():
#     directory_path = os.path.join(os.getcwd(), 'files', 'files')
#     csv_filename = 'sales.csv'
#     file_path = os.path.join(directory_path, csv_filename)

#     print(f"Reading CSV file from: {file_path}")
#     read_csv(file_path)

# if __name__ == '__main__':
#     run()


# # Using postgres command - copy 
# import os
# import pandas as pd
# import psycopg2
# import logging
# from datetime import datetime

# # Set up logging
# logger = logging.getLogger('import_csv')
# logging.basicConfig(
#     filename='import_log.log',
#     level=logging.DEBUG,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )

# def split_csv(file_path):
#     df = pd.read_csv(file_path)

#     # Create individual dataframes for each table
#     region_df = df[['Region']].drop_duplicates().rename(columns={'Region': 'name'})
#     country_df = df[['Country', 'Region']].drop_duplicates().rename(columns={'Country': 'name', 'Region': 'region'})
#     product_df = df[['Item Type', 'Unit Price', 'Unit Cost']].drop_duplicates().rename(columns={'Item Type': 'item_type', 'Unit Price': 'unit_price', 'Unit Cost': 'unit_cost'})
#     order_df = df[['Order ID', 'Order Date', 'Ship Date', 'Order Priority', 'Sales Channel']].drop_duplicates().rename(columns={'Order ID': 'order_id', 'Order Date': 'order_date', 'Ship Date': 'ship_date', 'Order Priority': 'order_priority', 'Sales Channel': 'sales_channel'})
#     sales_df = df[['Order ID', 'Country', 'Item Type', 'Units Sold', 'Total Revenue', 'Total Cost', 'Total Profit']].rename(columns={'Order ID': 'order_id', 'Country': 'country_name', 'Item Type': 'product_item_type', 'Units Sold': 'units_sold', 'Total Revenue': 'total_revenue', 'Total Cost': 'total_cost', 'Total Profit': 'total_profit'})

#     # Save the individual dataframes to CSV files
#     directory = os.path.dirname(file_path)
#     region_df.to_csv(os.path.join(directory, 'region.csv'), index=False)
#     country_df.to_csv(os.path.join(directory, 'country.csv'), index=False)
#     product_df.to_csv(os.path.join(directory, 'product.csv'), index=False)
#     order_df.to_csv(os.path.join(directory, 'order.csv'), index=False)
#     sales_df.to_csv(os.path.join(directory, 'sales_only.csv'), index=False)

# def create_temp_table(conn, temp_table_name, temp_table_columns): 
#     cursor = conn.cursor() 
#     cursor.execute(f"CREATE TEMP TABLE {temp_table_name} ({temp_table_columns})") 
#     conn.commit() 
#     cursor.close()
#     cursor.close()

# def copy_to_temp_table(conn, csv_file, temp_table_name, columns):
#     cursor = conn.cursor()
#     with open(csv_file, 'r') as f:
#         cursor.copy_expert(f"COPY {temp_table_name} ({columns}) FROM STDIN WITH CSV HEADER", f)
#     conn.commit()
#     cursor.close()

# def insert_from_temp_table(conn, temp_table_name, main_table_name, columns):
#     cursor = conn.cursor()
#     cursor.execute(f"""
#         INSERT INTO {main_table_name} ({columns})
#         SELECT {columns} FROM {temp_table_name}
#         ON CONFLICT (name) DO NOTHING
#     """)
#     conn.commit()
#     cursor.close()

# def process_table(conn, csv_file, temp_table_name, main_table_name, columns, temp_table_columns):
#      create_temp_table(conn, temp_table_name, temp_table_columns) 
#      copy_to_temp_table(conn, csv_file, temp_table_name, columns) 
#      insert_from_temp_table(conn, temp_table_name, main_table_name, columns) 
# def run():
#     # Record start time
#     start_time = datetime.now()
#     logger.info(f"Start Time: {start_time}")
#     print(f"Start Time: {start_time}")

#     # PostgreSQL connection
#     conn = psycopg2.connect(
#         dbname="Sales",
#         user="postgres",
#         password="postgres",
#         host="localhost",
#         port=5432
#     )

#     # File path
#     directory_path = os.path.join(os.getcwd(), 'files', 'files')
#     csv_file = os.path.join(directory_path, 'sales.csv')

#     # Split CSV into individual files
#     split_csv(csv_file)

#     # Define table and columns mapping
#     tables_columns = {
#         'upload_file_region': ('name', 'name TEXT'),
#         'upload_file_country': ('name,region_id', 'name TEXT, region TEXT'),
#         'upload_file_product': ('item_type,unit_price,unit_cost', 'item_type TEXT, unit_price NUMERIC, unit_cost NUMERIC'),
#         'upload_file_order': ('order_id,order_date,ship_date,order_priority,sales_channel', 'order_id TEXT, order_date DATE, ship_date DATE, order_priority TEXT, sales_channel TEXT'),
#         'upload_file_sales': ('order_id,country_id,product_id,units_sold,total_revenue,total_cost,total_profit', 'order_id TEXT, country_name TEXT, product_item_type TEXT, units_sold INT, total_revenue NUMERIC, total_cost NUMERIC, total_profit NUMERIC')
#     }

#     # File paths for split CSVs
#     split_files = {
#         'upload_file_region': os.path.join(directory_path, 'region.csv'),
#         'upload_file_country': os.path.join(directory_path, 'country.csv'),
#         'upload_file_product': os.path.join(directory_path, 'product.csv'),
#         'upload_file_order': os.path.join(directory_path, 'order.csv'),
#         'upload_file_sales': os.path.join(directory_path, 'sales_only.csv')
#     }

#     # Import data
#     for main_table_name, (columns, temp_table_columns) in tables_columns.items():
#         temp_table_name = f"temp_{main_table_name}"
#         logger.info(f"Processing table {main_table_name}.")
#         print(f"Processing table {main_table_name}.")
#         process_table(conn, split_files[main_table_name], temp_table_name, main_table_name, columns)
#         logger.info(f"Completed processing table {main_table_name}.")
#         print(f"Completed processing table {main_table_name}.")

#     # Record end time
#     end_time = datetime.now()
#     logger.info(f"End Time: {end_time}")
#     print(f"End Time: {end_time}")

#     # Calculate duration
#     duration = end_time - start_time
#     logger.info(f"Total Time Taken: {duration}")
#     print(f"Total Time Taken: {duration}")

#     conn.close()

# if __name__ == '__main__':
#     run()

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
        name = row['Region']
        if name not in region_set:
            # if not Region.objects.filter(name=name).exists():
            Region.objects.create(name=name)
            region_set.add(name)
            logger.info(f"Region created or already exists: {name}")
            print(f"Region created or already exists: {name}")

        name = row['Country']
        if name not in country_set:
            if Region.objects.filter(name=name).exists():
                region = Region.objects.get(name=name)
                if not Country.objects.filter(name=name, region=region).exists():
                    Country.objects.create(name=name, region=region)
                country_set.add(name)
                logger.info(f"Country created or already exists: {name}")

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
    for start_idx in range(0, len(df), chunk_size):
        end_idx = min(start_idx + chunk_size, len(df))
        df_chunk = df.iloc[start_idx:end_idx]
        
        # Create 5 threads for each chunk of 5000 rows
        threads = []
        for i in range(0, len(df_chunk), 1000):
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