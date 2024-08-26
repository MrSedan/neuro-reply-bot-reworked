import json
import os

from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from neuroapi import neuroapi

from ..handler import MessageHandlerABC


class ProxyStartCommand(MessageHandlerABC):
    filter = CommandStart()
    async def _command(self, message: Message):
        builder = InlineKeyboardBuilder()
        builder.button(text="Статус прокси📝", callback_data="proxy_status")
        is_admin = await neuroapi.admin.is_admin(message.from_user.id)
        if is_admin:
            builder.button(text="Всё плохо", callback_data="proxy_disable")
        
        markup = None # builder.as_markup()
        
        #TODO: Users to send list
        users = dict()
        
        if os.path.exists('users.json'):
            with open('users.json', 'r') as f:
                users = json.load(f)['users']
        else:
            with open('users.json', 'w+') as f:
                json.dump({'users': [message.from_user.id]}, f)
        
        
            
            
        
        await message.answer('Приветствуем, теперь вы будете получать оповещения о статусе прокси.', reply_markup=markup)