from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import SQLITE_URI


class Base(declarative_base()):
    __abstract__ = True

    def dict(self):
        column_names = self.__table__.columns.keys()
        return {c: getattr(self, c) for c in column_names}


engine = create_engine(f'sqlite:///{SQLITE_URI}', convert_unicode=True, echo=False)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
