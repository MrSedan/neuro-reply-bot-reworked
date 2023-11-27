from typing import Any

from aiogram import Bot, Router


class Handler:
    bot: Bot
    router: Router

    def __init__(self, bot: Bot) -> None:
        assert isinstance(bot, Bot)
        self.bot = bot
        self.router = Router()
    
    def __call__(self) -> Router:
        return self.router