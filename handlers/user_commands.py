from typing import Any, List

from aiogram import Bot, F, Router, types

from neuroapi import neuroapi

from neuroapi.types import Admin as AdminType


class User_commands:
    bot: Bot
    router: Router

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.router = Router()

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

    def __call__(self, *args: Any, **kwds: Any) -> Router:
        return self.router


def setup(bot: Bot) -> Router:
    return User_commands(bot)()
