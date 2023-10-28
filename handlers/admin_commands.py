from typing import Any

from aiogram import Bot, F, Router, types
from aiogram.filters import Command

from handlers.middlewares.user import AdminMiddleware


class Admin_commands:
    bot: Bot
    router: Router
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.router = Router()
        self.router.message.middleware(AdminMiddleware())
        
        @self.router.message(Command('info'))
        async def info_command(message: types.Message):
            await message.answer('Тест')
    
    def __call__(self, *args: Any, **kwds: Any) -> Router:
        return self.router