from typing import Any, Dict

from pydantic import BaseModel


class ApiModel(BaseModel):
    @classmethod
    def from_dict(cls: 'ApiModel', obj: Dict[str, Any]) -> 'ApiModel':
        """
        Create an instance of ApiModel from a dictionary object.

        Args:
            cls: The class object.
            obj: A dictionary containing attributes for the ApiModel.

        Returns:
            ApiModel: An instance of the ApiModel class.
        """
        return cls(**obj)
    
    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Convert the object to a dictionary
        """
        return self.model_dump(**kwargs)