import json
from typing import List, Optional

import requests
from aiogram.types import MessageEntity
from aiohttp import ClientSession

import neuroapi.types as neuroTypes

from .api_method import ApiMethod
from .enums import EGetAll


class Post(ApiMethod):
    """Class for Post API methods"""
    async def new(self, text: str, from_user_id: str, media_group_id: str = "None", message_entities: Optional[List[MessageEntity]] = None):
        """
        Asynchronously creates a new post with the given text, from_user_id, media_group_id, and message_entities.

        Args:
            text (str): The text of the post.
            from_user_id (str): The ID of the user creating the post.
            media_group_id (str, optional): The media group ID. Defaults to "None".
            message_entities (List[MessageEntity], optional): List of message entities. Defaults to None.

        Returns:
            Post: A new post created from the given data.
        """
        payload = {'text': text, 'from_user_id': from_user_id}
        if media_group_id != 'None':
            payload['media_group_id'] = media_group_id
        if message_entities is not None:
            mes_ent = list(map(lambda x: x.model_dump(), message_entities))
            arr =[]
            for item in mes_ent:
                if item['type'] == 'bot_command': continue
                item['offset'] -= 9
                arr.append(item)
            payload['message_entities'] = json.dumps(arr)
        response = requests.post(self.api_url+'/post/new', data=payload)
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def __get_all(self, status: EGetAll):
        """
        An asynchronous function to retrieve all items based on the given status using the provided API URL. 
        It takes a status parameter of type EGetAll. 
        The function returns the response obtained from the API call.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-all/{status.value}')
        return response

    async def get_all(self):
        """
        Asynchronously retrieves all items and returns a list of Post objects.
        """
        result = await self.__get_all(EGetAll.all)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get_will_post(self):
        """
        Asynchronously retrieves and returns the will_post data from the API.
        """
        result = await self.__get_all(EGetAll.will_post)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get_posted(self):
        """
        Asynchronously gets all the posted items and returns a list of Post objects.
        """
        result = await self.__get_all(EGetAll.posted)
        return [neuroTypes.Post.from_dict(post) for post in await result.json()]

    async def get(self, post_id: str):
        """
        An asynchronous function to retrieve a post by its ID from the API.

        Args:
            post_id (str): The ID of the post to retrieve.

        Returns:
            Post: The retrieved post object.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get/{post_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)
    
    async def get_by_order(self, post_order: str):
        """
        Asynchronously gets a post by order from the API.

        Args:
            post_order (str): The order of the post to retrieve.

        Returns:
            Post: The post retrieved from the API.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-post-by-order/{post_order}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def get_by_media_group_id(self, media_group_id: str):
        """
        Asynchronous function to retrieve data by media group ID.

        Args:
            media_group_id (str): The media group ID for retrieval.

        Returns:
            neuroTypes.Post: The retrieved post data.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-by-media-group-id/{media_group_id}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def edit_text(self, post_id: str, text: str):
        """
        Asynchronously edits the text of a post.

        Args:
            post_id (str): The ID of the post to edit.
            text (str): The new text for the post.

        Returns:
            Post: The edited post object.
        """
        response = requests.post(
            self.api_url+f"/post/edit/{post_id}", data={"text": text})
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)

    async def edit_text_by_order_num(self, order: str, text: str, message_entities: Optional[List[MessageEntity]] = None):
        """
        Asynchronously edits text by order number.

        Args:
            order (str): The order number.
            text (str): The new text.
            message_entities (Optional[List[MessageEntity]], optional): A list of message entities. Defaults to None.

        Returns:
            Post: The edited post.
        
        Raises:
            Exception: If the response contains an error status code.
        """
        payload = {"text": text}
        if message_entities is not None:
            if message_entities is not None:
                mes_ent = list(map(lambda x: x.model_dump(), message_entities))
                arr =[]
                for item in mes_ent:
                    if item['type'] == 'bot_command': continue
                    item['offset'] -= 7+len(order)
                    arr.append(item)
                payload['message_entities'] = json.dumps(arr)
        response = requests.post(self.api_url + f"/post/edit-post-by-order-num/{order}", data=payload)
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)
    
    async def get_post_to_post(self):
        """
        Retrieves a post from the API and returns it as a `neuroTypes.Post` object.

        Returns:
            neuroTypes.Post: The retrieved post.

        Raises:
            Exception: If the API returns a non-200 status code or if there is an error message in the response.

        Returns:
            None: If the API returns a 404 status code.
        """
        response = requests.get(self.api_url+f"/post/post")
        data = response.json()
        if 'statusCode' in data:
            if response.status_code==404:
                return None
            else:
                raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)
    
    async def delete_by_order(self, order: str):
        """
        Asynchronously deletes a post by order.

        Args:
            order (str): The order of the post to be deleted.

        Returns:
            None
        """
        response = requests.delete(self.api_url+f"/post/delete-post-by-order/{order}")
        data = response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
    async def get_deleted_posts(self) -> List[neuroTypes.Post]:
        """
        Asynchronously retrieves a list of deleted posts from the API.

        Parameters:
            self: The instance of the class.
        
        Returns:
            List[Post]: A list of Post objects representing the deleted posts.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/post/get-deleted')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return [neuroTypes.Post.from_dict(post) for post in data]
    
    async def restore_post(self, order: str):
        """
        Asynchronously restores a post using the given order string.

        Args:
            order (str): The order string used to identify the post to be restored.

        Returns:
            Post: A Post object representing the restored post.
        """
        async with ClientSession() as session:
            response = await session.put(self.api_url+f'/post/restore-post-by-order/{order}')
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
        return neuroTypes.Post.from_dict(data)
