from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    api_url: str = Field("http://localhost:3000", alias='API_URL')
    
    # Redis config
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_password: str = Field('', alias="REDIS_PASSWORD")
    redis_db: int = Field(0, alias='REDIS_DB')
    
    # Bot tokens
    token: Optional[str] = Field(None, alias='TOKEN')
    proxy_token: Optional[str] = Field(None, alias='PROXY_TOKEN')
    
    @property
    def redis_url(self):
        return f'redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}'
    
    class Config:
        env_file = '.env'