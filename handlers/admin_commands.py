import asyncio
from typing import List

import aioschedule as schedule
from aiogram import Bot, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

import neuroapi.types as neuroTypes
from handlers.filters.new_post import (ChangePosts, NewPostFilter,
                                       NewSoloPostFilter)
from handlers.filters.reply_to_user import ReplyToUser
from handlers.handler import Handler
from handlers.middlewares.user import AdminMiddleware
from handlers.states.change_post import ChangePost
from neuroapi import neuroapi
from neuroapi.types import BotSettings as BotSettingsType


def get_post_info(post: neuroTypes.Post, post_id: int) -> str:
    text = post.text
    time = post.timestamp
    from_user = post.from_user_id
    s = f"""Индекс: {post_id}\nТекст: {text}\nВремя отправки: {time}\nОт: [id{from_user}](tg://user?id={from_user})""".replace('#', '\#').replace(
        "_", "\_").replace('.', '\.').replace(',', '\,').replace('!', '\!').replace('-', '\-').replace(':', '\:').replace('+', '\+')
    return s


class AdminCommands(Handler):
    settings: BotSettingsType

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.router.message.middleware(AdminMiddleware())

        @self.router.message(NewPostFilter())
        async def new_post(message: types.Message):
            post: neuroTypes.Post = await neuroapi.post.get_by_media_group_id(message.media_group_id)
            await neuroapi.image.add(str(post.uuid), message.photo[-1].file_id, message.has_media_spoiler, message.message_id)

        @self.router.message(Command('info'))
        async def info_command(message: types.Message):
            posts: List[neuroTypes.Post] = await neuroapi.post.get_will_post()
            admins: List[neuroTypes.Admin] = await neuroapi.admin.get()
            post_c = {}
            for post in posts:
                if post.from_user_id not in post_c:
                    post_c[post.from_user_id] = 1
                else:
                    post_c[post.from_user_id] += 1
            res = "Количество постов от админов:\n"
            res2 = "\nПосты:\n"
            for admin in admins:
                if admin.user_id in post_c:
                    res += f'[{admin.user_name}](tg://user?id={admin.user_id}): {post_c[admin.user_id]}\n'
                else:
                    res += f'[{admin.user_name}](tg://user?id={admin.user_id}): 0\n'
                admin_posts = list(
                    filter(lambda x: x.from_user_id == admin.user_id, posts))
                res2 += f'Посты от {admin.user_name}:\n'
                if len(admin_posts):
                    for i, post in enumerate(admin_posts):
                        #TODO: Если возможно, сделать чтоб было ссылкой на сообщений с /newpost
                        res2 += f'{i+1}. {post.text}\n'
                else:
                    res2 += 'Их нет\)\n'
            await message.answer((res+res2).replace('#', '\#').replace("_", "\_").replace('.', '\.').replace(',', '\,').replace('!', '\!'), parse_mode='markdownv2')

        """
        TODO: Изменение постов сделать нормально, не через редактирование сообщений
        @self.router.message(ChangePosts())
        async def change_post(message: types.Message, state: FSMContext):
            posts = await neuroapi.post.get_will_post()
            if (posts):
                await state.update_data(posts=posts, id=0)
                select_btns = []
                if len(posts) > 1:
                    select_btns.append(types.InlineKeyboardButton(
                        text='->', callback_data='next_post'))
                kb = [
                    select_btns,
                    [types.InlineKeyboardButton(
                        callback_data='change_post_text', text='Текст')],
                    [types.InlineKeyboardButton(
                        text='Отмена', callback_data='cancel')]
                ]
                keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
                post = await neuroapi.post.get(str(posts[0].uuid))
                images = MediaGroupBuilder(
                    caption=get_post_info(post, 1))
                image: neuroTypes.Image
                for image in sorted(post.images, key=lambda x: x.message_id):
                    images.add_photo(image.file_id,
                                     has_spoiler=image.has_spoiler, parse_mode='markdownv2')
                mes = await message.answer_media_group(images.build())
                await state.update_data(edit_msg=mes[0].message_id)
                await message.answer('Действия', reply_markup=keyboard)
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
            posts: List[neuroTypes.Post] = data['posts']
            post_id = data['id']+1
            select_btns = [types.InlineKeyboardButton(
                text='<-', callback_data='prev_post')]
            if post_id < len(posts)-1:
                select_btns.append(types.InlineKeyboardButton(
                    text='->', callback_data='next_post'))
            kb = [
                select_btns,
                [types.InlineKeyboardButton(
                    callback_data='change_post_text', text='Текст')],
                [types.InlineKeyboardButton(
                    text='Отмена', callback_data='cancel')]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await state.update_data(id=post_id)
            post = await neuroapi.post.get(str(posts[post_id].uuid))
            await bot.edit_message_caption(caption=get_post_info(post, post_id+1), chat_id=callback.message.chat.id, message_id=data['edit_msg'], parse_mode='markdownv2')
            await callback.message.edit_reply_markup(reply_markup=keyboard)
            await callback.answer()

        @self.router.callback_query(F.data == 'change_post_text')
        async def change_post_text_call(callback: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            if 'posts' not in data:
                await state.clear()
                await callback.answer()
                await callback.message.delete()
                return
            await callback.message.delete()
            await callback.answer()
            kb = [
                [types.InlineKeyboardButton(
                    text='Отмена', callback_data='cancel')]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await state.set_state(ChangePost.Text)
            await callback.message.answer('Введите новый текст поста:', reply_markup=keyboard)

        @self.router.message(ChangePost.Text)
        async def change_post_text(message: types.Message, state: FSMContext):
            data = await state.get_data()
            if 'posts' not in data:
                await state.clear()
                return
            posts: List[neuroTypes.Post] = data['posts']
            post_id = data['id']
            post_uuid = str(posts[post_id].uuid)
            try:
                await neuroapi.post.edit_text(post_uuid, message.text)
                await message.answer(f'Текст поста изменен на: {message.text}')
            except:
                await message.answer('Ошибка')
            await state.clear()

        @self.router.callback_query(F.data == 'prev_post')
        async def prev_post_changing(callback: types.CallbackQuery, state: FSMContext):
            data = await state.get_data()
            if 'posts' not in data:
                await state.clear()
                await callback.answer()
                await callback.message.delete()
                return
            posts: List[neuroTypes.Post] = data['posts']
            post_id = data['id']-1
            select_btns = [types.InlineKeyboardButton(
                text='->', callback_data='next_post')]
            if post_id > 0:
                select_btns = [types.InlineKeyboardButton(
                    text='<-', callback_data='prev_post'), *select_btns]
            kb = [
                select_btns,
                [types.InlineKeyboardButton(
                    callback_data='change_post_text', text='Текст')],
                [types.InlineKeyboardButton(
                    text='Отмена', callback_data='cancel')]
            ]
            keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
            await state.update_data(id=post_id)
            post = await neuroapi.post.get(str(posts[post_id].uuid))
            await bot.edit_message_caption(caption=get_post_info(post, post_id), chat_id=callback.message.chat.id, message_id=data['edit_msg'], parse_mode='markdownv2')
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
        """

        @self.router.message(Command('post'))
        async def post(message: types.Message | None = None):
            try:
                post = await neuroapi.post.get_post_to_post()
                if (post):
                    images = MediaGroupBuilder(
                        caption=post.text + '\n\nПредложка: @neur0w0men_reply_bot')
                    image: neuroTypes.Image
                    for image in sorted(post.images, key=lambda x: x.message_id):
                        images.add_photo(image.file_id,
                                         has_spoiler=image.has_spoiler)
                    await self.bot.send_media_group(self.settings.channel, images.build())
                    if message:
                        await message.answer('Пост успешно опубликован!')
                elif message:
                    await message.answer('Нет постов')
            except Exception as e:
                if message:
                    await message.answer(f'Ошибка {e}')

        @self.router.message(NewSoloPostFilter())
        async def post_solo(message: types.Message):
            post: neuroTypes.Post = await neuroapi.post.new(message.caption.replace('/newpost ', ''), message.from_user.id)
            await neuroapi.image.add(str(post.uuid), message.photo[-1].file_id, message.has_media_spoiler, message.message_id)
            await message.answer('Пост успешно добавлен!')

        @self.router.message(ReplyToUser())
        async def reply_user(message: types.Message):
            if message.reply_to_message.forward_from is None:
                await message.reply('Пользователь стесняшка и не разрешает отвечать на его сообщения...')
            else:
                try:
                    await bot.send_message(message.reply_to_message.forward_from.id, f'Вам ответил админ:\n{message.text}')
                    await message.reply('Ваше сообщение было отправлено!')
                except Exception as e:
                    print(e)

        @self.router.message(Command('update_settings'))
        async def update_settings(mes: types.Message | None = None):
            self.settings = await neuroapi.bot_settings.get()
            schedule.clear()
            schedule.every().minute.do(update_settings, None)

            # TODO: Сделать в бэке и в боте, чтоб дни тоже можно было в настройках хранить
            for i in self.settings.message_times:
                schedule.every().monday.at(i).do(post, None)
                schedule.every().tuesday.at(i).do(post, None)
                schedule.every().wednesday.at(i).do(post, None)
                schedule.every().thursday.at(i).do(post, None)
                schedule.every().friday.at(i).do(post, None)
                if i not in ['10:00', '20:00']:
                    schedule.every().sunday.at(i).do(post, None)
            if mes:
                await mes.answer('Настройки обновлены!')

        async def settings_and_schedule_checker():
            await update_settings()
            while 1:
                await schedule.run_pending()
                await asyncio.sleep(1)

        asyncio.create_task(settings_and_schedule_checker())
