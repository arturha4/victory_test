import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from db import PgAsyncConn

API_TOKEN = '8481581028:AAFWhYT_nTmdeHfZM4Svw8fKCTwbficsloA'

# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()
pg_conn = PgAsyncConn()
router = Router()
dp.include_router(router)

# Хранение пользователей и ролей


ROLE_USER = "user"
ROLE_MODERATOR = "moderator"
ROLE_ADMIN = "admin"
DEFAULT_ROLE = ROLE_USER
users = {766109265: ROLE_ADMIN}
# Запланированные рассылки
scheduled_mailings = []

@router.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in users:
        users[user_id] = DEFAULT_ROLE
    await pg_conn.query()
    await message.answer("Привет! Вы используете бота.")

@router.message(Command(commands=["stats"]))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    if users.get(user_id) == ROLE_ADMIN:
        await message.answer(f"Всего пользователей бота: {len(users)}")
    else:
        await message.answer("Доступ запрещён. Команда только для администратора.")

@router.message(Command(commands=["setrole"]))
async def cmd_setrole(message: types.Message):
    user_id = message.from_user.id
    if users.get(user_id) != ROLE_ADMIN:
        await message.answer("Доступ запрещён. Команда только для администратора.")
        return
    args = message.text.split()
    if len(args) != 3:
        await message.answer("Использование: /setrole user_id роль (user, moderator, admin)")
        return
    try:
        target_id = int(args[1])
        role = args[2].lower()
        if role not in [ROLE_USER, ROLE_MODERATOR, ROLE_ADMIN]:
            await message.answer("Роль должна быть: user, moderator или admin")
            return
        users[target_id] = role
        await message.answer(f"Роль пользователя {target_id} изменена на {role}")
    except ValueError:
        await message.answer("Неверный user_id")

@router.message(Command(commands=["broadcast"]))
async def cmd_broadcast(message: types.Message):
    user_id = message.from_user.id
    if users.get(user_id) != ROLE_MODERATOR:
        await message.answer("Доступ запрещён. Команда только для модератора.")
        return
    text = message.get_args()
    if not text:
        await message.answer("Использование: /broadcast текст_рассылки")
        return
    scheduled_mailings.append({'creator': user_id, 'text': text})
    for uid in users.keys():
        try:
            await bot.send_message(uid, text)
        except Exception:
            pass  # Игнорируем ошибки отправки
    await message.answer("Рассылка отправлена всем пользователям.")

@router.message(Command(commands=["mailings"]))
async def cmd_mailings(message: types.Message):
    user_id = message.from_user.id
    if users.get(user_id) != ROLE_ADMIN:
        await message.answer("Доступ запрещён. Команда только для администратора.")
        return
    if not scheduled_mailings:
        await message.answer("Нет запланированных рассылок.")
        return
    msg = "Запланированные рассылки:\n"
    for i, mailing in enumerate(scheduled_mailings, 1):
        snippet = mailing['text'][:30].replace('\n', ' ') + ("..." if len(mailing['text']) > 30 else "")
        msg += f"{i}. От модератора {mailing['creator']}: {snippet}\n"
    await message.answer(msg)

async def main():
    await pg_conn.init_db_pool()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
