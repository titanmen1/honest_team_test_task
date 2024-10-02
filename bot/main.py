import asyncio
import logging
import os
import aiosqlite
from dotenv import load_dotenv
from telethon import TelegramClient, events
from bot import db
from bot.utils import extract_ids

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

# Установите свои значения API ID и API Hash
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
database_name = os.getenv('DATABASE_NAME')

# Инициализация клиента
client = TelegramClient('', api_id, api_hash)

# Обработчик сообщений
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    logger.info(f'Получено сообщение /start от {event.sender.first_name}')
    await event.respond('Привет! Пришли мне ссылку на пост в телеграмм-канале.')

@client.on(events.NewMessage(pattern=r'^(?!/start).*$'))
async def handler(event):
    link = event.message.message
    logger.info(f'Получено сообщение: {link}')
    channel, message_id = extract_ids(link)
    logger.info(f'Извлечены данные: channel={channel}, message_id={message_id}')
    if channel and message_id:
        try:
            # Получение сообщения из канала
            message = await client.get_messages(channel, ids=message_id)
            message_text = message.message

            # Сохранение сообщения в базе данных
            async with aiosqlite.connect(database_name) as connection:
                await db.insert_message(cursor=connection, link=link, message=message_text)
                await connection.commit()
                logger.info('Сообщение сохранено в базе данных')


            # Отправка сообщения пользователю
            await event.respond(f'Сообщение сохранено: {message_text}')
        except Exception as e:
            logger.error(f'Ошибка при обработке сообщения: {str(e)}')
            await event.respond(f'Ошибка: {str(e)}')
    else:
        msg = 'Неверная ссылка. Пожалуйста, пришлите правильную ссылку на пост в телеграмм-канале.'
        logger.warning(msg)
        await event.respond(msg)


async def main():
    logger.info('Запуск бота')
    async with aiosqlite.connect(database_name) as connection:
        await db.create_table(cursor=connection)
        await connection.commit()
        logger.info('Таблица базы данных создана')

    await client.start(bot_token=bot_token)
    logger.info('Клиент Telegram запущен')
    await client.run_until_disconnected()




if __name__ == '__main__':
    asyncio.run(main())