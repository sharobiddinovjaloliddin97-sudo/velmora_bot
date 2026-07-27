from django.contrib import admin

from .models import Loyalty


@admin.register(Loyalty)
class LoyaltyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "coins",
        "vouchers",
    )
    search_fields = (
        "user__email",
        "user__username",
    )