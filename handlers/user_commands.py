from typing import Any
from aiogram import Bot, Router, types, F
from sqlalchemy.orm import Session

from db.data import Admin, Image, Post, Admin, engine


class User_commands:
    bot: Bot
    router: Router

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.router = Router()

        @self.router.message(F.chat.type == 'private')
        async def forward_post(message: types.Message):

            with Session(engine) as session:
                admins = session.query(Admin).all()
                canReply = True
                for a in admins:
                    await bot.send_message(a.user_id, f'Вам новое сообщение от пользователя {message.from_user.full_name}. ' +
                                           (f'\nНик: @{message.from_user.username}' if message.from_user.username else f'ID: {message.from_user.id}'))
                    forwarded_message = await bot.forward_message(a.user_id, message.chat.id, message.message_id)
                    if forwarded_message.forward_from is None:
                        canReply = False
                await message.reply('Ваше сообщение было отправлено администраторам'+('' if canReply else '\nНо они не смогут вам ответить из-за ваших настроек конфиденциальности.'))

    def __call__(self, *args: Any, **kwds: Any) -> Router:
        return self.router


def setup(bot: Bot) -> Router:
    return User_commands(bot)()
