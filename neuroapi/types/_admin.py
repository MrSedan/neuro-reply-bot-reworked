from ._api_model import ApiModel


class Admin(ApiModel):        
    """Represents an admin with fields user_id of type int and user_name of type str"""
    user_id: int
    user_name: str
