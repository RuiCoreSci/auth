from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey

from orm import Permission
from orm.base import Base


class User(Base):
    __tablename__ = 'user'

    name: str = Column(String, nullable=False, comment="姓名")
    password: str = Column(String, nullable=False, comment="密码")
    phone: str = Column(String, comment="联系电话")
    age: int = Column(Integer, comment="年龄")
    role_id: int = Column(ForeignKey("role.id"), nullable=False, comment="角色")

    @classmethod
    def get_permission(cls, user_id):
        perms: List[Permission] = cls.session.query(Permission).join(User, User.role_id == Permission.role_id).filter(
            User.id == user_id).all()
        return {f"{p.operation_id}-{p.resource_id}" for p in perms}


if __name__ == '__main__':
    print(User.get_permission(user_id=1))
