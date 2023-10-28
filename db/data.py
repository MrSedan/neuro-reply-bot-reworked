import os
from os.path import dirname, join
from typing import List, Optional
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

load_dotenv(join(dirname(__file__), '..', '.env'))
DATABASE_PASSWORD=os.getenv('DATABASE_PASSWORD')
DATABASE_NAME=os.getenv('DATABASE_NAME')
DATABASE_USER=os.getenv('DATABASE_USER')
DATABASE_PORT=os.getenv('DATABASE_PORT')
DATABASE_HOST=os.getenv('DATABASE_HOST')
engine = create_engine(f"postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}", echo=True)


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[Optional[str]]
    
    admin: Mapped['Admin'] = relationship(back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f'User(id={self.id!r}, user_name={self.user_name!r})'

    def __str__(self) -> str:
        return f'User(id={self.id!r}, user_name={self.user_name!r})'
    
class Admin(Base):
    __tablename__ = 'admin'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), primary_key=True)
    user: Mapped['User'] = relationship(back_populates='admin')
    posts: Mapped[List['Post']] = relationship(back_populates='user', cascade='all, delete')

class Post(Base):
    __tablename__ = 'post'
    
    uuid: Mapped[UUID] = mapped_column(primary_key=True)
    from_user_id: Mapped[int] = mapped_column(ForeignKey('admin.user_id'))
    user: Mapped['Admin'] = relationship(back_populates='posts')
    text: Mapped[str]
    images: Mapped[str]
    
if __name__ == '__main__':
    Base.metadata.create_all(engine)