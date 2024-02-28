from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
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

class PostResponse(PostBase):
    id : int
    created_at : datetime
    owner: UserResponse
    
    class ConfigDict:
        from_attributes = True

class PostOutResponse(BaseModel):
    Post: PostResponse
    votes: int

    class ConfigDict:
        from_attributes = True

class VoteBase(BaseModel):
    post_id: int
    direction: conint(le=1)