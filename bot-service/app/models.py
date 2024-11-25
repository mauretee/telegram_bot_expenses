from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import MONEY


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    expenses = relationship("Expenses", back_populates="user")


class Expenses(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(MONEY, nullable=False)
    category = Column(String, nullable=False)
    added_at = Column(TIMESTAMP, server_default=text("now()"))
    user = relationship("User", back_populates="expenses")
