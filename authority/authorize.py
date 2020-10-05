from datetime import datetime, timedelta

from authority.token import Token
from redis import redis
from settings import JWT_LIFE_SPAN
from validations import User


class Authorize:
    @staticmethod
    async def authorize(user: User, device: str = "pc", auto_delete=True) -> str:
        """
        :param user:
        :param device:
        :param auto_delete: 过期是否自动删除，默认为 True
        :return:
        """
        exp = datetime.utcnow() + timedelta(seconds=JWT_LIFE_SPAN)
        token = Token.encode(user, exp=exp, device=device)
        await redis.execute("SET", f"{user.id}-{token}", "True")
        if auto_delete:
            expire_at = (exp + timedelta(seconds=JWT_LIFE_SPAN)).timestamp()
            await redis.execute("EXPIREAT", f"{user.id}-{token}", int(expire_at))
        return token

    @staticmethod
    async def revoke(token: str) -> bool:
        try:
            payload = Token.decode(token)
        except:  # noqa
            pass
        else:
            await redis.execute("DEL", f"{payload.id}-{token}")
        return True

    @staticmethod
    async def revoke_all(user: User):
        tokens = await redis.execute("KEYS", f"{user.id}-*")
        await redis.execute("DEL", *tokens)
