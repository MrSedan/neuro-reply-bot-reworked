from datetime import datetime

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.filters.proxy_status import ProxyStatusFilter

from ..handler import MessageHandlerABC


class ProxyStatusCallback(MessageHandlerABC):
    filter = ProxyStatusFilter()
    async def _command(self, data: types.CallbackQuery):
        builder = InlineKeyboardBuilder()
        builder.button(text="Обновить статус🔄", callback_data="refresh_proxy_status")
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        await self.bot.edit_message_text(f'{date} - Работаит', data.message.chat.id, data.message.message_id, reply_markup=builder.as_markup())