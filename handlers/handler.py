from typing import Any, Dict, List, Optional, Tuple

from aiogram import Bot, Router
from aiogram.filters import Filter

from .message_handlers.handler import MessageHandlerABC


class NeuroApiRouter(Router):
    bot: Bot
    def __init__(self, *, name: str | None = None, bot: Bot) -> None:
        super().__init__(name=name)
        self.bot = bot

    def add_message_handler(self, callback: MessageHandlerABC, *args: Any):
        handler = callback(self.bot, *args)
        self.message.register(handler.handler, handler.filter)
        
    
    
class Handler:
    bot: Bot
    router: NeuroApiRouter

    def __init__(self, bot: Bot) -> None:
        assert isinstance(bot, Bot)
        self.bot = bot
        self.router = NeuroApiRouter(bot=bot)
    
    def __call__(self) -> NeuroApiRouter:
        return self.router
    
    def add_handlers(self, handlers: List[MessageHandlerABC] | List[Tuple[MessageHandlerABC] | Optional[Tuple[Any, ...]]]):
        for handler in handlers:
            if isinstance(handler, tuple):
                args = handler[1:] if len(handler)>1 else []
                self.router.add_message_handler(handler[0], *args)
            else:
                self.router.add_message_handler(handler)