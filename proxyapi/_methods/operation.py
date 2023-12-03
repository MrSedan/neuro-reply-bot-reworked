from aiohttp import ClientSession

import proxyapi.types as proxyTypes

from neuroapi._methods.api_method import ApiMethod


class Operation(ApiMethod):

    async def add(self, user_name: str):
        payload = {'userName': user_name}
        async with ClientSession() as session:
            response = await session.post(
                self.api_url+'/proxy/operation/add', data=payload)
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return proxyTypes.Operation.from_dict(data)

    async def get(self, user_name: str):
        async with ClientSession() as session:
            response = await session.get(
                self.api_url + f'/proxy/operation/get/{user_name}')
        return [proxyTypes.Operation.from_dict(data) for data in await response.json()]

    async def get_all(self):
        async with ClientSession() as session:
            response = await session.get(
                self.api_url + f'/proxy/operation/get-all')
        return [proxyTypes.Operation.from_dict(data) for data in await response.json()]
