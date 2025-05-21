from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    def __repr__(self) -> str:
        body = ""
        return f"{self.__class__.__name__}[\n{body}\n"
