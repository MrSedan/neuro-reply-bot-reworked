from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Any
from neuroapi.types._helpers import *


@dataclass
class User:
    uuid: UUID
    user_name: str
    description: str
    link: str
    connect_date: datetime
    user_id: str

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        uuid = UUID(obj.get("uuid"))
        user_name = from_str(obj.get("userName"))
        description = from_str(obj.get("description"))
        link = from_str(obj.get("link"))
        connect_date = from_datetime(obj.get("connectDate"))
        user_id = from_none(obj.get("user_id"))
        return User(uuid, user_name, description, link, connect_date, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = str(self.uuid)
        result["userName"] = from_str(self.user_name)
        result["description"] = from_str(self.description)
        result["link"] = from_str(self.link)
        result["connectDate"] = self.connect_date.isoformat()
        result["user_id"] = from_none(self.user_id)
        return result
