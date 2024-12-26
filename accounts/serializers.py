from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import get_password_validators, validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.conf import settings

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')  # Include other fields as needed
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_password(self, value):
        validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
        try:
            validate_password(password=value, password_validators=validators)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
    

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = CustomUserSerializer(read_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if user and user.is_active:
            refresh = RefreshToken.for_user(user)
            return {
                'email': user.email,
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': CustomUserSerializer(user).data
            }
        else:
            raise serializers.ValidationError("Invalid email or password")

    def create(self, validated_data):
        # Optionally, we could create any additional login-related objects here.
        pass
