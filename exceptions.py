from graphql import GraphQLError


class BaseHttpException(GraphQLError):
    code = 500
    message = "服务器内部错误"


class InvalidToken(BaseHttpException):
    code = 403
    message = "登陆失效、请重新登陆"


class ObjectNotExist(BaseHttpException):
    code = 404
    message = "请求对象不存在"


class OperationNotAllowed(BaseHttpException):
    code = 403
    message = "没有权限"


class InvalidPassword(BaseHttpException):
    code = 401
    message = "密码错误"
