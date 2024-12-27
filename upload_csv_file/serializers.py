from rest_framework import serializers
from .models import Order
from accounts.models import CustomUser

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_active']