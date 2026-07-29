from config import api


class CartService:

    @staticmethod
    async def add_product(access_token: str, product_id: int, quantity: int = 1):
        return await api.post(
            "cart/add_product/",
            data={
                "product_id": product_id,
                "quantity": quantity,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def get_cart(access_token: str):
        return await api.get(
            "cart/my_cart/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def update_quantity(access_token: str, product_id: int, quantity: int):
        return await api.patch(
            "cart/update_quantity/",
            data={
                "product_id": product_id,
                "quantity": quantity,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def remove_product(access_token: str, product_id: int):
        return await api.delete(
            "cart/remove_product/",
            data={
                "product_id": product_id,
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def get_total(access_token: str):
        return await api.get(
            "cart/total/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def clear_cart(access_token: str):
        return await api.delete(
            "cart/clear_cart/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )