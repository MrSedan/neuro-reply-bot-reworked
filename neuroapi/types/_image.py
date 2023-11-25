from dataclasses import dataclass
from uuid import UUID
from ._helpers import *


@dataclass
class Image:
    message_id: int
    file_id: str
    has_spoiler: bool
    post_uuid: UUID

    @staticmethod
    def from_dict(obj: Any) -> 'Image':
        assert isinstance(obj, dict)
        message_id = from_int(obj.get("message_id"))
        file_id = from_str(obj.get("file_id"))
        has_spoiler = from_bool(obj.get("has_spoiler"))
        post_uuid = UUID(obj.get("post_uuid"))
        return Image(message_id, file_id, has_spoiler, post_uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["message_id"] = from_int(self.message_id)
        result["file_id"] = from_str(self.file_id)
        result["has_spoiler"] = from_bool(self.has_spoiler)
        result["post_uuid"] = str(self.post_uuid)
        return result
