import asyncio
import logging
import signal
import sys

# import aioschedule as schedule
from aiogram import Bot, Dispatcher

from handlers.admin_commands import AdminCommands
from handlers.handler import Handler
from handlers.user_commands import UserCommands
from neuroapi.config import Config


class NeuroApiBot:
    bot: Bot
    dp: Dispatcher
    
    _instances = {}
    
    def __init__(self, token: str) -> None:
        self.bot = Bot(token)
        self.dp = Dispatcher()
        self._instances
    
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

async def delay_bot()->None:
    if Config().token is None: 
        print('Delay bot needs token in environment')
        return
    bot = NeuroApiBot(Config().token)
    bot.include_router(AdminCommands, UserCommands)
    await bot.start()

async def proxy_bot()->None:
    if Config().proxy_token is None: 
        print('Proxy bot needs token in environment')
        return
    bot = NeuroApiBot(Config().proxy_token)
    bot.include_router()
    await bot.start()

async def main() -> None:
    tasks = [asyncio.create_task(delay_bot()), asyncio.create_task(proxy_bot())]
    await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), loop.stop)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass