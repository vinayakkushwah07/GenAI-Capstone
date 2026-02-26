import datetime
import uuid
from uuid6 import uuid7
from sqlalchemy import Column, DateTime , String,Integer,TIMESTAMP, Text,func ,ForeignKey
from sqlalchemy.orm import relationship, mapped_column
from database.dbconn import Base
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    chat_id = Column(String, index=True)
    role = Column(String) 
    content = Column(Text)
    created_at = Column(DateTime, default= datetime.datetime.now())