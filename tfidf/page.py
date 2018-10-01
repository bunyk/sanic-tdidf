'''
    Defines page views
'''
from sanic.views import HTTPMethodView
from sanic.response import json
from sanic.exceptions import InvalidUsage
from asyncpg import PostgresError, UniqueViolationError

from .database_setup import acquire_pool
from .helpers import error_response

# TODO: move out models

class PageView(HTTPMethodView):
    ''' Holds methods to work with page resource '''

    async def get(self, _, title):
        ''' Returns page content by title '''
        async with acquire_pool() as connection:
            results = await connection.fetch(
                'SELECT title, text FROM pages WHERE title = $1',
                title
            )
            if not results:
                return json({
                    "status": "HTTP 404",
                    "message": "Page not found",
                }, status=404)
            return json({
                "text": results[0],
                "title": title,
            })

    async def post(self, request, title):
        ''' Updates page content by title '''
        try:
            text = request.json['text']
        except InvalidUsage as e:
            return error_response(e)
        async with acquire_pool() as connection:
            async with connection.transaction():
                try:
                    await connection.execute(
                        'INSERT INTO pages (title, text) VALUES ($1, $2)',
                        title, text
                    )
                except UniqueViolationError:
                    pass # TODO: add UPDATE HERE
                except PostgresError as e:
                    return error_response(e)
                return json({"status": "success"})
