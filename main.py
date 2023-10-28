import asyncio
import logging
import os
import sys

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

async def main() -> None:
    dp.include_router(Admin_commands(bot)())
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())