import asyncio
import logging
import os
import sys
from os.path import dirname, join

import aioschedule as schedule
import dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.admin_commands import Admin_commands

dotenv.load_dotenv()

token = os.getenv('TOKEN')

bot = Bot(token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer('Абоба')

handlers_dir = join(dirname(__file__), 'handlers')

for filename in os.listdir(handlers_dir):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        setup = __import__(f"handlers.{module_name}", locals(), globals(), ['setup']).setup
        dp.include_router(setup(bot))


async def main() -> None:
    # dp.include_router(Admin_commands(bot)())
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())