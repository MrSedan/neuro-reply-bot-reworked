from typing import Self


class Singleton:
    """
    Returns the instance of the Singleton class.

    :return: Self - The instance of the Singleton class.
    """
    _instances = {}
    
    def __new__(cls, *args, **kwargs) -> Self:
        """
        Create a new instance of the class if it doesn't exist, and return the existing instance if it does.
        
        Parameters:
            cls: The class.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        
        Returns:
            Self: The instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls)
        return cls._instances[cls]
    
    @classmethod
    def get_instance(cls: Self):
        """
        Return the instance belonging to the class.
        """
        return cls._instances[cls]