from rest_framework import serializers

from .models import Category, Product, ProductImage

# Converts Category objects to/from JSON.
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("id", "image", "is_primary")


class ProductSerializer(serializers.ModelSerializer):
    #Includes all images of a product.
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"