from datetime import datetime
from typing import Any
from uuid import uuid4

from aiogram import Bot, F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder
from sqlalchemy.orm import Session

from db.data import Admin, Image, Post, User, engine
from handlers.filters.new_post import (ChangePosts, NewPostFilter,
                                       NewSoloPostFilter)
from handlers.middlewares.user import AdminMiddleware


def get_post_info(post: Post) -> str:
    text = post.text
    time = post.timestamp
    from_user = post.from_user_id
    s = f"""Текст: {text}\nВремя отправки: {time}\nОт: [id{from_user}](tg://user?id={from_user})""".replace('#', '\#').replace("_", "\_").replace('.', '\.').replace(',', '\,').replace('!', '\!').replace('-', '\-').replace(':', '\:')
    return s


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
                    photo = Image(message_id=message.message_id,
                                  post=post, file_id=message.photo[-1].file_id)
                    session.add(photo)
                    session.commit()
                else:
                    print('No posts anymore ;-(')

        @self.router.message(Command('info'))
        async def info_command(message: types.Message):
            with Session(engine) as session:
                posts = session.query(Post).filter(not Post.posted).all()
                admins = session.query(Admin).all()
                post_c = {}
                for admin in admins:
                    post_c[str(admin.user_id)] = 0
                for post in posts:
                    post_c[str(post.from_user_id)] += 1
            await message.answer(str(post_c))

        @self.router.message(ChangePosts())
        async def change_post(message: types.Message, state: FSMContext):
            with Session(engine) as session:
                posts = session.query(Post).filter(
                    Post.posted == False).order_by(Post.timestamp.asc()).all()
                if len(posts):
                    await state.update_data(posts=posts, id=0)
                    select_btns = []
                    if len(posts) > 1:
                        select_btns.append(types.InlineKeyboardButton(
                            text='->', callback_data='next_post'))
                    kb = [
                        select_btns,
                        [types.InlineKeyboardButton(
                            text='Отмена', callback_data='cancel')]
                    ]
                    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
                    images = MediaGroupBuilder(caption=get_post_info(posts[0]))
                    for image in posts[0].images:
                        images.add_photo(image.file_id, parse_mode='markdownv2')
                    mes = await message.answer_media_group(media=images.build())
                    await state.update_data(edit_msg=mes[0].message_id)
                    await message.answer('Действия', reply_markup=keyboard)
                    # await message.answer(get_post_info(posts[0]), reply_markup=keyboard, parse_mode='markdownv2')
                else:
                    await message.answer('Нет постов')

        @self.router.callback_query(F.data == 'next_post')
        async def next_post_changing(callback: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            if 'posts' not in data:
                await state.clear()
                await callback.answer()
                await callback.message.delete()
                return
            posts = data['posts']
            post_id = data['id']+1
            select_btns = [types.InlineKeyboardButton(
                text='<-', callback_data='prev_post')]
            if post_id < len(posts)-1:
                select_btns.append(types.InlineKeyboardButton(
                    text='->', callback_data='next_post'))
            kb = [
                select_btns,
                [types.InlineKeyboardButton(
                    text='Отмена', callback_data='cancel')]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await state.update_data(id=post_id)
            await bot.edit_message_caption(caption=get_post_info(posts[post_id]), chat_id=callback.message.chat.id, message_id=data['edit_msg'], parse_mode='markdownv2')
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer()

        @self.router.callback_query(F.data == 'prev_post')
        async def prev_post_changing(callback: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            if 'posts' not in data:
                await state.clear()
                await callback.answer()
                await callback.message.delete()
                return
            posts = data['posts']
            post_id = data['id']-1
            select_btns = [types.InlineKeyboardButton(
                text='->', callback_data='next_post')]
            if post_id > 0:
                select_btns = [types.InlineKeyboardButton(
                    text='<-', callback_data='prev_post'), *select_btns]
            kb = [
                select_btns,
                [types.InlineKeyboardButton(
                    text='Отмена', callback_data='cancel')]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await state.update_data(id=post_id)
            await bot.edit_message_caption(caption=get_post_info(posts[post_id]), chat_id=callback.message.chat.id, message_id=data['edit_msg'], parse_mode='markdownv2')
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer()

        @self.router.callback_query(F.data.casefold() == 'cancel')
        async def cancel_changing(callback: types.CallbackQuery, state: FSMContext):
            await state.clear()
            await callback.answer()
            await callback.message.delete()
            data = await state.get_data()
            if 'edit_msg' in data:
                await bot.delete_message(message_id=data['edit_msg'], chat_id=callback.message.chat.id)

        @self.router.message(Command('post'))
        async def post(message: types.Message):
            with Session(engine) as session:
                post = session.query(Post).filter(
                    Post.posted == False).order_by(Post.timestamp.asc()).first()
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
                post = Post(uuid=uuid4(), text=message.caption.replace(
                    '/newpost ', ''), media_group_id='')
                post_user = session.get(Admin, message.from_user.id)
                post.user = post_user
                photo = Image(message_id=message.message_id,
                              post=post, file_id=message.photo[-1].file_id)
                session.add(photo)
                session.add(post)
                session.commit()
                await message.answer('Пост успешно добавлен!')

    def __call__(self, *args: Any, **kwds: Any) -> Router:
        return self.router


def setup(bot: Bot) -> Router:
    return Admin_commands(bot)()
