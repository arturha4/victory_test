from typing import Optional

from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    admin = 'admin'
    manager = 'manager'
    user = 'user'


class User(BaseModel):
    telegram_id: Optional[int]
    role: Role
