from aiogram import types
from aiogram.filters import Filter


class NewPostFilter(Filter):
    """Check if the message is in a media group of photos"""
    async def __call__(self, message: types.Message) -> bool:
        if message.media_group_id is None or message.content_type != 'photo':
            return False
        return True


class NewSoloPostFilter(Filter):
    """Check if the message is /newpost command with photo"""
    async def __call__(self, message: types.Message) -> bool:
        return message.media_group_id is None and message.content_type == 'photo' and message.caption and message.caption.startswith('/newpost ')


class ChangePosts(Filter):
    """Change command filter"""
    async def __call__(self, message: types.Message) -> bool:
        return message.text and message.text.startswith("/change") and message.chat.type == 'private'
