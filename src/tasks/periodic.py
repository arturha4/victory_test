import asyncio
from celery import Celery

from ..bot import settings, bot

app = Celery('tasks',
             broker=settings.BROKER_URL,
             backend=settings.BROKER_URL)


@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    sender.add_periodic_task(10.0, send_telegram_message.s(766109265, 'hello'), name='add every 10')


def send_message_sync(chat_id: int, text: str):
    async def main():
        await bot.send_message(settings.TELEGRAM_BOT_ADMIN_ID, text)
        await bot.session.close()
    asyncio.run(main())


@app.task
def send_telegram_message(chat_id: int, text: str):
    send_message_sync(chat_id, text)
