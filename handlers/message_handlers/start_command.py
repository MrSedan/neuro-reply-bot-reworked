from aiogram import types
from aiogram.filters import CommandStart

from .handler import MessageHandlerABC


class StartCommand(MessageHandlerABC):
    filter = CommandStart()
    
    async def _command(self, message: types.Message):
        await message.answer("Добро пожаловать! Данный бот - предложка для канала @neur0w0men. Отправляйте свои пожелания насчет нейрокартинок, а также свои картинки, а админы постараются заняться этим!\nДанный бот принимает текст, картинки, документы и стикеры.")
        