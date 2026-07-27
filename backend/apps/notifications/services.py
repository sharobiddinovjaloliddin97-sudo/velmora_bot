from .models import Notification


class NotificationService:
    @staticmethod
    def create_notification(user, title, message):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
        )

    @staticmethod
    def get_notifications(user):
        return Notification.objects.filter(
            user=user,
        ).order_by("-created_at")

    @staticmethod
    def mark_as_read(notification_id):
        notification = Notification.objects.get(
            id=notification_id,
        )

        notification.is_read = True
        notification.save()

        return notification