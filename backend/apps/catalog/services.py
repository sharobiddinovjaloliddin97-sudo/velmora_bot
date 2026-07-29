from .models import Category, Product
from django.shortcuts import get_object_or_404

class CatalogService:

    @staticmethod
    def get_categories():
        return Category.objects.filter(is_active=True)

    @staticmethod
    def get_products(category=None):
        queryset = Product.objects.filter(is_active=True)

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset

#Returns one active product by its slug.
    @staticmethod
    def get_product_by_slug(slug):
        return get_object_or_404(
            Product,
            slug=slug,
            is_active=True,
        )