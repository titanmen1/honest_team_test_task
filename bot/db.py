import aiosqlite

# Подключение к базе данных SQLite
async def get_connection(database_name: str) -> aiosqlite.Connection:
    return aiosqlite.connect(database_name)

# Создание таблицы для хранения сообщений
async def create_table(cursor) -> None:
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')

async def insert_message(cursor, link: str, message: str) -> None:
    await cursor.execute(f"INSERT INTO messages (link, message) VALUES ('{link}', '{message}')")