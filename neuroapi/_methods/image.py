import json
from typing import List, Optional

from aiogram import types
from aiogram.types import MessageEntity
from aiohttp import ClientSession

from .api_method import ApiMethod


class Image(ApiMethod):
    """Class for Image API methods"""
    async def add(self, from_id: str, file_id: str, has_spoiler: bool | None, message_id: int, text: str, media_group_id: str | None, message_entities: Optional[List[MessageEntity]], message: types.Message):
        """
        An asynchronous function to add an image to post, along with its metadata, to a specific API endpoint. Also, creates a new post.

        Args:
            from_id (str): The ID of the user who sent the image.
            file_id (str): The ID of the file containing the image.
            has_spoiler (bool | None): A boolean indicating whether the image has spoiler content.
            message_id (int): The ID of the message containing the image.
            text (str): The text associated with the image.
            media_group_id (str | None): The ID of the media group containing the image, if applicable.
            message_entities (Optional[List[MessageEntity]]): A list of message entities associated with the image.
            message (types.Message): The message object associated with the image.

        Returns:
            None
        """
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
