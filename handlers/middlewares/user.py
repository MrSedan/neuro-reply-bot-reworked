from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

ADMIN_LIST = [248770879, 395543883]

class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        if event.from_user.id in ADMIN_LIST:
            await event.answer('Команда только для админов!')
            return None
        return await handler(event, data)
    