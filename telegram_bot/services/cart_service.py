cart = []


class CartService:

    @staticmethod
    async def add_product(product_name: str):
        cart.append(product_name)

    @staticmethod
    async def get_cart():
        return cart

    @staticmethod
    async def clear_cart():
        cart.clear()