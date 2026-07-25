import httpx


class APIClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, endpoint: str, params=None):
        response = await self.client.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data=None):
        response = await self.client.post(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, data=None):
        response = await self.client.put(endpoint, json=data)
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str):
        response = await self.client.delete(endpoint)
        response.raise_for_status()
        return response.json()