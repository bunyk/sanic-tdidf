from sanic.views import HTTPMethodView
from sanic.response import json

from tfidf.database_setup import acquire_pool

class PageView(HTTPMethodView): 
    async def get(self, request, title):
        print("Getting", title)
        async with acquire_pool() as connection:
            results = await connection.fetch('SELECT title, text FROM pages WHERE title = $1', title)
            print(results)
        return json({"hello": "world"})

    async def post(self, request, title):
        async with acquire_pool() as connection:
            async with connection.transaction():
                await connection.execute('''
                    INSERT INTO pages (title, text) VALUES ($1, $2)
                ''', title, request.json['text']
                )
                return json({"status": "success"})
