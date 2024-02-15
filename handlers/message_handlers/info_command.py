from typing import List

from aiogram import types
from aiogram.filters import Command

import neuroapi.types as neuroTypes
from neuroapi import neuroapi

from .handler import MessageHandlerABC


class InfoCommand(MessageHandlerABC):
    """Command to show info about posts"""
    filter = Command('info')
    
    async def _command(self, message: types.Message):        
        posts: List[neuroTypes.Post] = await neuroapi.post.get_will_post()
        admins: List[neuroTypes.Admin] = await neuroapi.admin.get()
        post_c = {}
        k = 1
        for post in posts:
            if post.from_user_id not in post_c:
                post_c[post.from_user_id] = 1
            else:
                post_c[post.from_user_id] += 1
        res = "Количество постов от админов:\n"
        res2 = "\nПосты:\n"
        posts_entities: List[types.MessageEntity] = []
        for admin in admins:
            if admin.user_id in post_c:
                res += f'[{admin.user_name}](tg://user?id={admin.user_id}): {post_c[admin.user_id]}\n'
            else:
                res += f'[{admin.user_name}](tg://user?id={admin.user_id}): 0\n'
            admin_posts = list(
                filter(lambda x: x.from_user_id == admin.user_id, posts))
            res2 += f'\nПосты от {admin.user_name}:\n'
            if len(admin_posts):
                for i, post in enumerate(admin_posts):
                    # TODO: Если возможно, сделать чтоб было ссылкой на сообщений с /newpost
                    s = f'{i+1}.({posts.index(post)+1}) {post.text}\n'
                    k+=1
                    res2 += s
                    for entity in post.message_entities:
                        entity.offset += 6+res2.index(s)
                        posts_entities.append(entity)
            else:
                res2 += 'Их нет)\n'
        await message.answer(res.replace('#', '\#').replace(
    "_", "\_").replace('.', '\.').replace(',', '\,').replace('!', '\!').replace('-', '\-').replace(':', '\:').replace('+', '\+'), parse_mode='markdownv2')
        await message.answer(res2, entities=posts_entities)