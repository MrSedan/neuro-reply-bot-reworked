from aiogram.filters import Command
from aiogram.types import Message

from neuroapi import neuroapi

from .handler import MessageHandlerABC


class RestoreCommand(MessageHandlerABC):
    filter = Command('restore')
    async def _command(self, message: Message):
        try:
            command = message.text.split()
            if len(command) != 2:
                raise Exception('Неверное количество аргументов')
            order = command[1]
            await neuroapi.post.restore_post(order)
            await message.answer('Пост восстановлен')
        except Exception as e:
            await message.answer(f'Ошибка: {e}')