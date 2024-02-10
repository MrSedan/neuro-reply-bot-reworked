from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    api_url: str = Field("http://localhost:3000", alias='API_URL')
    token: Optional[str] = Field(None, alias='TOKEN')
    proxy_token: Optional[str] = Field(None, alias='PROXY_TOKEN')