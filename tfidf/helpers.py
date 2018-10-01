'''
    Different utilities to reuse
'''
from sanic.response import json

def error_response(exception):
    ''' Return json response with message of exception '''
    return json({
        "status": "error",
        "message": str(exception),
    }, status=400)
