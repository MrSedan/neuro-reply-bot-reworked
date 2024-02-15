from pydantic import BaseModel, Field

from ..config import GlobalConfig as Config


class ApiMethod(BaseModel):
    """Base class for API methods"""
    api_url: str = Field(Config().api_url)
