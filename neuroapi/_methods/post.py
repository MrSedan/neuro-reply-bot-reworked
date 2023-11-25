import requests
from aiohttp import ClientSession

from .api_method import ApiMethod
from .enums import EGetAll
import neuroapi.types as nat


class Post(ApiMethod):

    async def new(self, text: str, from_user_id: str, media_group_id: str = "None"):
        payload = {'text': text, 'from_user_id': from_user_id}
        if media_group_id != 'None':
            payload['media_group_id'] = media_group_id
        response = requests.post(self.api_url+'/post/new', data=payload)
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return nat.Post.from_dict(data)

    async def __get_all(self, status: EGetAll):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-all/{status.value}')
        return response

    async def get_all(self):
        result = await self.__get_all(EGetAll.all)
        return [nat.Post.from_dict(post) for post in await result.json()]

    async def get_will_post(self):
        result = await self.__get_all(EGetAll.will_post)
        return [nat.Post.from_dict(post) for post in await result.json()]

    async def get_posted(self):
        result = await self.__get_all(EGetAll.posted)
        return [nat.Post.from_dict(post) for post in await result.json()]

    async def get(self, post_id: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get/{post_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return nat.Post.from_dict(data)

    async def get_by_media_group_id(self, media_group_id: str):
        response = requests.get(
            self.api_url+f'/post/get-by-media-group-id/{media_group_id}')
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return nat.Post.from_dict(data)

    async def edit_text(self, post_id: str, text: str):
        response = requests.post(
            self.api_url+f"/post/edit/{post_id}", data={"text": text})
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return nat.Post.from_dict(data)