import uuid
from uuid6 import uuid7
from sqlalchemy import Column , String,Integer,TIMESTAMP,func ,ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database.dbconn import Base
from sqlalchemy.dialects import postgresql as psql

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  
    # app_user = relationship("AppUser",back_populates="main_user")
    

    
class AppUser(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=True)
    profile_image = Column(String, nullable=True)

    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())  
    main_user_id = mapped_column(ForeignKey("users.id"))
    # main_user = relationship("User", back_populates="main_user")
    # user_chat = relationship("Chat",back_populates="app_user")
    
    
    

class Chat(Base):
    __tablename__="user_chat"
    id = Column(Integer, primary_key=True, index=True)
    chat_title= Column(String, nullable=True)
    app_user_id = mapped_column(ForeignKey("app_users.id"))
    # app_user = relationship("AppUser", back_populates="app_users")
    