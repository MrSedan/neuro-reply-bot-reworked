from aiogram import types
from aiogram.filters import Filter


class ReplyToUser(Filter):
    async def __call__(self, message: types.Message) -> bool:
        if message.reply_to_message is None or message.chat.type != 'private':
            return False
        return True
