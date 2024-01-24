import json
from typing import List, Optional

import requests
from aiogram.types import MessageEntity
from aiohttp import ClientSession

import neuroapi.types as neuroTypes

from .api_method import ApiMethod
from .enums import EGetAll


class Post(ApiMethod):

    async def new(self, text: str, from_user_id: str, media_group_id: str = "None", message_entities: Optional[List[MessageEntity]] = None):
        payload = {'text': text, 'from_user_id': from_user_id}
        if media_group_id != 'None':
            payload['media_group_id'] = media_group_id
        if message_entities is not None:
            mes_ent = list(map(lambda x: x.model_dump(), message_entities))
            arr =[]
            for item in mes_ent:
                if item['type'] == 'bot_command': continue
                item['offset'] -= 9
                arr.append(item)
            payload['message_entities'] = json.dumps(arr)
        response = requests.post(self.api_url+'/post/new', data=payload)
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def __get_all(self, status: EGetAll):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-all/{status.value}')
        return response

    async def get_all(self):
        result = await self.__get_all(EGetAll.all)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get_will_post(self):
        result = await self.__get_all(EGetAll.will_post)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get_posted(self):
        result = await self.__get_all(EGetAll.posted)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get(self, post_id: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get/{post_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def get_by_media_group_id(self, media_group_id: str):
        response = requests.get(
            self.api_url+f'/post/get-by-media-group-id/{media_group_id}')
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def edit_text(self, post_id: str, text: str):
        response = requests.post(
            self.api_url+f"/post/edit/{post_id}", data={"text": text})
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def edit_text_by_order_num(self, order: str, text: str):
        response = requests.post(self.api_url + f"/post/edit-post-by-order-num/{order}", data={"text": text})
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)
    
    async def get_post_to_post(self):
        response = requests.get(self.api_url+f"/post/post")
        data = response.json()
        if 'statusCode' in data:
            if response.status_code==404:
                return None
            else:
                raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)