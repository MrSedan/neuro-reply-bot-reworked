from aiogram import Bot

from handlers.handler import Handler
from handlers.message_handlers.delete_command import DeleteCommand
from handlers.message_handlers.edit_command import EditCommand
from handlers.message_handlers.info_command import InfoCommand
from handlers.message_handlers.newpost_command import (NewPostCommand,
                                                       NewPostSoloCommand)
from handlers.message_handlers.post_command import PostCommand
from handlers.message_handlers.preview_command import PreviewCommand
from handlers.message_handlers.reply_to_user import ReplyToUserCommand
from handlers.message_handlers.settings_command import SettingsCommand
from handlers.message_handlers.update_settings import UpdateSettingsCommand
from handlers.middlewares.media_group import MediaGroupMiddleware
from handlers.middlewares.user import AdminMiddleware
from neuroapi.types import BotSettings as BotSettingsType


class AdminCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.router.message.middleware(AdminMiddleware())

        self.add_handlers([
            InfoCommand,
            (UpdateSettingsCommand, PostCommand(self.bot).handler),
            EditCommand,
            PostCommand,
            SettingsCommand,
        ])
        self.router.message.middleware(MediaGroupMiddleware())
        self.add_handlers([
            NewPostCommand,
            NewPostSoloCommand,
            PreviewCommand,
            DeleteCommand,
            ReplyToUserCommand
        ])
