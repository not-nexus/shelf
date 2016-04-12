from pyshelf.json_response import JsonResponse
from pyshelf.cloud.cloud_exceptions import BucketNotFoundError, ArtifactNotFoundError, \
    DuplicateArtifactError, InvalidNameError, BucketConfigurationNotFound
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


def create_403(error_code, msg):
    """
        Creates a 403 response using vnd.error

        args:
            error_code(pyshelf.error_code.ErrorCode)
            msg(string)
        Returns:
            pyshelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 403
    }
    return vnd_error(error)


def create_404(error_code=ErrorCode.RESOURCE_NOT_FOUND, msg="Resource not found"):
    """
        Creates a 404 response.

        args:
            error_code(pyshelf.error_code.ErrorCode):
            msg(string)

        Returns:
            pyshelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 404
    }

    return vnd_error(error)


def create_400(error_code=ErrorCode.BAD_REQUEST, msg="Bad request"):
    """
        Creates response wiih 400 status code.

        args:
            error_code(pyshelf.error_code.ErrorCode):
            msg(string)

        Returns:
            pyshelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 400
    }

    return vnd_error(error)


def create_500(error_code=ErrorCode.INTERNAL_SERVER_ERROR, msg="Internal server error"):
    """
        Creates a 500 response using vnd.error

        Args:
            error_code(pyshelf.error_code.ErrorCode):
            msg(string)

        Returns:
            pyshelf.json_response.JsonResponse
    """
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


def create_200(body):
    """
        Creates a 200 response

        Args:
            body(dict): body of response.
    """
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
    elif isinstance(e, DuplicateArtifactError) or isinstance(e, InvalidNameError):
        return create_403(e.error_code, e.message)
    elif isinstance(e, BucketNotFoundError):
        return create_500(e.error_code, e.message)
    elif isinstance(e, BucketConfigurationNotFound):
        return create_404()

    return create_500()


def map_context_error(context):
    """
        Maps errors set on pyshelf.context.Context

        Args:
            context(pyshelf.context.Context)

        Returns:
            flask Response
    """
    if ErrorCode.INVALID_SEARCH_CRITERIA in context.errors:
        return create_400(ErrorCode.BAD_REQUEST, context.errors[ErrorCode.INVALID_SEARCH_CRITERIA])


def map_metadata_result_errors(result):
    if result.has_error(MetadataErrorCode.IMMUTABLE):
        return create_403(ErrorCode.FORBIDDEN, "Cannot update immutable metadata.")
    elif result.has_error(MetadataErrorCode.DUPLICATE):
        return create_403(ErrorCode.FORBIDDEN, "This metadata already exists.")
