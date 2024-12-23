from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, LoginView, LogoutView, ProfileUpdateView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
