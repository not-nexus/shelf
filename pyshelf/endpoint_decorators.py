import functools
import flask
import json
import utils
import pyshelf.response_map as response_map
from pyshelf.cloud.cloud_exceptions import BucketNotFoundError

"""
    This module contains decorator functions that are commonly
    used for the endpoints for this api.
"""


class EndpointDecorators(object):
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
            self.auth
        )

        return wrapper

    def foundation_headers(self, func):
        wrapper = self.merge(
            func,
            self.injectcontainer,
            self.logheaders,
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
                container.logger.info("{} : \n {}".format(message, data))

            if request_data:
                request_data = json.dumps(
                    json.loads(
                        request_data
                    ),
                    indent=4,
                    separators=(',', ': ')
                )

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

            def log(message, data):
                container.logger.info("{} : \n {}".format(message, data))

            log("REQUEST HEADERS", request.headers)
            response = func(container, *args, **kwargs)
            log("RESPONSE HEADERS", response.headers)
            return response

        return wrapper

    def injectcontainer(self, func):
        """
            Used to handle creating and injeceting RequrstContextContainer
            as well as any cleanup required by the container afterwards
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            container = utils.get_container()
            container.bucket_name = kwargs.get("bucket_name")
            result = func(container, *args, **kwargs)
            return result

        return wrapper

    def auth(self, func):
        """
            Attempts to authenticate the request and make sure the user has
            the proper permissions for the request that is attempted.
        """
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            try:
                if not container.permissions_validator.allowed():
                    response = flask.Response()
                    response.set_data("Permission Denied")
                    response.status_code = 401
                    return response
            except BucketNotFoundError as e:
                return response_map.map_exception(e)

            return func(container, *args, **kwargs)

        return wrapper

decorators = EndpointDecorators()
