from aiohttp import ClientSession

from .api_method import ApiMethod

from neuroapi.types import Admin as AdminType


class Admin(ApiMethod):

    async def get(self):
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/admin/get')
        return [AdminType.from_dict(admin) for admin in await response.json()]

    async def is_admin(self, id: str):
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/admin/is-admin/{id}')
        if await response.text() == 'false':
            return False
        return True
