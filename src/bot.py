import asyncio

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from src.config import settings
from src.database.models import Role, TaskStatus
from src.database.services import (
    create_user,
    get_user,
    get_count_of_users,
    patch_user,
    get_users,
    get_count_of_tasks,
    create_task,
    change_task_status)

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)


@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await get_user(telegram_id)
    if not user:
        if settings.TELEGRAM_BOT_ADMIN_ID == str(message.from_user.id):
            await create_user(telegram_id, Role.admin)
        else:
            await create_user(telegram_id, Role.user)
        await message.answer(f"Привет {message.from_user.username}! Теперь, вы используете бота.\n"
                             f"Команды бота: \n"
                             f"/stats - получить статистику по пользователям и рассылкам.\n"
                             f"/setrole <Telegram ID> <user, manager или admin> - изменить роль пользователя\n"
                             f"/broadcast <Текст рассылки>")
    else:
        await message.answer(f"Привет {message.from_user.username}!")


@router.message(Command(commands=["stats"]))
async def cmd_stats(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await get_user(telegram_id)
    if user and user.role == Role.admin:
        user_count = await get_count_of_users()
        task_count = await get_count_of_tasks()
        await message.answer(f"Всего пользователей бота: {user_count}\nВсего задач: {task_count}")
    else:
        await message.answer("Доступ запрещён. Команда только для администратора.")


@router.message(Command(commands=["setrole"]))
async def cmd_setrole(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await get_user(telegram_id)
    if not user or user.role != Role.admin:
        await message.answer("Доступ запрещён. Команда только для администратора.")
        return
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Использование: /setrole user_id роль (user, manager, admin)")
        return
    try:
        target_id = str(args[1])
        role_str = args[2].lower()
        if role_str not in Role._value2member_map_:
            await message.answer("Роль должна быть: user, manager или admin")
            return
        role = Role(role_str)
        target_user = await get_user(target_id)
        if not target_user:
            await message.answer(f"Пользователь с telegram_id={target_id} не найден.")
            return
        await patch_user(target_user, role)
        await message.answer(f"Роль пользователя {target_id} изменена на {role.value}")
    except ValueError:
        await message.answer("Неверный user_id")


@router.message(Command(commands=["broadcast"]))
async def cmd_broadcast(message: types.Message):
    telegram_id = str(message.from_user.id)
    user = await get_user(telegram_id)
    if not user or user.role != Role.manager:
        await message.answer("Доступ запрещён. Команда только для менеджера.")
        return
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        await message.answer("Использование: /broadcast текст_рассылки")
        return
    users = await get_users()
    task = await create_task(user.id)
    await change_task_status(task, TaskStatus.pending)
    for telegram_id in users:
        try:
            await message.bot.send_message(telegram_id, text)
        except Exception:
            pass
    await change_task_status(task, TaskStatus.finished)
    await message.answer("Рассылка отправлена всем пользователям.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
