from typing import List

from aiogram import Bot, F, types
from aiogram.filters import CommandStart

from handlers.handler import Handler
from neuroapi import neuroapi
from neuroapi.types import Admin as AdminType


class UserCommands(Handler):

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        
        @self.router.message(CommandStart())
        async def start_command(message: types.Message):
            await message.answer("Добро пожаловать! Данный бот - предложка для канала @neur0w0men. Отправляйте свои пожелания насчет нейрокартинок, а также свои картинки, а админы постараются заняться этим!\nДанный бот принимает текст, картинки, документы и стикеры.")
        
        @self.router.message(F.chat.type == 'private')
        async def forward_post(message: types.Message):
            admins: List[AdminType] = await neuroapi.admin.get()
            canReply = True
            for admin in admins:
                await bot.send_message(admin.user_id, f'Вам новое сообщение от пользователя {message.from_user.full_name}. ' +
                                       (f'\nНик: @{message.from_user.username}' if message.from_user.username else f'ID: {message.from_user.id}'))
                forwarded_message = await bot.forward_message(admin.user_id, message.chat.id, message.message_id)
                if forwarded_message.forward_from is None:
                    canReply = False
            await message.reply('Ваше сообщение было отправлено администраторам'+('' if canReply else '\nНо они не смогут вам ответить из-за ваших настроек конфиденциальности.'))

