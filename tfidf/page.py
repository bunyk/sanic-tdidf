from sanic.views import HTTPMethodView
from sanic.response import json

class PageView(HTTPMethodView): 
    def get(self, request, title):
        print("Getting", title)
        return json({"hello": "world"})

    def post(self, request, title):
        print("posting", title)
        return json({"hello": "world"})
