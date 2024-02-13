from typing import List

from aiogram import types

from handlers.filters.new_post import NewPostFilter, NewSoloPostFilter
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class NewPostCommand(MessageHandlerABC):
    filter = NewPostFilter()
    async def _command(self, message: types.Message, album: List[types.Message]):
        sorted_album = sorted(album, key=lambda x: x.message_id)
        if (not sorted_album[0].caption.startswith('/newpost ') if sorted_album[0].caption else True):
            return 
        for mes in sorted_album:
            await neuroapi.image.add(str(message.from_user.id), mes.photo[-1].file_id, mes.has_media_spoiler, mes.message_id, mes.caption if mes.caption else '', mes.media_group_id, mes.caption_entities, mes)
        await message.answer(f'Пост успешно добавлен!')


class NewPostSoloCommand(MessageHandlerABC):
    filter = NewSoloPostFilter()
    async def _command(self, message: types.Message):
        await neuroapi.image.add(str(message.from_user.id), message.photo[-1].file_id, message.has_media_spoiler, message.message_id, message.caption, None, message.caption_entities, message)
        await message.answer('Пост успешно добавлен!')