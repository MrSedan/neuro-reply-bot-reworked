from typing import Any, Dict

from pydantic import BaseModel


class ApiModel(BaseModel):
    @classmethod
    def from_dict(cls: 'ApiModel', obj: Dict[str, Any]) -> 'ApiModel':
        return cls(**obj)
    
    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        return self.model_dump(**kwargs)