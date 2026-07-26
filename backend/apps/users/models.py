from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager

class User(AbstractUser):

    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        EMPLOYEE = "employee", "Employee"
        ADMIN = "admin", "Admin"


    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    USERNAME_FIELD = "email"  # loginda avval username so'ragan bo'sa endi email so'redi
    REQUIRED_FIELDS = ["username"] # superuser yaratyotganda username ham so'ra

    objects = UserManager() # use the custom manager instead default

    def __str__(self):
        return self.email