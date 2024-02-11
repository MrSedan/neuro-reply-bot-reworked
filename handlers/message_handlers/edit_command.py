from aiogram import types
from aiogram.filters import Command

from neuroapi import neuroapi

from .handler import MessageHandlerABC


class EditCommand(MessageHandlerABC):
    filter = Command('edit')
    
    async def _command(self, message: types.Message):
        command = message.text.split(' ', 2)
        if len(command)<3:
            await message.reply('Недостаточно аргументов!')
            return
        try: 
            await neuroapi.post.edit_text_by_order_num(command[1], command[2], message.entities)
            #TODO: Message Entities для уведомления об изменении поста
            await message.reply(f'Текст поста успешно изменен на: {command[2]}')
        except Exception as e:
            await message.reply(f'Ошибка: {e}')