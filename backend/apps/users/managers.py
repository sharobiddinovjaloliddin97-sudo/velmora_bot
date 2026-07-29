#A manager is responsible for talking to the database.

from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    # creates a regular user safely (checks email, hashes password, saves to DB).
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email) #formatting
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # hashes password
        user.save(using=self._db)  # The database this manager is currently using." used in multiple dbs

        # goes back to serializer.save()
        return user

   #creates an admin by calling create_user() and automatically enabling admin privileges.
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        return self.create_user(email, password, **extra_fields)