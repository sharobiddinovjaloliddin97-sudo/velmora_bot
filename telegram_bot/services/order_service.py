class OrderService:

    @staticmethod
    async def create_order(products):
        return {
            "id": 1,
            "products": products,
            "status": "Pending",
        }