from aiogram.filters import Command
from aiogram.types import Message

from neuroapi import neuroapi

from .handler import MessageHandlerABC


class DeletedPostsCommand(MessageHandlerABC):
    filter = Command('deleted')
    async def _command(self, message: Message):
        try:
            deleted_posts = await neuroapi.post.get_deleted_posts()
            if len(deleted_posts):
                s = "Удаленные посты:\n"
                for i, post in enumerate(deleted_posts):
                    s += f"{i+1}. {post.text}\n"
            else:
                s = "Нет удаленных постов"
            await message.answer(s)
        except Exception as e:
            await message.answer(f'Ошибка: {e}')