from aiohttp import ClientSession

from .api_method import ApiMethod


class User(ApiMethod):
    """User class for API Methods"""
    async def get(self, id: str, username: str):
        """
        Asynchronous function to retrieve user information by ID and username.

        Args:
            id (str): The user ID.
            username (str): The username.

        Raises:
            Exception: If the API request failing.

        Returns:
            None
        """
        payload = {'id': id, 'username': username}
        async with ClientSession() as session:
            response = await session.post(
                self.api_url+'/user/get', data=payload)
        data = await response.json()
        if 'statusCode' in data:
            raise Exception(data['message'])
