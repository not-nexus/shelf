from pyshelf.json_response import JsonResponse
from pyshelf.cloud.cloud_exceptions import \
    ArtifactNotFoundError, BucketNotFoundError, DuplicateArtifactError, InvalidNameError
from pyshelf.error_code import ErrorCode
from pyshelf.metadata.error_code import ErrorCode as MetadataErrorCode


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
    response.set_data(body)
    return response


def create_403(error_code=None, msg=None):
    """
        Creates a 403 response using vnd.error

        args:
            error_code(pyshelf.error_code.ErrorCode):
                Defaults to ErrorCode.FORBIDDEN if a more specific code is not supplied
            msg(basestring): Defaults to "Forbidden" if a specific message is not supplied
        Returns:
            vnd.error formatted error response
    """
    if msg is None:
        msg = "Forbidden"
    if error_code is None:
        error_code = ErrorCode.FORBIDDEN
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 403
    }
    return vnd_error(error)


def create_404(error_code=None, msg=None):
    """
        Creates a 404 response using vnd.error

        args:
            error_code(pyshelf.error_code.ErrorCode):
                Defaults to ErrorCode.RESOURCE_NOT_FOUND if a more specific code is not supplied
            msg(basestring): Defaults to "Resource not found" if a specific message is not supplied
        Returns:
            vnd.error formatted error response
    """
    if msg is None:
        msg = "Resource not found"
    if error_code is None:
        error_code = ErrorCode.RESOURCE_NOT_FOUND
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 404
    }

    return vnd_error(error)


def create_400(error_code, msg):
    """
        Creates response wiih 400 status code.

        Args:
            error_code(pyshelf.error_code.ErrorCode):
            msg(string)

        Returns:
            flask Response
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 400
    }

    return vnd_error(error)


def create_500(error_code=None, msg=None):
    """
        Creates a 500 response using vnd.error

        args:
            error_code(pyshelf.error_code.ErrorCode):
                Defaults to ErrorCode.INTERNAL_SERVER_ERROR if a more specific code is not supplied
            msg(basestring): Defaults to "Internal server error" if a specific message is not supplied
        Returns:
            vnd.error formatted error response
    """
    if msg is None:
        msg = "Internal server error"
    if error_code is None:
        error_code = ErrorCode.INTERNAL_SERVER_ERROR
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 500
    }

    return vnd_error(error)


def create_201():
    """
        Creates a 201 response
    """
    body = {
        "success": True
    }
    response = JsonResponse()
    response.status_code = 201
    response.set_data(body)
    return response


def create_204():
    """
        Creates a 204 response
    """
    response = JsonResponse()
    response.status_code = 204
    return response


def create_200(body=None):
    """
        Creates a 200 response

        Args:
            body(dict): body of response.
    """
    if body is None:
        body = {"success": True}
    response = JsonResponse()
    response.status_code = 200
    response.set_data(body)
    return response


def map_exception(e):
    """
        Maps exception to a response. This way you can catch a generic
        CloudStorageException.

        Args:
            e(Exception): instance of the exception that was caught

        Returns:
            vnd.error formatted error response
    """
    if isinstance(e, ArtifactNotFoundError):
        return create_404(e.error_code, e.message)
    if isinstance(e, DuplicateArtifactError) or isinstance(e, InvalidNameError):
        return create_403(e.error_code, e.message)
    if isinstance(e, BucketNotFoundError):
        return create_500(e.error_code, e.message)
    return create_500()


def map_context_error(context):
    """
        Maps errors set on pyshelf.context.Context

        Args:
            context(pyshelf.context.Context)

        Returns:
            flask Response
    """
    if ErrorCode.INVALID_SEARCH_CRITERIA in context.error_list:
        return create_400(ErrorCode.BAD_REQUEST, "Invalid search and/or sort criteria.")


def map_metadata_result_errors(result):
    if result.has_error(MetadataErrorCode.IMMUTABLE):
        return create_403(ErrorCode.FORBIDDEN, "Cannot update immutable metadata.")
    elif result.has_error(MetadataErrorCode.DUPLICATE):
        return create_403(ErrorCode.FORBIDDEN, "This metadata already exists.")
