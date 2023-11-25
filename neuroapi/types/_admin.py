from dataclasses import dataclass
from typing import Any
from ._helpers import *


@dataclass
class Admin:
    id: int
    user_id: int

    @staticmethod
    def from_dict(obj: Any) -> 'Admin':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        user_id = int(from_str(obj.get("user_id")))
        return Admin(id, user_id)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["user_id"] = from_str(str(self.user_id))
        return result
