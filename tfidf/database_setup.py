'''
    Defines functions to create and obtain connection pool
'''
from asyncpg import create_pool

_POOL = None

async def register_db(app, loop):
    '''
        Creates connection pool with configuration provided in app
        loop - event_loop
    '''
    global _POOL # pylint: disable=global-statement
    _POOL = await create_pool(
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

def attach_db(app):
    ''' Creates connection pool before app starts '''
    before_server_start = app.listener('before_server_start')
    before_server_start(register_db)


def acquire_pool():
    ''' Returns database connection from the pool '''
    return _POOL.acquire()
