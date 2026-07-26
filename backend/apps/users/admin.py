from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

admin.site.register(User, UserAdmin)

#UserAdmin gives your custom User model the same rich admin interface that Django's default User model has.