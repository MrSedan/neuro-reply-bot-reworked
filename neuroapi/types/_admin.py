from dataclasses import dataclass
from typing import Any

from ._helpers import *


@dataclass
class Admin:
    user_id: int
    user_name: str

    @staticmethod
    def from_dict(obj: Any) -> 'Admin':
        assert isinstance(obj, dict)
        user_id = int(from_str(obj.get("user_id")))
        user_name = from_str(obj.get("user_name"))
        return Admin(user_id, user_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["user_id"] = from_str(str(self.user_id))
        result["user_name"] = from_str(self.user_name)
        return result
