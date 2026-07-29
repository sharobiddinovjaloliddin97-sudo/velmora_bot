from rest_framework import serializers

from .models import User
from .services import UserService


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "telegram_id",
            "role",
            "loyalty_coins",
            "date_of_birth",
        )

        read_only_fields = (
            "id",
            "role",
            "telegram_id",
            "loyalty_coins",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
        )

    def create(self, validated_data):
        return UserService.create_user(validated_data)


class TelegramRegisterSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)

    language = serializers.ChoiceField(
        choices=["uz", "ru"],
        default="uz",
    )

    username = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    first_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
    )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        return UserService.login(
            email=attrs["email"],
            password=attrs["password"],
        )


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        request = self.context["request"]

        UserService.change_password(
            user=request.user,
            current_password=attrs["current_password"],
            new_password=attrs["new_password"],
        )

        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField(write_only=True)

    def validate(self, attrs):
        UserService.logout(attrs["refresh"])
        return attrs


