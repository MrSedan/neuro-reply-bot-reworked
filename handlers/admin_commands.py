from aiogram import Bot

from handlers.handler import Handler
# Message handlers
from handlers.message_handlers.delete_command import DeleteCommand
from handlers.message_handlers.deleted_posts_command import DeletedPostsCommand
from handlers.message_handlers.edit_command import EditCommand
from handlers.message_handlers.info_command import InfoCommand
from handlers.message_handlers.newpost_command import (NewPostCommand,
                                                       NewPostSoloCommand)
from handlers.message_handlers.post_command import PostCommand
from handlers.message_handlers.preview_command import PreviewCommand
from handlers.message_handlers.reply_to_user import ReplyToUserCommand
from handlers.message_handlers.restore_command import RestoreCommand
from handlers.message_handlers.settings_command import SettingsCommand
from handlers.message_handlers.update_settings import UpdateSettingsCommand
# Middlewares
from handlers.middlewares.media_group import MediaGroupMiddleware
from handlers.middlewares.user import AdminMiddleware
from neuroapi.types import BotSettings as BotSettingsType


class AdminCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        """Initialize the group of admin commands"""
        super().__init__(bot)
        self.router.message.middleware(AdminMiddleware()) # Admin checking

        self.add_handlers([
            InfoCommand,
            (UpdateSettingsCommand, PostCommand(self.bot).handler),
            EditCommand,
            PostCommand,
            RestoreCommand,
            SettingsCommand,
        ])
        self.router.message.middleware(MediaGroupMiddleware()) # Media group handling
        self.add_handlers([
            NewPostCommand,
            NewPostSoloCommand,
            PreviewCommand,
            DeleteCommand,
            DeletedPostsCommand,
            ReplyToUserCommand
        ])
