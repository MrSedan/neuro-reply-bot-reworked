from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder

import neuroapi.types as neuroTypes
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class PreviewCommand(MessageHandlerABC):
    """Command to preview posts like it posted to channel"""
    filter = Command('preview')
    async def _command(self, message: Message):
        text = message.text.split()
        if len(text)!=2:
            await message.answer('Неверное количество аргументов')
            return
        try:
            post = await neuroapi.post.get_by_order(text[1])
        except Exception as e:
            await message.answer(f'Ошибка {e}')
            return
        if (post):
            images = MediaGroupBuilder(
                caption=post.text + '\n\nПредложка: @neur0w0men_reply_bot', caption_entities=post.message_entities)
            image: neuroTypes.Image
            for image in sorted(post.images, key=lambda x: x.message_id):
                images.add_photo(image.file_id,
                                    has_spoiler=image.has_spoiler)
            await self.bot.send_media_group(message.chat.id, images.build())
        elif message:
            await message.answer('Нет постов')