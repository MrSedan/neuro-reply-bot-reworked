from asyncio import create_task
from time import sleep
from typing import Any
from uuid import uuid4

from aiogram import types
from aiogram.filters import Filter
from sqlalchemy.orm import Session

from db.data import Admin, Image, Post, User, engine


class NewPostFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if message.media_group_id is None or message.content_type != 'photo':
            return False
        with Session(engine) as session:
            post = session.query(Post).filter(
                Post.media_group_id == message.media_group_id).first()
            if post is None:
                if not (message.caption.startswith('/newpost ') if message.caption else False):
                    return False
                new_post = Post(uuid=uuid4(), text=message.caption.replace(
                    '/newpost ', ''), media_group_id=message.media_group_id)
                post_user = session.get(Admin, message.from_user.id)
                new_post.user = post_user
                session.add(new_post)
                session.commit()
                
                await message.answer('Пост успешно добавлен!')
        return True


class NewSoloPostFilter(Filter):
    async def __call__(self, message: types.Message) -> bool:
        return message.media_group_id is None and message.content_type == 'photo' and message.caption.startswith('/newpost ')
