import asyncio
import logging
import platform
import signal
import sys

import aiohttp

from handlers.admin_commands import AdminCommands
from handlers.user_commands import UserCommands
from neuroapi.config import GlobalConfig as Config
from neuroapi.types import NeuroApiBot


async def delay_bot()->None:
    if Config().token is None: 
        logging.warning('Delay bot needs token in environment')
        return
    bot = NeuroApiBot(Config().token)
    bot.include_router(AdminCommands, UserCommands)
    await bot.start()

async def proxy_bot()->None:
    if Config().proxy_token is None: 
        logging.warning('Proxy bot needs token in environment')
        return
    bot = NeuroApiBot(Config().proxy_token)
    bot.include_router()
    await bot.start()

async def main() -> None:
    for i in range(5):
        logging.warning(f'Checking connectivity to backend ({i+1}/5)...')
        try:
            async with aiohttp.ClientSession() as session:
                response = await session.get(Config().api_url+'/ping')
                data = str(await response.content.read(), encoding='utf-8')
                if data == 'pong':
                    logging.warning('Successfully connected to backend')
                    break
                else:
                    raise TimeoutError()
        except:
            logging.error('Waiting 3 secs and retrying...')
            await asyncio.sleep(3)
    tasks = [asyncio.create_task(delay_bot()), asyncio.create_task(proxy_bot())]
    await asyncio.gather(*tasks)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING, stream=sys.stdout, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d.%m.%Y %H:%M:%S')
    loop = asyncio.get_event_loop()
    if platform.system() == 'Windows':
        try:
            loop.run_until_complete(main())
        except KeyboardInterrupt:
            logging.error("KeyboardInterrupt occurred")
        finally:
            loop.close()
    else: 
        for signame in ('SIGINT', 'SIGTERM'):
            loop.add_signal_handler(getattr(signal, signame), loop.stop)
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            pass