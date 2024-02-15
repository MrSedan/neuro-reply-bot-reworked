import asyncio
import logging
from typing import Coroutine

from aiogram import Bot, types
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from neuroapi import neuroapi
from neuroapi.config import GlobalConfig
from neuroapi.types import BotSettings

from .handler import MessageHandlerABC


class UpdateSettingsCommand(MessageHandlerABC):
    """Command to update settings manually or by timer"""
    settings: BotSettings
    post: Coroutine # async post command method to post posts to channel by timer
    filter = Command('update_settings')
    
    async def settings_and_schedule_checker(self):
            await self._auto_update_settings()
                
    async def _auto_update_settings(self):
        """
        An asynchronous function that updates settings and schedules jobs.
        """
        self.settings = await neuroapi.bot_settings.get()
        self.scheduler.remove_all_jobs()
        self.scheduler.add_job(self._auto_update_settings, 'interval', seconds=60) # Auto updating settings

        # TODO: Сделать в бэке и в боте, чтоб дни тоже можно было в настройках хранить
        for i in self.settings.message_times:
            self.scheduler.add_job(self.post, 'cron', day_of_week='mon-sun', hour=i.split(':')[0], minute=i.split(':')[1]) # Auto posting
        logging.debug(self.scheduler.get_jobs())
    
    def __init__(self, bot: Bot, post_command: Coroutine, *args) -> None:
        super().__init__(bot)
        self.post = post_command
        config = GlobalConfig()
        logging.debug(config)
        self.scheduler = AsyncIOScheduler(event_loop=asyncio.get_event_loop())
        self.scheduler.add_job(self.settings_and_schedule_checker, 'interval', seconds=60)
        self.scheduler.start()
    
    async def _command(self, mes: types.Message):
        """Clearing server cache and returning actual settings"""
        self.settings = await neuroapi.bot_settings.get_update()
        await mes.answer('Настройки обновлены')
        