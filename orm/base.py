from typing import TypeVar

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import SQLITE_URI

engine = create_engine(f'sqlite:///{SQLITE_URI}', convert_unicode=True, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

T = TypeVar("T")


class Base(declarative_base()):
    __abstract__ = True

    def dict(self):
        column_names = self.__table__.columns.keys()
        return {c: getattr(self, c) for c in column_names}

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)  # noqa
        return instance.save()

    def save(self) -> T:
        """Save the record."""
        session.add(self)
        session.commit()
        return self
