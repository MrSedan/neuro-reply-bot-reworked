from typing import List

from aiogram import Bot, F, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command, CommandStart

from handlers.handler import Handler
from neuroapi import neuroapi
from neuroapi.types import Admin as AdminType
from neuroapi.types import BotSettings as BotSettingsType


class UserCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        
        @self.router.message(CommandStart())
        async def start_command(message: types.Message):
            await message.answer("Добро пожаловать! Данный бот - предложка для канала @neur0w0men. Отправляйте свои пожелания насчет нейрокартинок, а также свои картинки, а админы постараются заняться этим!\nДанный бот принимает текст, картинки, документы и стикеры.")
                
        @self.router.message(F.chat.type == 'private')
        async def forward_post(message: types.Message):
            self.settings = BotSettingsType.get_active()
            user = await bot.get_chat_member(self.settings.channel, message.from_user.id)
            if user is None:
                await message.reply('Ошибка')
                return
            user_in_channel = user.status == ChatMemberStatus.LEFT
            admins: List[AdminType] = await neuroapi.admin.get()
            canReply = True
            for admin in admins:
                await bot.send_message(admin.user_id, f'Вам новое сообщение от пользователя {message.from_user.full_name}. ' +
                                       (f'\nНик: @{message.from_user.username}' if message.from_user.username else f'ID: {message.from_user.id}') + 
                                       f'\nПользователь{" не " if user_in_channel else " "}состоит в канале')
                try:
                    forwarded_message = await bot.forward_message(admin.user_id, message.chat.id, message.message_id)
                    if forwarded_message.forward_from is None:
                        canReply = False
                except:
                    pass
            await message.reply('Ваше сообщение было отправлено администраторам'+('' if canReply else '\nНо они не смогут вам ответить из-за ваших настроек конфиденциальности.'))
