from aiogram import Bot

from handlers.handler import Handler
from handlers.message_handlers.proxy.proxy_status_command import \
    ProxyStatusCallback
from handlers.message_handlers.proxy.refresh_proxy_status_command import \
    RefreshProxyStatusCallback
from handlers.message_handlers.proxy.start_command import ProxyStartCommand
from neuroapi.types import BotSettings as BotSettingsType


class ProxyCommands(Handler):
    settings: BotSettingsType
    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.add_handlers([ProxyStartCommand])
        self.add_callback_handlers([ProxyStatusCallback, RefreshProxyStatusCallback])