import email
from pydantic import BaseModel, EmailStr ,ConfigDict
from typing import Literal, Optional

from core import password
from schemas.access_role import AccesRole

class GetUser(BaseModel):
    email: EmailStr
    username: Optional[str]
    role: Literal["user","admin","system"]
    model_config = ConfigDict( use_enum_values = True  , from_attributes = True)


class LoginUser(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict( use_enum_values = True  , from_attributes = True)


class PostUser(BaseModel):
    email: EmailStr
    username: Optional[str]
    role:AccesRole
    model_config = ConfigDict( use_enum_values = True  , from_attributes = True)


class CreateUser(BaseModel):
    email:EmailStr
    username:Optional[str]
    password:str
    role:AccesRole
    