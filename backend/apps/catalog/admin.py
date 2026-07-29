from django.contrib import admin

from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_uz",
        "name_ru",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name_uz",
        "name_ru",
    )
    prepopulated_fields = {
        "slug": ("name_uz",),
    }


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name_uz",
        "name_ru",
        "category",
        "price",
        "stock",
        "is_active",
    )
    list_filter = (
        "category",
        "is_active",
    )
    search_fields = (
        "name_uz",
        "name_ru",
    )
    prepopulated_fields = {
        "slug": ("name_uz",),
    }
    inlines = [ProductImageInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
        "is_primary",
    )