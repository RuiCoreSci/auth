from typing import Optional

from pydantic import BaseModel


class AuthCredentials(BaseModel):
    scopes: Optional[list] = []
    logged_in: bool = False
    error_message: str = ""

    @property
    def is_admin(self):
        return True


class AuthUser(BaseModel):
    user_id: Optional[int]

    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None

    @property
    def display_id(self) -> int:
        return self.user_id
