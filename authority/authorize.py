from datetime import datetime, timedelta

from authority.token import Token
from redis import redis
from settings import JWT_LIFE_SPAN
from validations import User


class Authorize:
    @staticmethod
    async def authorize(user: User, device: str = "pc") -> str:
        exp = datetime.utcnow() + timedelta(seconds=JWT_LIFE_SPAN)
        token = Token.encode(user, exp=exp, device=device)
        expire_at = (exp + timedelta(seconds=JWT_LIFE_SPAN)).timestamp()
        await redis.execute("SET", f"{user.id}-{token}", "True")
        await redis.execute("EXPIREAT", f"{user.id}-{token}", int(expire_at))
        return token

    @staticmethod
    async def revoke(token: str):
        try:
            payload = Token.decode(token)
        except:  # noqa
            pass
        else:
            await redis.execute("DEL", f"{payload.id}-{token}")

    @staticmethod
    async def revoke_all(user: User):
        tokens = await redis.execute("KEYS", f"{user.id}-*")
        await redis.execute("DEL", *tokens)
