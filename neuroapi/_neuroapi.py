from ._methods.admin import Admin
from ._methods.image import Image
from ._methods.post import Post
from ._methods.user import User


class neuroapi:
    post = Post()
    admin = Admin()
    user = User()
    image = Image()
