from pyshelf.json_response import JsonResponse

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

def create_403(error_code, msg=None):
    if msg is None:
        msg = "Forbidden"
    error = {    
        "code": error_code,
        "message": msg,
        "status_code": 403
    }
    
    return vnd_error(error)

def create_404(error_code, msg=None):
    if msg is None:
        msg = "Resource not found"
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 404
    }

    return vnd_error(error)


def create_500(error_code, msg=None):
    if msg is None:
        msg = "Internal Server Error"
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 500
    }

    return vnd_error(error)


def create_201():
    body = {
        "success": True
    }
    response = JsonResponse()
    response.status_code = 201
    response.data = body
    return response
