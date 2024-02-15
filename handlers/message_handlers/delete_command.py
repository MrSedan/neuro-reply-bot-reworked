from aiogram.filters import Command
from aiogram.types import Message

from neuroapi import neuroapi

from .handler import MessageHandlerABC


class DeleteCommand(MessageHandlerABC):
    """Command to delete posts"""
    filter = Command('delete')
    async def _command(self, message: Message):
        text = message.text.split()
        if len(text)!=2:
            await message.answer('Неверное количество аргументов')
            return
        try:
            await neuroapi.post.delete_by_order(text[1])
        except Exception as e:
            await message.answer(f'Ошибка {e}')
            return
        await message.answer('Пост удален')