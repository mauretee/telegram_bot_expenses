from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class Expenses(BaseModel):
    user_id: int
    description: Optional[str] = None
    amount: Optional[Decimal] = None
    category: Optional[str] = None

    class Config:
        orm_mode = True


class CreateExpenses(BaseModel):
    telegram_id: int
    message: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    telegram_id: int

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    telegram_id: int

    class Config:
        orm_mode = True
