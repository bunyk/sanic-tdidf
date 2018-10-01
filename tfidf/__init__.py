from sanic import Sanic
from sanic.response import json

from .database_setup import attach_db
from .page import PageView


def create_app():
    ''' Creates configured application with db connection pool and routes '''
    app = Sanic(load_env='TFIDF_')

    attach_db(app)

    app.add_route(PageView.as_view(), '/page/<title>')

    app.static('/', './static')
    app.static('/', './static/index.html')
    return app


app = create_app()
print("ROUTES:", app.router.routes_names)

