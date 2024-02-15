from typing import List
from uuid import UUID

from pydantic import Field

from ._api_model import ApiModel
from ._singleton import Singleton


class BotSettings(ApiModel, Singleton):
    """
    Bot settings model with UUID, message times, channel, and activity status.
    """
    uuid: UUID
    message_times: List[str] = Field([], alias='messageTimes')
    channel: str
    is_active: bool = Field(False, alias='isActive')
    
    def get_text(self):
        """
        Method to get the text containing channel and message times.

        :return: string - the text containing channel and message times
        """
        return f"Канал: {self.channel}\nВремя: {', '.join(self.message_times)}"