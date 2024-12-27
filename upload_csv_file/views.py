from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
# Create your views here.

from .models import Order
from accounts.models import CustomUser
from .serializers import OrderSerializer
from rest_framework import filters as rest_filters
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, UserActivationSerializer
from accounts.serializers import CustomUserSerializer
from .filters import OrderFilter
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter 
from rest_framework.permissions import IsAdminUser



class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"message": "Order created successfully", "data": response.data}, status=response.status_code)

class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response({"message": "Order updated successfully", "data": response.data}, status=response.status_code)

class OrderDeleteView(APIView):
    def delete(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            order.is_delete = True
            order.save()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderListView(generics.ListAPIView):
    queryset = Order.objects.filter(is_delete=False)
    serializer_class = OrderSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = OrderFilter
    ordering_fields = ['order_date', 'ship_date', 'order_priority', 'sales_channel']
    pagination_class = OrderPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "Order list retrieved successfully", "data": response.data}, status=response.status_code)

class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        response = self.list(request, *args, **kwargs)
        return Response({"message": "Admin order list retrieved successfully", "data": response.data}, status=response.status_code)

class UserActivationView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            serializer = UserActivationSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User activation status updated successfully", "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class= OrderPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "User list retrieved successfully", "data": response.data}, status=response.status_code)
