from aiohttp import ClientSession

from neuroapi.types import Admin as AdminType

from .api_method import ApiMethod


class Admin(ApiMethod):
    """Class for admin methods"""
    async def get(self):
        """
        Asynchronous function to retrieve data from the specified API endpoint and return a list of admins.
        :return List[Admin]
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/admin/get')
        return [AdminType.from_dict(admin) for admin in await response.json()]

    async def is_admin(self, id: str):
        """
        Asynchronous function to check if the user with the given ID is an admin.

        Args:
            id (str): The ID of the user to be checked.

        Returns:
            bool: True if the user is an admin, False otherwise.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+f'/admin/is-admin/{id}')
        if await response.text() == 'false':
            return False
        return True
