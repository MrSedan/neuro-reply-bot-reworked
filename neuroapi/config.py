import os
import tomllib
from typing import List, Self, TypeVar

from attr import dataclass
from dotenv import load_dotenv

from .types._helpers import *


class _Singleton:
    _instances = {}
    
    def __new__(cls) -> Self:
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__new__(cls)
        return cls._instances[cls]
    
@dataclass
class Settings:
    time: List[str]
    
    @staticmethod
    def from_dict(obj: Any) -> 'Settings':
        assert isinstance(obj, dict)
        time = from_list(from_str, obj.get("time", []))
        return Settings(time)
    
    def to_dict(self) -> dict:
        result: dict = {}
        result['time'] = from_list(from_str, self.time)
        return result

class Config(_Singleton):
    api_url: str
    settings: Settings
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        if not os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'settings.toml')): raise Exception('Settings.toml must be in root folder')
        with open(os.path.join(os.path.dirname(__file__), '..', 'settings.toml'), 'rb') as f:
            settings = tomllib.load(f)
            self.settings = Settings.from_dict(settings)
        self.api_url = os.environ.get('API_URL')