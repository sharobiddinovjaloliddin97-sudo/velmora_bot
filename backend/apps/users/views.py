from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, ChangePasswordSerializer, LogoutSerializer


# CreateAPIView creates db object
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  #When a request arrives, use RegisterSerializer

    # Normally, CreateAPIView already has a create() implementation.
    #We're overriding it because we want to return a different serializer.
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # this save() goes to serializer - create() ->
        # then comes back from UserManager as saved user
        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

# doesn't create a database record.
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data) # creates LoginSerializer
        serializer.is_valid(raise_exception=True)  # calls LoginSerializer.validate()

        data = serializer.validated_data  # Convert the user to JSON

        return Response(
            {
                "user": UserSerializer(data["user"]).data,
                "access": data["access"],
                "refresh": data["refresh"],
            },
            status=status.HTTP_200_OK,
        )

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # is_valid() - triggers validate() in serializer
        serializer.is_valid(raise_exception=True)

        # ---View's only responsibility is to return an HTTP response.
        return Response(
            {"detail": "Password changed successfully."},
            status=status.HTTP_200_OK,
        )

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            {"detail": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )
# RegisterSerializer is designed for input.
# UserSerializer is designed for output.