from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import Session

from db.data import User, engine

ADMIN_LIST = [248770879, 395543883]

class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        with Session(engine) as session:
                if not session.get(User, event.from_user.id):
                    user = User(id=event.from_user.id, user_name=event.from_user.username)
                    session.add(user)
                    session.commit()
        if event.from_user.id not in ADMIN_LIST:
            await event.answer('Команда только для админов!')
            return None
        return await handler(event, data)
    