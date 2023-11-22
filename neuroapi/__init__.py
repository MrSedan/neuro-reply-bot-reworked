from .post import Post
from .admin import Admin
from .user import User
from .image import Image
from dotenv import load_dotenv
import os
from os.path import join, dirname


load_dotenv(join(dirname(__file__), "..", '.env'))


class neuroapi:
    post = Post(os.environ.get('API_URL'))
    admin = Admin(os.environ.get('API_URL'))
    user = User(os.environ.get('API_URL'))
    image = Image(os.environ.get('API_URL'))
