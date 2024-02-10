from uuid import UUID

from ._api_model import ApiModel


class Image(ApiModel):
    message_id: int
    file_id: str
    has_spoiler: bool
    post_uuid: UUID
