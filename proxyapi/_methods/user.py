from aiohttp import ClientSession

import proxyapi.types as proxyTypes

from neuroapi._methods.api_method import ApiMethod


class User(ApiMethod):

    async def new_user(self, user_name: str, description: str, link: str, user_id: str):
        payload = {'userName': user_name, 'description': description,
                   'link': link, 'user_id': user_id}
        async with ClientSession() as session:
            response = await session.post(self.api_url+'/proxy/new-user', data=payload)
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return proxyTypes.User.from_dict(data)

    async def get_user(self, user_name: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/proxy/get-user/{user_name}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return proxyTypes.User.from_dict(data)

    async def get_all_users(self):
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/proxy/get-all-users')
        return [proxyTypes.User.from_dict(data) for data in await response.json()]
