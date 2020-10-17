from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    payload = {"success": False,"error":{ "code":HTTP_STATUS_CODES.get(status_code, 'Unknown error')}}
    if message:
        payload['error']['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response