from django.urls import path
from .views import (
    OrderCreateView, OrderUpdateView, OrderDeleteView, OrderListViewV1,
    AdminOrderListView, UserActivationView, UserListView
)
app_name = 'v1'
urlpatterns = [
    path('orders/', OrderListViewV1.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('orders/update/<int:pk>/', OrderUpdateView.as_view(), name='order-update'),
    path('orders/delete/<int:pk>/', OrderDeleteView.as_view(), name='order-delete'),
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),
    path('admin/users/', UserListView.as_view(), name='user-list'),
    path('admin/users/activate/<int:pk>/', UserActivationView.as_view(), name='user-activate'),
]