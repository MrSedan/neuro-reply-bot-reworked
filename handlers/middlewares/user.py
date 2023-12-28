from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from neuroapi import neuroapi


class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        if event.chat.type not in ['private', 'group']:
            return None
        await neuroapi.user.get(str(event.from_user.id), event.from_user.username)
        isAdmin = await neuroapi.admin.is_admin(str(event.from_user.id))
        if not isAdmin:
            await event.answer('Команда только для админов!')
            return None
        return await handler(event, data)
    