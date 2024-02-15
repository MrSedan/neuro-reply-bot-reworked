from aiogram import Bot

from handlers.handler import Handler
from handlers.message_handlers.forward_message import ForwardMessageCommand
from handlers.message_handlers.start_command import StartCommand
from neuroapi.types import BotSettings as BotSettingsType


class UserCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        """Initialize the group of user commands"""
        super().__init__(bot)
        
        self.add_handlers([
            StartCommand,
            ForwardMessageCommand
        ])