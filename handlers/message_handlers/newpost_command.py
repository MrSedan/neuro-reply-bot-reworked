from aiogram import types

import neuroapi.types as neuroTypes
from handlers.filters.new_post import NewPostFilter, NewSoloPostFilter
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class NewPostCommand(MessageHandlerABC):
    filter = NewPostFilter()
    async def _command(self, message: types.Message):
        post: neuroTypes.Post = await neuroapi.post.get_by_media_group_id(message.media_group_id)
        await neuroapi.image.add(str(post.uuid), message.photo[-1].file_id, message.has_media_spoiler, message.message_id)
        
class NewPostSoloCommand(MessageHandlerABC):
    filter = NewSoloPostFilter()
    async def _command(self, message: types.Message):
        post: neuroTypes.Post = await neuroapi.post.new(message.caption.replace('/newpost ', ''), message.from_user.id, message_entities=message.caption_entities)
        await neuroapi.image.add(str(post.uuid), message.photo[-1].file_id, message.has_media_spoiler, message.message_id)
        await message.answer('Пост успешно добавлен!')