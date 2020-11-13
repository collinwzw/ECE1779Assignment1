from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def error_response(status_code, message=None):
    '''
    Function that returns required format error json
    :param: status_code:http error code, error message:detailed customized error message
    :return:json
    '''
    payload = {"success": False,"error":{ "code":status_code}}
    if message:
        payload['error']['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response