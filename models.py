from datetime import datetime
from enum import Enum

from sqlalchemy import Integer, func, String, text, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'


class Role(str, Enum):
    admin = 'admin'
    manager = 'manager'
    user = 'user'


class TaskStatus(str, Enum):
    pending = 'pending'
    active = 'active'
    finished = 'finished'


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[str] = mapped_column(String, unique=True)
    role: Mapped[Role] = mapped_column(
        default=Role.user,
        server_default=text("'user'")
    )


class Task(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    status: Mapped[TaskStatus] = mapped_column(
        default=TaskStatus.pending,
        server_default=text("'pending'")
    )
