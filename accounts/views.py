from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .tokens import account_activation_token
from .models import CustomUser as User
from .serializers import CustomUserSerializer, LoginSerializer
from .tasks import send_verification_email
import strings

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if password != confirm_password:
            return Response(strings.PASSWORDS_DO_NOT_MATCH_ERROR, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()

            # send verification email asynchronously
            current_site = get_current_site(request)
            send_verification_email(user.id, current_site.domain)
            return Response(strings.USER_REGISTERED_MESSAGE, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        try:
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return Response(strings.ACTIVATED_USER_MESSAGE, status=status.HTTP_200_OK)
        else:
            return Response(strings.INVALID_ACTIVATION_LINK_ERROR, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            user = User.objects.get(email=data['email'])
            login(request, user)
            
            # Update the login success message with dynamic data
            strings.LOGIN_SUCCESS_MESSAGE['refresh'] = data['refresh']
            strings.LOGIN_SUCCESS_MESSAGE['access'] = data['access']
            strings.LOGIN_SUCCESS_MESSAGE['user'] = data['user']

            return Response(strings.LOGIN_SUCCESS_MESSAGE, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            logout(request)
            return Response(strings.LOGOUT_SUCCESS_MESSAGE, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(strings.PROFILE_UPDATED_MESSAGE, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
