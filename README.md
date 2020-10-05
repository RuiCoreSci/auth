# 权限验证

 ![python3.8](https://img.shields.io/badge/language-python3.8-blue.svg) &nbsp; ![framework](https://img.shields.io/badge/framework-graphql-blue) &nbsp; ![issues](https://img.shields.io/github/issues/RuiCoreSci/auth) ![stars](https://img.shields.io/github/stars/RuiCoreSci/auth) &nbsp; ![license](https://img.shields.io/github/license/RuiCoreSci/auth)

* 此项目是模板项目，使用 PyJwt 进行基本的登录验证。
* 基于 pyjwt、[ariadne](https://github.com/mirumee/ariadne)、[aioredis](https://github.com/aio-libs/aioredis)、[starlette](https://github.com/encode/starlette)、sqlalchmy 进行开发。
* 使用 redis 存储 token，token 的有效期为一天，用户可以选择登出，登出即撤销 token。

**目录**

<!-- TOC -->

- [权限验证](#%E6%9D%83%E9%99%90%E9%AA%8C%E8%AF%81)
    - [认证](#%E8%AE%A4%E8%AF%81)
    - [授权](#%E6%8E%88%E6%9D%83)
    - [鉴权](#%E9%89%B4%E6%9D%83)

<!-- /TOC -->

## 认证
* 认证是指根据声明者所持有的信息，确认声明者的身份，在英文中对应 `identification`。常见的认证方式是【用户名 + 密码】。
* 此模块对登录的用户进行认证。

```py
class Identity:
    @staticmethod
    def identity(user_id: int, password: str) -> User:
```
* 验证输入的 id【可以替换成任意能唯一标识用户的属性】对应的用户密码和输入的密码是否一致，若一致，返回用户，否则抛出异常。

## 授权
* 授权是指资源所有者委派资源执行者，赋予执行者指定范围的资源操作权限，在英文中对应 `authorization`。
* 此模块进行授权，为 user 返回生成的 token。
```py
    async def authorize(user: User, device: str = "pc", auto_delete=True) -> str:
    pass
```
* authorize 方法接收三个参数，用户 `user`，设备类型 `device`,以及是否主动删除过期 token `auto_delete`。


## 鉴权
* 鉴权是指对于一个声明者所声明的权限，对声明的真实性进行鉴别并确认的过程，在英文中对应 `authentication`。
* 此模块进行 token 验证，验证 token 是否有效。
```py
class _Authenticate:
    @staticmethod
    async def verify(token: str):
      pass
```
* verify 对 token 进行验证，验证 token 是否合法；对于某些设备【比如移动端】，即使 token 超过了有效期，仍然可以认为这个 token 有效；因此 token 有效的规则是：

```py
1、token 格式合法 && token 在 redis 数据库中存在 && token 没有过有效期 or
2、token 格式合法 && token 在 redis 数据库中存在 && token 过期 && token 为指定类型
```

* 一般来说，这几者之间的关系是 **认证**-->**授权**-->**鉴权**-->**权限控制**（本文未列出）。

<!-- TOC ignore:true -->
## Maintainers

[@ ruicore](https://github.com/ruicore)

<!-- TOC ignore:true -->
## Contributing

PRs are accepted.

<!-- TOC ignore:true -->
## License

MIT © 2020 ruicore
