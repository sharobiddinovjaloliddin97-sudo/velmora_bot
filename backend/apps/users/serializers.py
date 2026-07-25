from rest_framework import serializers

from .models import User
from .services import UserService
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

#Historically, Django was designed around username-based authentication.
#Nowadays, many applications use email instead.
#Since we're extending AbstractUser, we inherit username, first_name, and last_name.

# this serializer is for displaying data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #Passwords are hashed and should never be returned in API responses.
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
        )
        #This means clients can see these fields but cannot change them through this serializer.
        #This prevents a user from making themselves an admin through the API.
        read_only_fields = (
            "id",
            "role",
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



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    # no create() - because login validates credentials.
    def validate(self, attrs):
        return UserService.login(
            email=attrs["email"],
            password=attrs["password"],
        )