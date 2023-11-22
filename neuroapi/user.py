from aiohttp import ClientSession
from .api_method import ApiMethod


class User(ApiMethod):
    async def get(self, id: str, username: str):
        payload = {'id': id, 'username': username}
        async with ClientSession() as session:
            response = await session.post(
                self.api_url+'/user/get', data=payload)
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
