from ..config import Config


class ApiMethod:
    api_url: str

    def __init__(self) -> None:
        self.api_url = Config().api_url
