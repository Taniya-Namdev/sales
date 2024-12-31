from .models import Order
from django_filters import rest_framework as filters

class OrderFilter(filters.FilterSet):
    order_date = filters.DateFilter(field_name="order_date")
    ship_date = filters.DateFilter(field_name="ship_date")
    order_priority = filters.ChoiceFilter(choices=Order.ORDER_PRIORITY_CHOICE)
    sales_channel = filters.ChoiceFilter(choices=Order.SALES_CHANNEL_CHOICE)

    class Meta:
        model = Order
        fields = ['order_date', 'ship_date', 'order_priority', 'sales_channel']
