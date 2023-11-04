from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy.orm import Session

from db.data import Admin, User, engine


class AdminMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass
    
    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        with Session(engine) as session:
            if not session.get(User, event.from_user.id):
                user = User(id=event.from_user.id, user_name=event.from_user.username)
                session.add(user)
                session.commit()
            isAdmin = session.get(Admin, event.from_user.id)
        if not isAdmin:
            await event.answer('Команда только для админов!')
            return None
        return await handler(event, data)
    