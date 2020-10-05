from sqlalchemy import Column, Integer, String

from orm.base import Base, engine, session


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)
    age = Column(Integer)


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session.add(User(name="test", phone="12345", age=1, password="fadfadfad"))
    session.commit()
    print(session.query(User).first().id)
