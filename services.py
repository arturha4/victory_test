from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from db import connection
from models import (
    User,
    Role, Task, TaskStatus
)


@connection
async def create_user(telegram_id: str, role: Role, session: AsyncSession = None):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user is not None:
        return
    user = User(
        telegram_id=telegram_id,
        role=role
    )
    session.add(user)
    await session.commit()
    return user


@connection
async def get_user(telegram_id: str, session: AsyncSession = None):
    query = select(User).where(User.telegram_id == telegram_id)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    return existing_user


@connection
async def get_count_of_users(session: AsyncSession = None):
    res = await session.execute(select(func.count()).select_from(User))
    count = res.scalar_one()
    return count


@connection
async def patch_user(user: User, role: Role, session: AsyncSession = None):
    user.role = role
    session.add(user)
    await session.commit()


@connection
async def get_users(session: AsyncSession):
    q = select(User.telegram_id)
    result = await session.execute(q)
    user_ids = [int(tid) for tid, in result.all()]
    return user_ids


@connection
async def get_tasks(session: AsyncSession):
    q = await session.execute(select(Task))
    tasks = q.scalars().all()
    return tasks


@connection
async def get_count_of_tasks(session: AsyncSession = None):
    res = await session.execute(select(func.count()).select_from(Task))
    count = res.scalar_one()
    return count


@connection
async def create_task(creator_id: str, session: AsyncSession):
    task = Task(creator_id=creator_id)
    session.add(task)
    await session.commit()
    return task


@connection
async def close_task(task_id: int, session: AsyncSession):
    q = select(Task).where(Task.id == task_id)
    task = await session.execute(q)
    task.status = TaskStatus.finished
    session.add(task)
    await session.commit()

@connection
async def change_task_status(task: Task, status: TaskStatus, session: AsyncSession):
    task.status = status
    session.add(task)
    await session.commit()
    return session
