from typing import Self


class Singleton:
    _instances = {}
    
    def __new__(cls, *args, **kwargs) -> Self:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
        return cls._instances[cls]