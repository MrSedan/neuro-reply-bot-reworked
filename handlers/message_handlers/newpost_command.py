from aiogram import types

import neuroapi.types as neuroTypes
from handlers.filters.new_post import NewPostFilter, NewSoloPostFilter
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class NewPostCommand(MessageHandlerABC):
    filter = NewPostFilter()
    async def _command(self, message: types.Message):
        created = await neuroapi.image.add(str(message.from_user.id), message.photo[-1].file_id, message.has_media_spoiler, message.message_id, message.caption if message.caption else '', message.media_group_id, message.caption_entities, message)
        if created: await message.answer('Пост успешно добавлен!')
        
class NewPostSoloCommand(MessageHandlerABC):
    filter = NewSoloPostFilter()
    async def _command(self, message: types.Message):
        #FIXME: Починить добавление постов с одной картинкой, выводит ошибку на /info
        await neuroapi.image.add(str(message.from_user.id), message.photo[-1].file_id, message.has_media_spoiler, message.message_id, message.caption, None, message.caption_entities)
        await message.answer('Пост успешно добавлен!')