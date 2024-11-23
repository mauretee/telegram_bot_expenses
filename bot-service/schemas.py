import hashlib
from typing import Optional

from pydantic import BaseModel


class CreateExpenses(BaseModel):
    user_id : int
    message: str

    class Config:
        orm_mode = True
