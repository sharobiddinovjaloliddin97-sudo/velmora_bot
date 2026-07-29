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
    @transaction.atomic
    def telegram_register(validated_data):
        telegram_id = validated_data["telegram_id"]

        defaults = {
            "email": f"tg_{telegram_id}@telegram.local",
            "username": f"tg_{telegram_id}",
            "phone_number": validated_data["phone_number"],
            "first_name": validated_data.get("first_name", ""),
            "last_name": validated_data.get("last_name", ""),
            "language": validated_data["language"],
        }

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults=defaults,
        )

        if not created:
            user.phone_number = validated_data["phone_number"]
            user.first_name = validated_data.get("first_name", "")
            user.last_name = validated_data.get("last_name", "")
            user.language = validated_data["language"]
            user.save()

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "created": created,
        }

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

    @staticmethod
    @transaction.atomic
    def change_password(user, current_password, new_password):
        if not user.check_password(current_password):
            raise ValidationError("Current password is incorrect.")

        if current_password == new_password:
            raise ValidationError(
                "The new password must be different from the current password."
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return user

    @staticmethod
    def logout(refresh_token):
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            raise ValidationError("Invalid or expired refresh token.")


