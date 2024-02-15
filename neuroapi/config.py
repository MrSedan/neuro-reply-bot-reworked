import logging
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class GlobalConfig(BaseSettings):
    """Config class"""
    api_url: str = Field("http://localhost:3000", alias='API_URL')
    
    # Redis config
    redis_host: str = Field("localhost", alias="REDIS_HOST")
    redis_port: int = Field(6379, alias="REDIS_PORT")
    redis_password: str = Field('', alias="REDIS_PASSWORD")
    redis_db: int = Field(0, alias='REDIS_DB')
    
    # Bot tokens
    token: Optional[str] = Field(None, alias='TOKEN')
    proxy_token: Optional[str] = Field(None, alias='PROXY_TOKEN')
    
    logging_lvl_text: str = Field('WARNING', alias='LOGGING_LVL')
    
    @property
    def logging_lvl(self):
        lvl = self.logging_lvl_text.upper()
        if lvl == 'INFO':
            return logging.INFO
        elif lvl == 'DEBUG':
            return logging.DEBUG
        elif lvl in ['WARNING', 'WARN']:
            return logging.WARNING
        elif lvl == 'ERROR':
            return logging.ERROR
        elif lvl == 'CRITICAL':
            return logging.CRITICAL
        else:
            return logging.WARNING        
        
    
    @property
    def redis_url(self):
        """Getter method to construct and return the redis URL using the provided redis password, host, port, and database number"""
        return f'redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}'
    
    class Config:
        """Config file for pydantic settings"""
        env_file = '.env'
        