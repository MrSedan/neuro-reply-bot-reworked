from aiogram import types
from aiogram.filters import Command

from neuroapi.types import BotSettings

from .handler import MessageHandlerABC


class SettingsCommand(MessageHandlerABC):
    filter = Command('settings')
    async def _command(self, message: types.Message):
        self.settings = BotSettings.get_instance()
        s = f"Текущие настройки:\n{self.settings.get_text()}"
        await message.answer(s)