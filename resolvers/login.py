from graphql import GraphQLResolveInfo

from authority.authenticate import login_required
from authority.authorize import Authorize
from authority.identity import Identity
from authority.password import Password
from orm import User
from orm.base import session
from resolvers.base import mutation, query
from settings import JWT_AUTH_HEADER
from validations import CreateUser


@mutation.field("register")
async def register(*_, create: dict = None) -> User:
    create_user = CreateUser(**create)
    create_user.password = Password.encode(create_user.password)
    user = User(**create_user.dict())
    session.add(user)
    session.commit()
    return user


@query.field("login")
async def login(*_, id: int, password: str) -> str:
    user = Identity.identity(user_id=id, password=password)
    return await Authorize.authorize(user)


@query.field("logout")
@login_required
async def logout(_, info: GraphQLResolveInfo, id: int) -> bool:
    token = info.context["request"].headers[JWT_AUTH_HEADER]
    await Authorize.revoke(token)
    return True


@query.field("user")
@login_required
async def get_user(*_, id: int):
    return session.query(User).filter(User.id == id).first()
