from apps.cart.models import Cart
from apps.catalog.models import Product

from .models import Order, OrderItem


class OrderService:
    @staticmethod
    def create_order(user):
        cart = Cart.objects.get(user=user)

        # Creates an empty order.
        order = Order.objects.create(
            user=user,
        )

        total = 0

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

            total += item.product.price * item.quantity

        order.total_price = total
        order.save()

        cart.items.all().delete()

        return order