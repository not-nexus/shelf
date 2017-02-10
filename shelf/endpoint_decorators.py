import functools
import json
from shelf.error_code import ErrorCode
from shelf.get_container import get_container
import shelf.response_map as response_map
from jsonschema import ValidationError
from fuzzywuzzy import fuzz
from copy import deepcopy

"""
    This module contains decorator functions that are commonly
    used for the endpoints for this api.
"""


class EndpointDecorators(object):
    # Headers that should be redacted with associated fuzzy match ratio.
    # This is to allow expansion to other headers in the future if necessary.
    REDACTED_HEADERS = {
        "authorization": 50
    }

    def merge(self, func, *decorator_list):
        """
            What this does is wraps a list of decorators provided
            manually so that I can combine multiple decorators into
            a single decorator

            For example, normal usage would be like so

            @decorator1
            @decorator2

            Now I can expose a single decorator which will run as if both
            were added

            @merged_decorator
        """
        for decorator in reversed(decorator_list):
            func = decorator(func)
        return func

    def foundation(self, func):
        wrapper = self.merge(
            func,
            self.injectcontainer,
            self.logtraffic,
            self.validate_storage_accessible,
            self.auth
        )

        return wrapper

    def foundation_headers(self, func):
        wrapper = self.merge(
            func,
            self.injectcontainer,
            self.logheaders,
            self.validate_storage_accessible,
            self.auth
        )
        return wrapper

    def logtraffic(self, func):
        """
            Requires injectcontainer to be used first.  Will log the request
            and response of the endpoint this is applied to.

            This decorator assumes that a flask.Response object is returned
            from the route

            this logs the body of the request
        """
        wrapper = self.merge(
            func,
            self.logheaders,
            self.logbodies
        )

        return wrapper

    def logbodies(self, func):
        """
            Used to log the request and response
            bodies.
        """
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            request = container.request
            request_data = request.get_data()

            def log(message, data):
                container.logger.info("{0} : \n {1}".format(message, data))

            if request_data:
                try:
                    request_data = json.dumps(
                        json.loads(
                            request_data
                        ),
                        indent=4,
                        separators=(',', ': ')
                    )
                except ValueError as ex:
                    container.logger.info("Invalid JSON from request.")
                    container.logger.exception(ex)

            log("REQUEST BODY", request_data)
            response = func(container, *args, **kwargs)
            if response.headers["content-type"] == "application/json":
                log("RESPONSE DATA", response.data)
            return response

        return wrapper

    def logheaders(self, func):
        """
            this logs the request headers
        """
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            request = container.request

            def redact_headers(headers):
                """
                    Redacts any items in EndpointDecorators.REDACTED_HEADERS.

                    Args:
                        headers(dict) - Note this is written to handle immutable
                                        dictionary types such as
                                        Werkzueg.DataStructures.EnvironHeaders.
                """
                redacted_headers = []

                # Werkzueg.DataStructures.EnvironHeaders are immutable.
                # Cannot copy and change, so chose to redact and log this way.
                for header_name, value in headers.iteritems():
                    for header_to_redact, ratio in EndpointDecorators.REDACTED_HEADERS.iteritems():
                        # Using partial ratio with a > 50 as a match yieled
                        # the best results. Partial ratio catches stuff like
                        # "auth" where as ratio does not. I decided to use
                        # fuzzywuzzy because the amount of time to do this
                        # check is paltry.
                        if fuzz.partial_ratio(header_name, header_to_redact) > ratio:
                            value = "REDACTED"

                    redacted_headers.append("{0}: {1}".format(header_name, value))

                return redacted_headers

            request_headers = redact_headers(request.headers)
            container.logger.info("{0} : \n{1}".format("REQUEST HEADERS", "\n".join(request_headers)))
            response = func(container, *args, **kwargs)
            response_headers = redact_headers(response.headers)
            to_log = [
                "STATUS CODE: {0}".format(str(response.status_code))
            ]
            to_log = to_log + response_headers
            container.logger.info("{0} : \n{1}".format("RESPONSE HEADERS", "\n".join(to_log)))

            return response

        return wrapper

    def injectcontainer(self, func):
        """
            Used to handle creating and injeceting RequrstContextContainer
            as well as any cleanup required by the container afterwards
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            container = get_container()
            container.bucket_name = kwargs.get("bucket_name")

            result = func(container, *args, **kwargs)
            return result

        return wrapper

    def validate_storage_accessible(self, func):
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            with container.create_silent_bucket_storage() as storage:
                if not storage.is_accessible():
                    return response_map.create_500()

            return func(container, *args, **kwargs)

        return wrapper

    def auth(self, func):
        """
            Attempts to authenticate the request and make sure the user has
            the proper permissions for the request that is attempted.
        """
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            if not container.permissions_validator.allowed():
                response = None
                if container.context.has_error():
                    response = response_map.map_context_error(container.context)
                else:
                    response = response_map.create_401()

                return response

            return func(container, *args, **kwargs)

        return wrapper

    def decode_request(self, container, default_request_body=None):
        """
            Decodes data from flask request.
            Only accepts array or object as valid JSON.

            Args:
                container(shelf.container.Container)
                default_request_body(dict)

            Returns:
                object | None: decoded JSON from request. None if invalid.
        """
        if container.request.data:
            data = container.request.get_json(silent=True, force=True)

            if not isinstance(data, (list, dict)):
                container.context.add_error(ErrorCode.INVALID_REQUEST_DATA_FORMAT)
                data = None
        else:
            # Since Python passes objects by reference, we need to do a
            # deep copy so it won't assign "data" to the
            # reference of "default_request_body".
            data = deepcopy(default_request_body)

        return data

    def validate_request(self, schema_path, default_request_body=None):
        """
            It decodes data as JSON, validates request data against schema,
            and injects that data into the route.

            Args:
                schema_path(string)
                default_request_body(dict) - This argument is used to allow
                                             an empty request body. To use it,
                                             pass an empty dict ({}) to the
                                             decorator.

            Returns:
                function
        """
        def validation_decorator(func):
            @functools.wraps(func)
            def wrapper(container, *args, **kwargs):
                data = self.decode_request(container, default_request_body)

                if container.context.has_error():
                    return response_map.map_context_error(container.context)
                else:
                    try:
                        container.schema_validator.validate(schema_path, data)
                    except ValidationError as e:
                        msg = container.schema_validator.format_error(e)
                        response = response_map.create_400(ErrorCode.INVALID_REQUEST_DATA_FORMAT, msg)

                        return response

                return func(container, data=data, *args, **kwargs)

            return wrapper

        return validation_decorator


decorators = EndpointDecorators()
