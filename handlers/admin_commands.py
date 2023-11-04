from typing import Any
from uuid import uuid4

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.orm import Session

from db.data import Admin, Image, Post, User, engine
from handlers.filters.new_post import NewPostFilter, NewSoloPostFilter
from handlers.middlewares.user import AdminMiddleware


class Admin_commands:
    bot: Bot
    router: Router
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.router = Router()
        self.router.message.middleware(AdminMiddleware())
        
        @self.router.message(Command('test'))
        async def test_command(message: types.Message):
            with Session(engine) as session:
                user = session.get(User, message.from_user.id)
                await message.answer(str(user))
        
        @self.router.message(NewPostFilter())
        async def new_post(message: types.Message):
            with Session(engine) as session:
                post = session.query(Post).filter(
                    Post.media_group_id == message.media_group_id).first()
                if post:
                    photo = Image(message_id=message.message_id, post=post, file_id=message.photo[-1].file_id)
                    session.add(photo)
                    session.commit()
                else:
                    print('No posts anymore ;-(')
        
        @self.router.message(Command('info'))
        async def info_command(message: types.Message):
            await message.answer('Тест')
    
        @self.router.message(Command('post'))
        async def post(message: types.Message):
            with Session(engine) as session:
                post = session.query(Post).filter(Post.posted == False).order_by(Post.timestamp.asc()).first()
                if post:
                    images = MediaGroupBuilder(caption=post.text)
                    for image in post.images:
                        images.add_photo(image.file_id)
                    await message.answer_media_group(images.build())
                    post.posted = True
                    session.commit()
                else:
                    await message.answer('Постов немаэ')
        
        @self.router.message(NewSoloPostFilter())
        async def post_solo(message: types.Message):
            with Session(engine) as session:
                post = Post(uuid=uuid4(), text=message.caption.replace('/newpost ', ''), media_group_id='')
                post_user = session.get(Admin, message.from_user.id)
                post.user = post_user
                photo = Image(message_id=message.message_id, post=post, file_id=message.photo[-1].file_id)
                session.add(photo)
                session.add(post)
                session.commit()
                await message.answer('Пост успешно добавлен!')
                
    
    def __call__(self, *args: Any, **kwds: Any) -> Router:
        return self.router
    
    
def setup(bot: Bot) -> Router:
    return Admin_commands(bot)()