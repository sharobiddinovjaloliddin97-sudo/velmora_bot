from rest_framework import serializers

from apps.users.models import User
from .models import Loyalty


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
        )


class LoyaltySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Loyalty
        fields = "__all__"