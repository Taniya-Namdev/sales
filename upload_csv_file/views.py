from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, filters
from rest_framework.pagination import PageNumberPagination 
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .models import Order
from accounts.models import CustomUser
from .filters import OrderFilter
from .serializers import OrderSerializer, UserActivationSerializer
from accounts.serializers import CustomUserSerializer
from django_filters.rest_framework import DjangoFilterBackend



class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]

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
        order = Order.objects.filter(pk=pk).first()
        if order:
            order.delete()
            return Response({"message": "Order deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

class OrderPagination(PageNumberPagination):
    page_size = 10  # Number of records per page
    page_size_query_param = 'page_size'
    max_page_size = 100

class OrderListViewV1(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = OrderPagination
    

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "Order list retrieved successfully", "data": response.data}, status=response.status_code)


class OrderListViewV2(generics.ListAPIView):
    queryset = Order.objects.filter(deleted_at=None)
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = OrderFilter
    ordering_fields = ['order_date', 'ship_date', 'order_priority', 'sales_channel']
    pagination_class = OrderPagination
    permission_classes = [IsAuthenticated]


    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "Order list retrieved successfully", "data": response.data}, status=response.status_code)

class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = [IsAdminUser]
    filterset_class = OrderFilter
    ordering_fields = ['order_date', 'ship_date', 'order_priority', 'sales_channel']

    def list(self, request, *args, **kwargs): 
        response = super().list(request, *args, **kwargs)
        return Response({"message": "Admin order list retrieved successfully", "data": response.data}, status=response.status_code)

class UserActivationView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        user = CustomUser.objects.filter(pk=pk).first()
        if user:
            serializer = UserActivationSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User activation status updated successfully", "data": serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: 
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class= OrderPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"message": "User list retrieved successfully", "data": response.data}, status=response.status_code)
