from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from pydantic import BaseModel

from handlers.handler import Handler


class Token(BaseModel):
    token: str

class NeuroApiBot:
    bot: Bot
    dp: Dispatcher
    
    _instances = {}
    
    def __init__(self, token: str, storage: RedisStorage | None = None) -> None:
        """
        Initializes the class with the provided token and optional RedisStorage object.
        
        Args:
            token (str): The token for the bot.
            storage (RedisStorage | None, optional): The RedisStorage object for storing data. Defaults to None.
        
        Returns:
            None
        """
        token_data = Token(token=token)
        self.bot = Bot(token_data.token)
        self.dp = Dispatcher(storage=storage)
    
    def __new__(cls, token: str, storage: RedisStorage | None = None) -> 'NeuroApiBot':
        """
        Create a new instance of NeuroApiBot, using the provided token and optional storage. Return bot if its created early with this token
        
        Args:
            cls: The class itself.
            token (str): The token for the instance.
            storage (RedisStorage | None, optional): The optional storage for the instance. Defaults to None.
        
        Returns:
            'NeuroApiBot': The instance of NeuroApiBot.
        """
        token_data = Token(token=token)
        if token_data.token not in cls._instances:
            cls._instances[token_data.token] = super(NeuroApiBot, cls).__new__(cls)
        return cls._instances[token_data.token]
    
    def include_router(self, *routerClasses: Handler) -> None:
        """
        Include the given router classes in the dispatcher.
        
        Parameters:
            *routerClasses (Handler): The router classes to include.
            
        Returns:
            None
        """
        for routerClass in routerClasses:
            assert issubclass(routerClass, Handler)
            self.dp.include_routers(routerClass(self.bot)())
        
    async def start(self, skip_updates=True):
        """
        Starts the bot by calling the `start_polling` method of the `dp` object.

        :param skip_updates: A boolean indicating whether to skip updates or not. Defaults to True.
        :type skip_updates: bool

        :return: None
        :rtype: None
        """
        await self.dp.start_polling(self.bot, skip_updates=skip_updates)