from sqlalchemy import Column, Integer, Boolean, VARCHAR

from db.orm import Base


class User(Base):
    __tablename__ = "users"

    id_number = Column("id", Integer, primary_key=True)
    username = Column(VARCHAR(20), nullable=False)
    password = Column(VARCHAR(100), nullable=False)
    is_admin = Column(Boolean, nullable=False)


class Task(Base):
    __tablename__ = "tasks"

    id_number = Column("id", Integer, primary_key=True)
    description = Column(VARCHAR(50), nullable=False)
    priority = Column(Integer, nullable=True)
    is_completed = Column(Boolean, nullable=False)
