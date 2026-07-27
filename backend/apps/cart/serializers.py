from rest_framework import serializers

from .models import Cart, CartItem

# Returns each product in the cart.
class CartItemSerializer(serializers.ModelSerializer):
    #Go through the product relationship and return its name
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    product_price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product",
            "product_name",
            "product_price",
            "quantity",
        )


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "user",
            "created_at",
            "updated_at",
        )