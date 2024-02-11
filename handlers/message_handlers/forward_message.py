from typing import List

from aiogram import F, types
from aiogram.enums import ChatMemberStatus

from neuroapi import neuroapi
from neuroapi.types import Admin as AdminType
from neuroapi.types import BotSettings

from .handler import MessageHandlerABC


class ForwardMessageCommand(MessageHandlerABC):
    filter = F.chat.type == 'private'
    async def _command(self, message: types.Message):
        self.settings = BotSettings.get_instance()
        user = await self.bot.get_chat_member(self.settings.channel, message.from_user.id)
        if user is None:
            await message.reply('Ошибка')
            return
        user_in_channel = user.status == ChatMemberStatus.LEFT
        admins: List[AdminType] = await neuroapi.admin.get()
        canReply = True
        for admin in admins:
            await self.bot.send_message(admin.user_id, f'Вам новое сообщение от пользователя {message.from_user.full_name}. ' +
                                    (f'\nНик: @{message.from_user.username}' if message.from_user.username else f'ID: {message.from_user.id}') + 
                                    f'\nПользователь{" не " if user_in_channel else " "}состоит в канале')
            try:
                forwarded_message = await self.bot.forward_message(admin.user_id, message.chat.id, message.message_id)
                if forwarded_message.forward_from is None:
                    canReply = False
            except:
                pass
        await message.reply('Ваше сообщение было отправлено администраторам'+('' if canReply else '\nНо они не смогут вам ответить из-за ваших настроек конфиденциальности.'))