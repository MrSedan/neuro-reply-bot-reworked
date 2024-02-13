import json
from typing import List, Optional

from aiogram import types
from aiogram.types import MessageEntity
from aiohttp import ClientSession

from .api_method import ApiMethod


class Image(ApiMethod):
    async def add(self, from_id: str, file_id: str, has_spoiler: bool | None, message_id: int, text: str, media_group_id: str | None, message_entities: Optional[List[MessageEntity]], message: types.Message):
        payload = {'from_user_id': from_id, 'file_id': file_id,
                   'has_spoiler': has_spoiler, 'message_id': message_id }
        if text != '':
            payload['post_text'] = text.replace('/newpost ', '')
        if media_group_id != 'None' and media_group_id is not None:
            payload['media_group_id'] = media_group_id
        if message_entities is not None:
            mes_ent = list(map(lambda x: x.model_dump(), message_entities))
            arr =[]
            for item in mes_ent:
                if item['type'] == 'bot_command': continue
                item['offset'] -= 9
                arr.append(item)
            payload['message_entities'] = json.dumps(arr)
        if has_spoiler is None:
            payload.pop('has_spoiler')
        payload = json.dumps(payload)
        async with ClientSession() as session:
            response = await session.post(
                self.api_url+'/image/add', data=payload, headers={'Content-Type': 'application/json'})
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return data['created']
