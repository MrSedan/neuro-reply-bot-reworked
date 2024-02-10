import json
from typing import Optional

from pydantic import Field

from ._api_model import ApiModel


class User(ApiModel):
    id: int
    username: str = Field(..., alias='user_name')
    banned: Optional[bool] = Field(None)

    def to_dict(self) -> dict:
        obj = super().to_dict(exclude_unset=True)
        obj['id'] = str(obj['id'])
        return obj