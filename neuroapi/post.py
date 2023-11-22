from aiohttp import ClientSession, ClientResponse
from .enums import EGetAll
from .api_method import ApiMethod


class Post(ApiMethod):

    async def new(self, text: str, from_user_id: str, media_group_id: str):
        payload = {'text': text, 'from_user_id': from_user_id}
        if media_group_id != 'None':
            payload['media_group_id'] = media_group_id
        async with ClientSession() as session:
            response: ClientResponse = await session.post(self.api_url+'/post/new', data=payload)
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return data['status']

    async def __get_all(self, status: EGetAll):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-all/{status.value}')
        return response

    async def get_all(self):
        result = await self.__get_all(EGetAll.all)
        return await result.json()

    async def get_will_post(self):
        result = await self.__get_all(EGetAll.will_post)
        return await result.json()

    async def get_posted(self):
        result = await self.__get_all(EGetAll.posted)
        return await result.json()

    async def get(self, post_id: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get/{post_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return data

    async def get_by_media_group_id(self, media_group_id: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-by-media-group-id/{media_group_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return await response.json()