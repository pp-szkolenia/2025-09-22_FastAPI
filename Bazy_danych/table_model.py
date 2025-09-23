from sqlalchemy import Column, Integer, String, Text, Boolean, Date, Float, DateTime
from datetime import datetime, timedelta

from base import Base
    

class Task(Base):
    __tablename__ = "tasks"

    user_id = Column("id", Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    email = Column("email_address", String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    date_of_birth = Column(Date)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self) -> str:
        return f"User(id={self.user_id}, username={self.username})"
        