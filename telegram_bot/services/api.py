import httpx


class APIClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, endpoint: str, params=None, headers=None):
        response = await self.client.get(
            endpoint,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data=None, headers=None):
        response = await self.client.post(
            endpoint,
            json=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def put(self, endpoint: str, data=None, headers=None):
        response = await self.client.put(
            endpoint,
            json=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def patch(self, endpoint: str, data=None, headers=None):
        response = await self.client.patch(
            endpoint,
            json=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    async def delete(self, endpoint: str, data=None, headers=None):
        response = await self.client.request(
            "DELETE",
            endpoint,
            json=data,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    