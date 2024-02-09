from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ._helpers import *
from ._singleton import Singleton


@dataclass
class BotSettings(Singleton):
    uuid: UUID
    message_times: List[str]
    channel: str
    is_active: bool

    @staticmethod
    def from_dict(obj: Any) -> 'BotSettings':
        assert isinstance(obj, dict)
        uuid = UUID(obj.get("uuid"))
        message_times = from_list(from_str, obj.get("messageTimes"))
        channel = from_str(obj.get("channel"))
        is_active = from_bool(obj.get("isActive"))
        return BotSettings(uuid, message_times, channel, is_active)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = str(self.uuid)
        result["messageTimes"] = from_list(from_str, self.message_times)
        result["channel"] = from_str(self.channel)
        result["isActive"] = from_bool(self.is_active)
        return result

    @staticmethod
    def get_active() -> Optional['BotSettings']:
        try:
            return BotSettings._instances[BotSettings]
        except:
            return None