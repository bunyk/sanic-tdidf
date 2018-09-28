from sanic import Sanic
from sanic.response import json

from tfidf.database_setup import attach_db
from tfidf.page import PageView


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config.PORT)
