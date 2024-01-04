import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional
from uuid import UUID

from aiogram.types import MessageEntity

from ._helpers import *
from ._image import Image


def to_message_dict_class(x: Any) -> dict:
    assert isinstance(x, MessageEntity)
    return cast(MessageEntity, x).model_dump()


@dataclass
class Post:
    uuid: UUID
    posted: bool
    text: str
    media_group_id: int | str
    timestamp: datetime
    from_user_id: int
    images: Optional[List[Image]] = None
    message_entities: Optional[List[MessageEntity]] = None

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
        mes_ent = json.loads(obj.get('message_entities','[]'))
        message_entities = from_list(MessageEntity.model_validate, mes_ent)
        return Post(uuid, posted, text, media_group_id, timestamp, from_user_id, images, message_entities)

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
        if self.message_entities is not None:
            result['message_entities'] = from_union([lambda x: from_list(
                lambda x: to_message_dict_class(x), x), from_none], self.message_entities)
        return result
