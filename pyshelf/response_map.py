from pyshelf.json_response import JsonResponse
from pyshelf.error_code import ErrorCode


def vnd_error(error):
    """
        Creates vnd.error type error responses
        https://github.com/blongden/vnd.error
    """
    body = {
        "code": error["code"],
        "message": error["message"]
    }
    status_code = error.get("status_code", 500)
    response = JsonResponse()
    response.status_code = status_code
    response.data = body
    return response


def create_404(msg=None):
    if msg is None:
        msg = "Resource not found"
    error = {
        "code": ErrorCode.RESOURCE_NOT_FOUND,
        "message": msg,
        "status_code": 404
    }

    return vnd_error(error)


def create_500(msg=None):
    if msg is None:
        msg = "Internal Server Error"
    error = {
        "code": ErrorCode.INTERNAL_SERVER_ERROR,
        "message": msg,
        "status_code": 500
    }

    return vnd_error(error)

def create_201():
    body = {
        "message": "Creation request has been fulfilled",
        "status_code": 201
    }
    response = JsonResponse()
    response.status_code = 201
    response.data = body
    return response
