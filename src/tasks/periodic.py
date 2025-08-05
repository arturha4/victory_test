import asyncio

from celery import Celery

from ..bot import bot

app = Celery('tasks',
             broker='redis://broker:6379/0',
             backend='redis://broker:6379/0')


# @app.task(name='tasks.add')
# def create_celery_task_send_message(text: str, chat_id: str) -> None:
#     """Таска для отправки напоминания о задаче"""
#     asyncio.run(send_notification_message(text, chat_id))
#
#
# async def send_notification_message(text: str, chat_id: str) -> None:
#     """Отправляем напоминалку"""
#     message = text
#     await bot.send_message(chat_id=chat_id, text=message)


def send_message_sync(chat_id: int, text: str):
    async def main():
        await bot.send_message(chat_id, text)
        await bot.session.close()

    asyncio.run(main())


@app.task
def send_telegram_message(chat_id: int, text: str):
    send_message_sync(chat_id, text)