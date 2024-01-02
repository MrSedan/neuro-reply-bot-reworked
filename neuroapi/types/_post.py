from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from typing import Any, List, Optional
from ._image import Image
from ._helpers import *


@dataclass
class Post:
    uuid: UUID
    posted: bool
    text: str
    media_group_id: int | str
    timestamp: datetime
    from_user_id: int
    images: Optional[List[Image]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Post':
        assert isinstance(obj, dict)
        uuid = UUID(obj.get("uuid"))
        posted = from_bool(obj.get("posted"))
        text = from_str(obj.get("text"))
        media_group_id = from_str(obj.get("media_group_id")) if obj.get(
            "media_group_id") is not None else 'None'
        timestamp = from_datetime(obj.get("timestamp"))
        from_user_id = int(from_str(obj.get("from_user_id")))
        images = from_union([lambda x: from_list(
            Image.from_dict, x), from_none], obj.get("images"))
        return Post(uuid, posted, text, media_group_id, timestamp, from_user_id, images)

    def to_dict(self) -> dict:
        result: dict = {}
        result["uuid"] = str(self.uuid)
        result["posted"] = from_bool(self.posted)
        result["text"] = from_str(self.text)
        result["media_group_id"] = from_str(str(self.media_group_id))
        result["timestamp"] = self.timestamp.isoformat()
        result["from_user_id"] = from_str(str(self.from_user_id))
        if self.images is not None:
            result["images"] = from_union([lambda x: from_list(
                lambda x: to_class(Image, x), x), from_none], self.images)
        return result
