from django.db import models

# Create your models here.
from django.db import models

class File(models.Model):
    file = models.FileField(upload_to='files')
    uploaded_at = models.DateTimeField(auto_now_add =True)


# Schema Design for csv-data
    
# Geographical Info

class Region(models.Model):
    name = models.CharField(max_length=150,unique=True)

    def __str__(self):
        return str(self.name)

class Country(models.Model):
    name = models.CharField(max_length=150,unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.name)

# Product Info

class Product(models.Model):
    item_type = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.item_type)
    class Meta:
        unique_together=('item_type','unit_price','unit_cost')    



# Order Info 
    

from django.utils import timezone

class Order(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    SALES_CHANNEL_CHOICE = [
        (ONLINE,'online'),
        (OFFLINE,'offline')
    ]

    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    CRUCIAL = 'C'
    ORDER_PRIORITY_CHOICE = [
        (HIGH,'H'),
        (MEDIUM,'M'),
        (LOW,'L'),
        (CRUCIAL,'C')
    ]

    order_id = models.CharField(max_length=50, unique=True)
    order_date = models.DateField(default=timezone.now)
    ship_date = models.DateField(default=timezone.now)
    order_priority = models.CharField(max_length=5, choices=ORDER_PRIORITY_CHOICE, default = LOW)
    sales_channel = models.CharField(max_length=10, choices=SALES_CHANNEL_CHOICE,default=ONLINE)

    def __str__(self):
        return str(self.order_id)

# Sales Info

# models.py



class Sales(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return str(f"{self.order} - {self.product}")


