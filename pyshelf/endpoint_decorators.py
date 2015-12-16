import functools
import flask
import json
import utils

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

    def logtraffic(self, func):
        """
            Requires injectcontainer to be used first.  Will log the request
            and response of the endpoint this is applied to.

            This decorator assumes that a flask.Response object is returned
            from the route
        """
        @functools.wraps(func)
        def wrapper(container, *args, **kwargs):
            request = container.request
            request_data = request.get_data()

            def log(message, data):
                container.logger.info("%s : \n %s" % (message, data))

            # To pretty print the request
            # TODO : Is this worth it?
            if request_data:
                request_data = json.dumps(json.loads(request_data), indent=4, separators=(',', ': '))
            log("REQUEST HEADERS", request.headers)
            log("REQUEST BODY", request_data)
            response = func(container, *args, **kwargs)
            response_data = response.get_data()
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
            result = func(container, *args, **kwargs)
            return result

        return wrapper

decorators = EndpointDecorators()
