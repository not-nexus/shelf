from shelf.json_response import JsonResponse
from shelf.cloud.cloud_exceptions import ArtifactNotFoundError, DuplicateArtifactError, BucketConfigurationNotFound
from shelf.error_code import ErrorCode
from shelf.metadata.error_code import ErrorCode as MetadataErrorCode


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
            error_code(shelf.error_code.ErrorCode)
            msg(string)
        Returns:
            shelf.json_response.JsonResponse
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
            error_code(shelf.error_code.ErrorCode):
            msg(string)

        Returns:
            shelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 404
    }

    return vnd_error(error)


def create_400(error_code=ErrorCode.BAD_REQUEST, msg="Bad request"):
    """
        Creates response with 400 status code.

        args:
            error_code(shelf.error_code.ErrorCode):
            msg(string)

        Returns:
            shelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 400
    }

    return vnd_error(error)


def create_401(error_code=ErrorCode.PERMISSION_DENIED, msg="Permission denied"):
    """
        Creates response with 401 status code.

        args:
            error_code(shelf.error_code.ErrorCode):
            msg(string)

        Returns:
            shelf.json_response.JsonResponse
    """
    error = {
        "code": error_code,
        "message": msg,
        "status_code": 401
    }

    return vnd_error(error)


def create_500(error_code=ErrorCode.INTERNAL_SERVER_ERROR, msg="Internal server error"):
    """
        Creates a 500 response using vnd.error

        Args:
            error_code(shelf.error_code.ErrorCode):
            msg(string)

        Returns:
            shelf.json_response.JsonResponse
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
    response = JsonResponse()
    response.status_code = 201
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
    elif isinstance(e, DuplicateArtifactError):
        return create_403(e.error_code, e.message)
    elif isinstance(e, BucketConfigurationNotFound):
        return create_404()

    return create_500()


def map_context_error(context):
    """
        Maps errors set on shelf.context.Context

        Args:
            context(shelf.context.Context)

        Returns:
            flask Response
    """
    if ErrorCode.INVALID_SEARCH_CRITERIA in context.errors:
        return create_400(ErrorCode.INVALID_SEARCH_CRITERIA, context.errors[ErrorCode.INVALID_SEARCH_CRITERIA])
    elif ErrorCode.INVALID_ARTIFACT_NAME in context.errors:
        return create_403(
            ErrorCode.INVALID_ARTIFACT_NAME,
            "Artifact and directories names that BEGIN "
            "with an underscore are reserved as private and cannot be accessed or created. This of "
            "course exludes _search and _meta which are not part of the artifact path itself."
        )
    elif ErrorCode.INVALID_REQUEST_DATA_FORMAT in context.errors:
        return create_400(
            ErrorCode.INVALID_REQUEST_DATA_FORMAT,
            msg="Data sent with request must be in JSON format and also be either an array or an object."
        )


def map_metadata_result_errors(result):
    if result.has_error(MetadataErrorCode.IMMUTABLE):
        return create_403(ErrorCode.FORBIDDEN, "Cannot update immutable metadata.")
    elif result.has_error(MetadataErrorCode.DUPLICATE):
        return create_403(ErrorCode.FORBIDDEN, "This metadata already exists.")
