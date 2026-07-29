from config import api


class ProductService:

    @staticmethod
    async def get_products(category_id: int):
        data = await api.get(f"/catalog/products/?category={category_id}")
        return data["results"]