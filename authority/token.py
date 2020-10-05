from datetime import datetime

import jwt

from settings import JWT_ALGORITHM, JWT_SECRET_KEY
from validations import PayLoad, User


class Token:
    @staticmethod
    def encode(user: User, exp: datetime, device: str = "pc") -> str:
        payload = {"id": user.id, "device": device, "exp": exp}
        return jwt.encode(payload, JWT_SECRET_KEY, JWT_ALGORITHM).decode("UTF-8")

    @staticmethod
    def decode(token: str) -> PayLoad:
        payload = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return PayLoad(**payload)
