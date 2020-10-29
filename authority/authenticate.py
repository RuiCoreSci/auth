from functools import wraps
from typing import Optional, Tuple

from graphql import GraphQLResolveInfo
from jwt import DecodeError, ExpiredSignatureError
from starlette.authentication import AuthenticationBackend
from starlette.requests import HTTPConnection

from authority.credentials import AuthCredentials, AuthUser
from authority.token import Token
from exceptions import InvalidToken, OperationNotAllowed
from orm import User
from redis import redis
from settings import JWT_AUTH_HEADER


class _Authenticate:
    @classmethod
    async def verify(cls, token: str):
        """
        token 有效的规则：
        1、token 格式合法 && token 在 redis 数据库中存在 && token 没有过有效期 or
        2、token 格式合法 && token 在 redis 数据库中存在 && token 过期 && token 为指定类型
        """
        try:
            payload = Token.decode(token)
        except ExpiredSignatureError:
            payload = Token.decode(token, verify_exp=False)
            if not await cls.exists(payload.user_id, token):
                raise InvalidToken("登陆过期,请重新登陆")
            if payload.device == "mobile":  # noqa
                "we cat set mobile token to be valid forever"
                return payload
        except DecodeError as e:
            raise InvalidToken("token 格式错误") from e
        else:
            if not await cls.exists(payload.user_id, token):
                raise InvalidToken("登陆过期,请重新登陆")
            return payload

    @classmethod
    async def exists(cls, user_id, token):
        token = await redis.execute("GET", f"{user_id}-{token}")
        return token is not None


class StarAuthenticate(AuthenticationBackend):
    async def authenticate(
            self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, AuthUser]]:
        if JWT_AUTH_HEADER not in request.headers:
            return AuthCredentials(scopes=[]), AuthUser(user_id=None)

        auth = request.headers[JWT_AUTH_HEADER]
        try:
            scheme, token = auth.split()
            payload = await _Authenticate.verify(token)
        except Exception as exc:
            return AuthCredentials(scopes=[], error_message=str(exc)), AuthUser(user_id=None)

        scopes = User.get_permission(user_id=payload.user_id)
        return AuthCredentials(scopes=scopes, logged_in=True), AuthUser(user_id=payload.user_id)


def login_required(func):
    @wraps(func)
    async def wrap(parent, info: GraphQLResolveInfo, *args, **kwargs):
        auth: AuthCredentials = info.context["request"].auth
        if not auth.logged_in:
            raise OperationNotAllowed(auth.error_message or "请登录")
        return await func(parent, info, *args, **kwargs)

    return wrap
