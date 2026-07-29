from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        EMPLOYEE = "employee", "Employee"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)

    telegram_id = models.BigIntegerField(
        unique=True,
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        default="",
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email

    LANGUAGE_CHOICES = [
        ("uz", "Uzbek"),
        ("ru", "Russian"),
    ]
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="uz",
    )
    
    loyalty_coins = models.PositiveIntegerField(
        default=0,
        help_text="Loyalty coins earned from orders"
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="User's date of birth for birthday vouchers"
    )