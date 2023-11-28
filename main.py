import asyncio
import logging
import signal
import sys

import aiohttp

from handlers.admin_commands import AdminCommands
from handlers.user_commands import UserCommands
from neuroapi.config import Config
from neuroapi.types import NeuroApiBot

# import aioschedule as schedule


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
    for i in range(5):
        print(f'Checking connectivity to backend ({i+1}/5)...')
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(Config().api_url+'/ping')
                data = str(await response.content.read(), encoding='utf-8')
                if data == 'pong':
                    print('Successfully connected to backend')
                    break
                else:
                    raise TimeoutError()
        except:
            print('Error! Waiting 3 secs and retrying...')
            await asyncio.sleep(3)
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