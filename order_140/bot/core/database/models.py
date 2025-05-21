from sqlalchemy import BigInteger, Boolean, Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

from .base import Base


class AdminModel(Base):

    __tablename__ = "admins"

    user_id: int = Column(BigInteger, primary_key=True)
    full_name: str = Column(String)
    username: str = Column(String, nullable=True)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"user_id={self.user_id}"
            f"full_name={self.full_name}" 
            f"username={self.username}"
            f")>"
        )


class ChannelModel(Base):
    __tablename__ = "channels"

    channel_id: int = Column(BigInteger, primary_key=True)
    username: str = Column(String)
    full_name: str = Column(String)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"channel_id={self.channel_id}"
            f"username={self.username}"
            f"full_name={self.full_name}"
            f")>"
        )

class PostModel(Base):
    __tablename__ = "posts"
    post_id: int = Column(BigInteger, primary_key=True, autoincrement=True)
    channel_id: int = Column(BigInteger)
    creator_id: int = Column(BigInteger)
    timer_delete: int = Column(Integer)
    content: dict = Column(JSON)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"post_id={self.post_id}"
            f"channel_id={self.channel_id}"
            f"creator_id={self.creator_id}"
            f"timer_delete={self.timer_delete}"
            f"content={self.content}"
            f")>"
        )

Base = declarative_base()

class Topic(Base):
    __tablename__ = "topics"

    chat_id = Column(BigInteger, primary_key=True)
    topic_id = Column(BigInteger, primary_key=True)
