from aiogram import types

from handlers.filters.reply_to_user import ReplyToUser

from .handler import MessageHandlerABC


class ReplyToUserCommand(MessageHandlerABC):
    """Send reply to user from admins"""
    filter = ReplyToUser()
    async def _command(self, message: types.Message):
        if message.reply_to_message.forward_from is None:
            await message.reply('Пользователь стесняшка и не разрешает отвечать на его сообщения...')
        else:
            try:
                await self.bot.send_message(message.reply_to_message.forward_from.id, f'Вам ответил админ:\n{message.text}', entities=message.entities)
                await message.reply('Ваше сообщение было отправлено!')
            except Exception as e:
                await message.reply(f'Ошибка! "{e}"')