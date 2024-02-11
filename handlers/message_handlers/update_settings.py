import asyncio
from typing import Coroutine

import aioschedule as schedule
from aiogram import Bot, types
from aiogram.filters import Command

from neuroapi import neuroapi
from neuroapi.types import BotSettings

from .handler import MessageHandlerABC


class UpdateSettingsCommand(MessageHandlerABC):
    settings: BotSettings
    post: Coroutine
    filter = Command('update_settings')
    
    async def settings_and_schedule_checker(self):
            await self._command()
            while 1:
                await schedule.run_pending()
                await asyncio.sleep(1)
    
    def __init__(self, bot: Bot, post_command: Coroutine, *args) -> None:
        super().__init__(bot)
        self.post = post_command
        asyncio.create_task(self.settings_and_schedule_checker())
    
    async def _command(self, mes: types.Message | None = None):
        self.settings = await neuroapi.bot_settings.get()
        schedule.clear()
        schedule.every().minute.do(self._command, None)

        # TODO: Сделать в бэке и в боте, чтоб дни тоже можно было в настройках хранить
        for i in self.settings.message_times:
            schedule.every().monday.at(i).do(self.post, None)
            schedule.every().tuesday.at(i).do(self.post, None)
            schedule.every().wednesday.at(i).do(self.post, None)
            schedule.every().thursday.at(i).do(self.post, None)
            schedule.every().friday.at(i).do(self.post, None)
            schedule.every().sunday.at(i).do(self.post, None)
        if mes:
            await mes.answer('Настройки обновлены!')
        