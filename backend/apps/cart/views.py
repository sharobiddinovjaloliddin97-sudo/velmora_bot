from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import CartSerializer
from .services import CartService


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # we can give the url-name as well via @action
    @action(detail=False, methods=["get"])
    def my_cart(self, request):
        cart = CartService.get_cart(request.user)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_product(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        CartService.add_product(
            request.user,
            product_id,
            quantity,
        )

        return Response(
            {"detail": "Product added to cart."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["patch"])
    def update_quantity(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        CartService.update_quantity(
            request.user,
            product_id,
            quantity,
        )

        return Response(
            {"detail": "Cart updated successfully."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["delete"])
    def remove_product(self, request):
        product_id = request.data.get("product_id")

        CartService.remove_product(
            request.user,
            product_id,
        )

        return Response(
            {"detail": "Product removed from cart."},
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["delete"])
    def clear_cart(self, request):
        CartService.clear_cart(request.user)

        return Response(
            {"detail": "Cart cleared successfully."},
            status=status.HTTP_200_OK,
        )
    
    @action(detail=False, methods=["get"])
    def total(self, request):
        total = CartService.get_cart_total(request.user)

        return Response(
            {"total": total},
            status=status.HTTP_200_OK,
        )