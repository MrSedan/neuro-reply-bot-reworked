from typing import Any, Dict, List, Optional, Tuple

from aiogram import Bot, Router
from aiogram.filters import Filter

from .message_handlers.handler import MessageHandlerABC


class NeuroApiRouter(Router):
    bot: Bot
    def __init__(self, *, name: str | None = None, bot: Bot) -> None:
        """
        Initializes a new instance of the class with the provided name and bot.

        Args:
            name (str, optional): The name of the instance. Defaults to None.
            bot (Bot): The bot instance.

        Returns:
            None
        """
        super().__init__(name=name)
        self.bot = bot

    def add_message_handler(self, callback: MessageHandlerABC, *args: Any):
        """
        Add a message handler to the bot.

        :param callback: The message handler callback.
        :param args: Additional arguments for the message handler.
        :return: None
        """
        handler = callback(self.bot, *args)
        self.message.register(handler.handler, handler.filter)
        
    
    
class Handler:
    bot: Bot
    router: NeuroApiRouter

    def __init__(self, bot: Bot) -> None:
        """
        Initializes the class with the given bot instance.

        Args:
            bot (Bot): The bot instance to be initialized with.

        Returns:
            None
        """
        assert isinstance(bot, Bot)
        self.bot = bot
        self.router = NeuroApiRouter(bot=bot)
    
    def __call__(self) -> NeuroApiRouter:
        return self.router
    
    def add_handlers(self, handlers: List[MessageHandlerABC] | List[Tuple[MessageHandlerABC] | Optional[Tuple[Any, ...]]]):
        """
        Add multiple message handlers to the router.

        Args:
            handlers (List[MessageHandlerABC] | List[Tuple[MessageHandlerABC] | Optional[Tuple[Any, ...]]]): The list of message handlers to be added.

        Returns:
            None
        """
        for handler in handlers:
            if isinstance(handler, tuple):
                args = handler[1:] if len(handler)>1 else []
                self.router.add_message_handler(handler[0], *args)
            else:
                self.router.add_message_handler(handler)