from aiogram import Bot, Dispatcher

from handlers.handler import Handler


class NeuroApiBot:
    bot: Bot
    dp: Dispatcher
    
    _instances = {}
    
    def __init__(self, token: str) -> None:
        self.bot = Bot(token)
        self.dp = Dispatcher()
    
    def __new__(cls, token: str) -> 'NeuroApiBot':
        assert isinstance(token, str)
        if token not in cls._instances:
            cls._instances[token] = super(NeuroApiBot, cls).__new__(cls)
        return cls._instances[token]
    
    def include_router(self, *routerClasses: Handler) -> None:
        for routerClass in routerClasses:
            assert issubclass(routerClass, Handler)
            self.dp.include_routers(routerClass(self.bot)())
        
    async def start(self, skip_updates=True):
        await self.dp.start_polling(self.bot, skip_updates=skip_updates)