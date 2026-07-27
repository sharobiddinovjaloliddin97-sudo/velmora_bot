from django.db import models

from apps.users.models import User


class Loyalty(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="loyalty",
    )
    coins = models.PositiveIntegerField(default=0)
    vouchers = models.PositiveIntegerField(default=0)