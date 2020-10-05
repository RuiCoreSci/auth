from functools import wraps
from typing import Optional, Tuple

from graphql import GraphQLResolveInfo
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from starlette.authentication import AuthenticationBackend
from starlette.requests import HTTPConnection

from authority.credentials import AuthCredentials, AuthUser
from authority.token import Token
from exceptions import InvalidToken, OperationNotAllowed
from redis import redis
from settings import JWT_AUTH_HEADER


class _Authenticate:
    @staticmethod
    async def verify(token: str):
        try:
            payload = Token.decode(token)
        except (InvalidSignatureError, InvalidTokenError, DecodeError) as e:
            raise InvalidToken("token 格式错误") from e
        except ExpiredSignatureError:
            if payload.device == "mobile":  # noqa
                "we cat set mobile token to be valid forever"
                return payload
            else:
                raise InvalidToken("登陆过期,请重新登陆")
        else:
            token = await redis.execute("GET", f"{payload.id}-{token}")
            if token is None:
                raise InvalidToken("登陆过期,请重新登陆")
            return payload


class StarAuthenticate(AuthenticationBackend):
    async def authenticate(
        self, request: HTTPConnection
    ) -> Optional[Tuple[AuthCredentials, AuthUser]]:
        if JWT_AUTH_HEADER not in request.headers:
            return AuthCredentials(scopes=[]), AuthUser(user_id=None)

        auth = request.headers[JWT_AUTH_HEADER]
        try:
            scheme, token = auth.split()
            if scheme.lower() != 'token':
                return
            payload = await _Authenticate.verify(token)
        except Exception as exc:
            return AuthCredentials(scopes=[], error_message=str(exc)), AuthUser(user_id=None)

        return AuthCredentials(scopes=[], logged_in=True), AuthUser(user_id=payload.id)


def login_required(func):
    @wraps(func)
    async def wrap(parent, info: GraphQLResolveInfo, *args, **kwargs):
        auth: AuthCredentials = info.context["request"].auth
        if not auth.logged_in:
            raise OperationNotAllowed(auth.error_message)
        return await func(parent, info, *args, **kwargs)

    return wrap
