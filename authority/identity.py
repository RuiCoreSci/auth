from authority.password import Password
from exceptions import InvalidPassword, ObjectNotExist
from orm import User as OrmUser
from orm.base import session
from validations import User


class Identity:
    @staticmethod
    def identity(user_id: int, password: str) -> User:
        user = session.query(OrmUser).filter_by(id=user_id).first()
        if not user:
            raise ObjectNotExist("用户不存在")
        user = User(**user.dict())
        if not Password.verify(password, user.password):
            raise InvalidPassword("用户密码错误")
        return user
