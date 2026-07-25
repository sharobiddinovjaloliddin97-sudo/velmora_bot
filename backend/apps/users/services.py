from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class UserService:

    @staticmethod
    @transaction.atomic
    def create_user(validated_data):
        return User.objects.create_user(**validated_data)

    @staticmethod
    def login(email, password):
        user = authenticate(
            username=email,
            password=password,
        )

        if user is None:
            raise ValidationError("Invalid email or password.")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }