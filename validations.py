from datetime import datetime
from typing import Optional, Text

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    age: Optional[int]
    name: Optional[Text]
    phone: Optional[Text]
    password: Optional[Text]


class PayLoad(BaseModel):
    id: int
    device: Text
    exp: datetime
    iat: datetime


class CreateUser(BaseModel):
    name: Text
    age: Optional[int]
    phone: Optional[Text]
    password: Optional[Text]
