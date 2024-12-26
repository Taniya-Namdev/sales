from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

admin.site.register(File)
admin.site.register(Region)
admin.site.register(Country)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Sales)


