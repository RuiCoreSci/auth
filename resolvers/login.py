from graphql import GraphQLResolveInfo

from authority.authenticate import login_required
from authority.authorize import Authorize
from authority.identity import Identity
from authority.password import Password
from orm import User
from orm.base import global_session
from resolvers.base import mutation, query
from settings import DEVICE_HEADER, JWT_AUTH_HEADER
from validations import CreateUser


@mutation.field("register")
async def register(*_, create: dict = None) -> User:
    create_user = CreateUser(**create)
    create_user.password = Password.encode(create_user.password)
    return User.create(**create_user.dict())


@query.field("login")
async def login(_, info: GraphQLResolveInfo, id: int, password: str) -> str:
    try:
        device = info.context["request"].headers[DEVICE_HEADER]
    except KeyError:
        device = "pc"
    auto_delete = False if device == "mobile" else True
    user = Identity.identity(user_id=id, password=password)
    return await Authorize.authorize(user, device=device, auto_delete=auto_delete)


@query.field("logout")
@login_required
async def logout(_, info: GraphQLResolveInfo, id: int) -> bool:
    token = info.context["request"].headers[JWT_AUTH_HEADER]
    return await Authorize.revoke(token)


@query.field("user")
@login_required
async def get_user(*_, id: int):
    return global_session.query(User).filter(User.id == id).first()
