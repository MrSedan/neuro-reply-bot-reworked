from typing import List

from aiogram import Bot, F, types
from aiogram.enums import ChatMemberStatus
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

from handlers.handler import Handler
from neuroapi import neuroapi
from neuroapi.types import Admin as AdminType
from neuroapi.types import BotSettings as BotSettingsType


class UserCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        
        @self.router.message(CommandStart())
        async def start_command(message: types.Message):
            await message.answer("Добро пожаловать! Данный бот - предложка для канала @neur0w0men. Отправляйте свои пожелания насчет нейрокартинок, а также свои картинки, а админы постараются заняться этим!\nДанный бот принимает текст, картинки, документы и стикеры.")
                
        @self.router.message(F.chat.type == 'private')
        async def forward_post(message: types.Message):
            self.settings = BotSettingsType.get_active()
            user = await bot.get_chat_member(self.settings.channel, message.from_user.id)
            if user is None:
                await message.reply('Ошибка')
                return
            user_in_channel = user.status == ChatMemberStatus.LEFT
            admins: List[AdminType] = await neuroapi.admin.get()
            canReply = True
            for admin in admins:
                bankeyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text='❌ Баннах', callback_data=f'ban {message.from_user.id}')                        
                    ]
                ])
                await bot.send_message(admin.user_id, f'Вам новое сообщение от пользователя {message.from_user.full_name}. ' +
                                       (f'\nНик: @{message.from_user.username}' if message.from_user.username else f'ID: {message.from_user.id}') + 
                                       f'\nПользователь{" не " if user_in_channel else " "}состоит в канале.', reply_markup=bankeyboard)
                try:
                    forwarded_message = await bot.forward_message(admin.user_id, message.chat.id, message.message_id)
                    if forwarded_message.forward_from is None:
                        canReply = False
                except:
                    pass
            await message.reply('Ваше сообщение было отправлено администраторам'+('' if canReply else '\nНо они не смогут вам ответить из-за ваших настроек конфиденциальности.'))
        
        @self.router.callback_query(lambda query: True)
        async def handle_button_click(callback_query: types.CallbackQuery):
            admins: List[AdminType] = await neuroapi.admin.get()
            callback_data = callback_query.data.split()
            unbankeyboard = types.InlineKeyboardMarkup(inline_keyboard=[
                    [
                        types.InlineKeyboardButton(text='✅ Пардон, мсье', callback_data=f'unban {callback_data[1]}')                        
                    ]
                ])
            for admin in admins:
                if callback_data[0] == 'ban':
                    try:
                        await neuroapi.user.ban(callback_data[1])
                        await bot.send_message(admin.user_id, f'Великий банхаммер покарал пользователя {callback_data[1]}.', reply_markup=unbankeyboard)
                    except Exception as ex: 
                        await bot.answer_callback_query(callback_query.id, f'Не смог забанить, {ex}')
                        pass
                    await bot.answer_callback_query(callback_query.id)
                if callback_data[0] == 'unban':
                    try:
                         await bot.send_message(admin.user_id, f'Великий банхаммер пощадил пользователя {callback_data[1]}.')
                    except:
                        await neuroapi.user.unban(callback_data[1])
                        await bot.answer_callback_query(callback_query.id, f'Банхаммер не прощает, {ex}')
                        pass
                    await bot.answer_callback_query(callback_query.id)