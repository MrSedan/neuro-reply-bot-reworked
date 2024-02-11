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
        token_data = Token(token=token)
        self.bot = Bot(token_data.token)
        self.dp = Dispatcher(storage=storage)
    
    def __new__(cls, token: str, storage: RedisStorage | None = None) -> 'NeuroApiBot':
        token_data = Token(token=token)
        if token_data.token not in cls._instances:
            cls._instances[token_data.token] = super(NeuroApiBot, cls).__new__(cls)
        return cls._instances[token_data.token]
    
    def include_router(self, *routerClasses: Handler) -> None:
        for routerClass in routerClasses:
            assert issubclass(routerClass, Handler)
            self.dp.include_routers(routerClass(self.bot)())
        
    async def start(self, skip_updates=True):
        await self.dp.start_polling(self.bot, skip_updates=skip_updates)