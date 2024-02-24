from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class PostBase(BaseModel):
    title : str
    content : str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostRespone(PostBase):
    id : int
    created_at : datetime
    owner: UserResponse
    
    class Config:
        orm_mode = True


class VoteBase(BaseModel):
    post_id: int
    direction: conint(le=1)