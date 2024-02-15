from uuid import UUID

from ._api_model import ApiModel


class Image(ApiModel):
    """
    Represents an image with the following fields:
    
    - message_id: int
    - file_id: str
    - has_spoiler: bool
    - post_uuid: UUID
    """
    message_id: int
    file_id: str
    has_spoiler: bool
    post_uuid: UUID
