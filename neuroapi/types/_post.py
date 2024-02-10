import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from aiogram.types import MessageEntity
from pydantic import Field

from ._api_model import ApiModel
from ._image import Image


class Post(ApiModel):
    uuid: UUID
    posted: bool
    text: str
    media_group_id: int | str
    timestamp: datetime
    from_user_id: int
    images: Optional[List[Image]] = Field(None)
    message_entities: Optional[List[MessageEntity]] = Field(None)
        

    @classmethod
    def from_dict(cls: 'Post', obj: Dict[str, Any]) -> 'Post':
        mes_ent = json.loads(obj.get('message_entities', '[]'))
        obj['message_entities'] = mes_ent
        return cls(**obj)

    def to_dict(self) -> dict:
        obj = super().to_dict()
        obj['message_entities'] = json.dumps(obj['message_entities'])
        obj['media_group_id'] = str(obj['media_group_id']) 
        return obj