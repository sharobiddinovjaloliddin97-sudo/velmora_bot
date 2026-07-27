from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import NotificationSerializer
from .services import NotificationService


class NotificationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def my_notifications(self, request):
        notifications = NotificationService.get_notifications(
            request.user,
        )

        serializer = NotificationSerializer(
            notifications,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def mark_as_read(self, request):
        notification_id = request.data.get(
            "notification_id",
        )

        notification = NotificationService.mark_as_read(
            notification_id,
        )

        serializer = NotificationSerializer(
            notification,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )