from asyncio import create_task
from time import sleep
from typing import Any
from uuid import uuid4

from aiogram import types
from aiogram.filters import Filter
from sqlalchemy.orm import Session

from db.data import Admin, Image, Post, User, engine
from neuroapi import neuroapi


class NewPostFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if message.media_group_id is None or message.content_type != 'photo':
            return False
        try:
            await neuroapi.post.get_by_media_group_id(message.media_group_id)
        except:
            if not (message.caption.startswith('/newpost ') if message.caption else False):
                    return False
            await neuroapi.post.new(message.caption.replace(
                    '/newpost ', ''), str(message.from_user.id), str(message.media_group_id))
            await message.answer('Пост успешно добавлен!')
        return True


class NewSoloPostFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.media_group_id is None and message.content_type == 'photo' and message.caption and message.caption.startswith('/newpost ')


class ChangePosts(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.text and message.text.startswith("/change") and message.chat.type == 'private'
