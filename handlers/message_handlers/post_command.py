from aiogram import types
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder

import neuroapi.types as neuroTypes
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class PostCommand(MessageHandlerABC):
    """Command to post posts manually or by timer"""
    filter = Command('post')
    async def _command(self, message: types.Message | None = None):
        settings = neuroTypes.BotSettings.get_instance()
        try:
            post = await neuroapi.post.get_post_to_post()
            if (post):
                images = MediaGroupBuilder(
                    caption=post.text + '\n\nПредложка: @neur0w0men_reply_bot', caption_entities=post.message_entities)
                image: neuroTypes.Image
                for image in sorted(post.images, key=lambda x: x.message_id):
                    images.add_photo(image.file_id,
                                        has_spoiler=image.has_spoiler)
                await self.bot.send_media_group(settings.channel, images.build())
                if message:
                    await message.answer('Пост успешно опубликован!')
            elif message:
                await message.answer('Нет постов')
        except Exception as e:
            if message:
                await message.answer(f'Ошибка {e}')