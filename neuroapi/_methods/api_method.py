from pydantic import BaseModel, Field

from ..config import GlobalConfig as Config


class ApiMethod(BaseModel):
    api_url: str = Field(Config().api_url)
