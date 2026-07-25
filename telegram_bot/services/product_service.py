class ProductService:

    @staticmethod
    async def get_products(category: str):
        products = {
            "Pizza": [
                "Pepperoni",
                "Margarita",
                "BBQ Chicken",
            ],
            "Burger": [
                "Cheeseburger",
                "Double Burger",
            ],
            "Drinks": [
                "Coca-Cola",
                "Fanta",
            ],
        }

        return products.get(category, [])

    