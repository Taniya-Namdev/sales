# Generated by Django 5.1.4 on 2024-12-24 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('upload_csv_file', '0003_sales_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='user',
        ),
    ]
