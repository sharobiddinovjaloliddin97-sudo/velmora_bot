from apps.catalog.models import Product

from .models import Cart, CartItem


class CartService:
    @staticmethod
    def get_cart(user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @staticmethod
    def add_product(user, product_id, quantity=1):
        cart = CartService.get_cart(user)
        product = Product.objects.get(id=product_id)

        #"Is this product already in the cart?"
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save()

        return item

    @staticmethod
    def update_quantity(user, product_id, quantity):
        cart = CartService.get_cart(user)

        item = CartItem.objects.get(
            cart=cart,
            product_id=product_id,
        )

        item.quantity = quantity
        item.save()

        return item

    @staticmethod
    def remove_product(user, product_id):
        cart = CartService.get_cart(user)

        CartItem.objects.filter(
            cart=cart,
            product_id=product_id,
        ).delete()

    @staticmethod
    def get_cart_total(user):
        cart = CartService.get_cart(user)

        total = 0

        for item in cart.items.all():
            total += item.product.price * item.quantity

        return total