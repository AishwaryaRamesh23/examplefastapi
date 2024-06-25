from sqlalchemy import Column,Integer,String,Boolean,func,ForeignKey,TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__="smposts"
    id= Column(Integer,primary_key= True, nullable= False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='True',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    user=relationship("User")

class User(Base):
    __tablename__="users"
    id= Column(Integer,primary_key= True, nullable= False)
    email=Column(String,nullable=False,unique=True)
    e_password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    phone_number=Column(String)

class Vote(Base):
    __tablename__="votes"
    post_id=Column(Integer,ForeignKey("smposts.id",ondelete="CASCADE"),primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    