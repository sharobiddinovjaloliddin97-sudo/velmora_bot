from config import api


class OrderService:

    @staticmethod
    async def create_order(access_token: str):
        return await api.post(
            "orders/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def get_orders(access_token: str):
        data = await api.get(
            "orders/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )
        return data["results"]
        
    @staticmethod
    async def get_order(access_token: str, order_id: int):
        return await api.get(
            f"orders/{order_id}/",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )

    @staticmethod
    async def cancel_order(access_token: str, order_id: int):
        return await api.patch(
            f"orders/{order_id}/",
            data={
                "status": "Cancelled"
            },
            headers={
                "Authorization": f"Bearer {access_token}",
            },
        )