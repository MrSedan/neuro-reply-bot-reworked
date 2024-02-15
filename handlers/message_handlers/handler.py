from abc import ABC, abstractmethod
from typing import Any, Coroutine, Dict

from aiogram import Bot
from aiogram.filters import Filter


class MessageHandlerABC(ABC):
    """Base class for all message handlers"""
    bot: Bot
    
    def __init__(self, bot: Bot, *args: Any, **kwargs: Dict[str, Any]) -> None:
        assert isinstance(bot, Bot)
        self.bot = bot
        
    @abstractmethod
    def _command(self, *args, **kwargs):
        """Handler for the command"""
        raise NotImplementedError
    
    @property
    def handler(self) -> Coroutine[None, None, None]:
        """Command handler method"""
        return self._command        
    
    @property
    @abstractmethod
    def filter(self) -> Filter:
        """Filter for the command"""
        raise NotImplementedError