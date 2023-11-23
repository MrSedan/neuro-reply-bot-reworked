import os
from typing import Self

from dotenv import load_dotenv


class _Singleton:
    _instances = {}
    
    def __new__(cls) -> Self:
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__new__(cls)
        return cls._instances[cls]

class Config(_Singleton):
    api_url: str
    def __init__(self):
        load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
        self.api_url = os.environ.get('API_URL')