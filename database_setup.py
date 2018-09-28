from asyncpg import create_pool

async def register_db(app, loop):
    app.pool = await create_pool(
        host=app.config.DB_HOST,
        user=app.config.DB_USER,
        password=app.config.DB_PASSWORD,
        port=app.config.DB_PORT,
        database=app.config.DB_NAME,
        loop=loop,
        max_size=100
    )
    async with app.pool.acquire() as connection:
        await connection.execute("""
            CREATE TABLE IF NOT EXISTS pages (
            id serial primary key,
            title varchar(255) unique not null,
            text text
        );""")

def attach_db(app):
    before_server_start = app.listener('before_server_start')
    before_server_start(register_db)
