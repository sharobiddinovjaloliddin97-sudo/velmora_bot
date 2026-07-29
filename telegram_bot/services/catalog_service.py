from config import api


async def get_categories():
    data = await api.get("/catalog/categories/")
    return data["results"]