from aiohttp import ClientSession

from neuroapi.types import BotSettings as BotSettingsType

from .api_method import ApiMethod


class BotSettings(ApiMethod):
    async def get(self)-> BotSettingsType:
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/settings')
            settings = BotSettingsType.from_dict(await response.json())
            return settings
    
    async def get_update(self) -> BotSettingsType:
        async with ClientSession() as session:
            response = await session.get(self.api_url+'/settings/active')
            settings = BotSettingsType.from_dict(await response.json())
            return settings