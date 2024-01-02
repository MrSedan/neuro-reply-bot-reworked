from dataclasses import dataclass
from typing import Any
from ._helpers import *


@dataclass
class User:
    id: int
    username: str

    @staticmethod
    def from_dict(obj: Any) -> 'User':
        assert isinstance(obj, dict)
        id = int(from_str(obj.get("id")))
        username = from_str(obj.get("username"))
        return User(id, username)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_str(str(self.id))
        result["username"] = from_str(self.username)
        return result
