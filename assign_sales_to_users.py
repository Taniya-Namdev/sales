import os
import django
import random
import logging
from django.db import transaction

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sales.settings')
django.setup()

from accounts.models import CustomUser  
from upload_csv_file.models import Sales

# Set up logging
logger = logging.getLogger('assign_sales')
logging.basicConfig(
    filename='assign_sales_log.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def assign_sales_to_users(batch_size=10):
    # Fetch all users and sales
    users = list(CustomUser.objects.all())
    sales_records = list(Sales.objects.all())

    if not users:
        logger.error("No users found in the database.")
        return False  # Indicate failure due to no users
    
    if not sales_records:
        logger.error("No sales records found in the database.")
        return False  # Indicate failure due to no sales records
    
    # Shuffle the list of users to randomize assignment
    random.shuffle(users)

    # Assign batches of sales to users
    user_index = 0
    for i in range(0, len(sales_records), batch_size):
        batch = sales_records[i:i + batch_size]
        current_user = users[user_index % len(users)]
        
        with transaction.atomic():
            for sales in batch:
                sales.user = current_user
                sales.save()
                logger.info(f"Assigned Sales ID {sales.id} to User {current_user.email}")
        
        user_index += 1

    return True  # Indicate success

def run():
    try:
        logger.info("Starting the process to assign sales orders to users.")
        success = assign_sales_to_users()
        if success:
            logger.info("Successfully assigned sales orders to users.")
        else:
            logger.warning("Assignment process was not successful due to missing users or sales records.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == '__main__':
    run()
