from asyncpg import create_pool

_pool = None

async def register_db(app, loop):
    global _pool
    _pool = await create_pool(
        host=app.config.DB_HOST,
        user=app.config.DB_USER,
        password=app.config.DB_PASSWORD,
        port=app.config.DB_PORT,
        database=app.config.DB_NAME,
        loop=loop,
        max_size=100
    )
    async with acquire_pool() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS pages (
            id serial primary key,
            title varchar(255) unique not null,
            text text
        );""")

def acqire_pool():
    return _pool.acquire()

def attach_db(app):
    before_server_start = app.listener('before_server_start')
    before_server_start(register_db)
