import os
import django
import csv

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sales.settings")
django.setup()

from accounts.models import CustomUser  
def export_users_to_csv():
    file_path = 'users.csv'
    with open(file_path, 'w', newline='') as csvfile:
        fieldnames = ['id','email', 'first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for user in CustomUser.objects.all():
            writer.writerow({
                'id': user.id,
                'email':user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                
            })

    print(f'Successfully exported users to {file_path}')

if __name__ == "__main__":
    export_users_to_csv()
