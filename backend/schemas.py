from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

"""
ユーザとAPIあるいは関数同士でどういうデータをやり取りするのか定義
"""

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    password: str
    address: Optional[str] = None

class CreatedUserOut(BaseModel):
    user_name: str
    user_email: EmailStr

    class Config: # 返すときはこれで返さないとエラーが出る。
        orm_mode = True

class UserLogin(BaseModel):
    user_email: str
    password: str

class PostBase(BaseModel):
    content: str
    mind: str

class Post(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

class PostCreate(PostBase):
    user_name: str

class SharePost(PostBase):
    created_at: datetime

    class Config:
        orm_mode = True

class UserOpinionSupport(BaseModel):
    user_email: EmailStr
    tag: str
    content: str

class TokenData(BaseModel):
    user_email: Optional[str] = None