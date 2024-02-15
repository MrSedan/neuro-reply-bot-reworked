from ._methods.admin import Admin
from ._methods.bot_settings import BotSettings
from ._methods.image import Image
from ._methods.post import Post
from ._methods.user import User


class neuroapi:
    """Class with all neuroapi methods"""
    post = Post()
    admin = Admin()
    user = User()
    image = Image()
    bot_settings = BotSettings()
