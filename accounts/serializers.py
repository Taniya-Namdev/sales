from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.conf import settings
from django.contrib.auth.password_validation import get_password_validators, validate_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')  # Include other fields as needed
        extra_kwargs = {
            'password': {'write_only': True, 'required': False}
        }

    def validate_password(self, value):
        if value:
            validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
            errors = []
            for validator in validators:
                try:
                    validator.validate(value)
                except DjangoValidationError as e:
                    errors.extend(e.messages)
            if errors:
                raise serializers.ValidationError(errors)
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance
