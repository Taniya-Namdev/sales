from django.db import models
from django.utils import timezone


# File model (Indexing 'uploaded_at' field)
class File(models.Model):
    file = models.FileField(upload_to='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['uploaded_at']),  # Index on uploaded_at
        ]


# Geographical Info

class Region(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Index on 'name' for faster searches
        ]

    def __str__(self):
        return str(self.name)


class Country(models.Model):
    name = models.CharField(max_length=150, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['name']),  # Index on 'name' for faster searches
            models.Index(fields=['region']),  # Index on 'region' for better performance of region-based queries
        ]

    def __str__(self):
        return str(self.name)


# Product Info

class Product(models.Model):
    item_type = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('item_type', 'unit_price', 'unit_cost')
        indexes = [
            models.Index(fields=['item_type']),  # Index on 'item_type' for better performance when filtering by item_type
            models.Index(fields=['unit_price']),  # Index on 'unit_price' for better performance when filtering by unit_price
            models.Index(fields=['unit_cost']),  # Index on 'unit_cost' for better performance when filtering by unit_cost
        ]

    def __str__(self):
        return str(self.item_type)


# Order Info 

class Order(models.Model):
    ONLINE = 'online'
    OFFLINE = 'offline'
    SALES_CHANNEL_CHOICE = [
        (ONLINE, 'online'),
        (OFFLINE, 'offline')
    ]

    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    CRUCIAL = 'C'
    ORDER_PRIORITY_CHOICE = [
        (HIGH, 'H'),
        (MEDIUM, 'M'),
        (LOW, 'L'),
        (CRUCIAL, 'C')
    ]

    order_id = models.CharField(max_length=50, unique=True)
    order_date = models.DateField(default=timezone.now)
    ship_date = models.DateField(default=timezone.now)
    order_priority = models.CharField(max_length=5, choices=ORDER_PRIORITY_CHOICE, default=LOW)
    sales_channel = models.CharField(max_length=10, choices=SALES_CHANNEL_CHOICE, default=ONLINE)

    class Meta:
        indexes = [
            models.Index(fields=['order_id']),  # Index on 'order_id' for faster lookups
            models.Index(fields=['order_date']),  # Index on 'order_date' for filtering by date
            models.Index(fields=['ship_date']),  # Index on 'ship_date' for filtering by shipping date
            models.Index(fields=['order_priority']),  # Index on 'order_priority' for filtering by priority
            models.Index(fields=['sales_channel']),  # Index on 'sales_channel' for filtering by sales channel
        ]

    def __str__(self):
        return str(self.order_id)


# Sales Info

class Sales(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    units_sold = models.IntegerField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_cost = models.DecimalField(max_digits=15, decimal_places=2)
    total_profit = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['order']),  # Index on 'order' for join optimization
            models.Index(fields=['country']),  # Index on 'country' for filtering by country
            models.Index(fields=['product']),  # Index on 'product' for filtering by product
        ]

    def __str__(self):
        return str(f"{self.order} - {self.product}")
