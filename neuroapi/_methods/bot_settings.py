from aiohttp import ClientSession

from neuroapi.types import BotSettings as BotSettingsType

from .api_method import ApiMethod


class BotSettings(ApiMethod):
    """Class for bot settings API methods"""
    async def get(self)-> BotSettingsType:
        """
        Asynchronous function that retrieves bot settings from the API.
        
        Returns:
            BotSettings: The bot settings retrieved from the API.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/settings')
            settings = BotSettingsType.from_dict(await response.json())
            return settings
    
    async def get_update(self) -> BotSettingsType:
        """
        Asynchronously gets and returns the bot settings from the specified API URL. Clearing server cache.

        Parameters:
            self: The instance of the class.
        
        Returns:
            BotSettings: The bot settings obtained from the API.
        """
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/settings/active')
            settings = BotSettingsType.from_dict(await response.json())
            return settings