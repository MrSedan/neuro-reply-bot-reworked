import json

from aiohttp import ClientSession

from .api_method import ApiMethod


class Image(ApiMethod):
    async def add(self, post_id: str, file_id: str, has_spoiler: bool | None, message_id: int):
        payload = {'post_id': post_id, 'file_id': file_id,
                   'has_spoiler': has_spoiler, 'message_id': message_id}
        if has_spoiler is None:
            payload.pop('has_spoiler')
        payload = json.dumps(payload)
        async with ClientSession() as session:
            response = await session.post(
                self.api_url+'/image/add', data=payload, headers={'Content-Type': 'application/json'})
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
