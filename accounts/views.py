from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class SignupView(APIView): 
    def post(self, request): 
        email = request.data.get('email') 
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password') 
        if password != confirm_password: 
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST) 
        # Validate password strength
        validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS) 
        errors = [] 
        for validator in validators: 
            try: 
                validator.validate(password, user=None)

            except DjangoValidationError as e: 
                errors.extend(e.messages) 

        if errors: 
            return Response({'error': ' '.join(errors)}, status=status.HTTP_400_BAD_REQUEST) 
        
        serializer = CustomUserSerializer(data={'email': email, 'password': password})
        if serializer.is_valid(): 
            user = serializer.save() 
            user.set_password(password) 
            # Hash the password 
            user.save() 
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                'message': 'You are logged in!',
                'access': access_token,
                'refresh': refresh_token,
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Invalid credentials',
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
