from pydantic import BaseModel,EmailStr, conint
from datetime import datetime
from typing import Optional

class Post(BaseModel):            # it serves as a schema for validating data
    title: str
    content:str
    published: bool = True

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        form_attributes= True

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    created_at:datetime
    user_id:int
    user:UserResponse
    class Config:
        form_attributes= True

class PostOut(BaseModel):
    Post:PostResponse
    Votes:Optional[int]
    class Config:
        form_attributes= True
    
class UserCreate(BaseModel):
    email:EmailStr
    password:str
        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:Optional[str] = None
    
class Vote(BaseModel):
    post_id:int
    dir:conint(le=1) # type: ignore