from flask import Response
import json
from pyshelf.cloud.stream_iterator import StreamIterator


class ContextResponseMapper(object):
    def __init__(self, link_mapper, context):
        self.link_mapper = link_mapper
        self.context = context

    def to_response(self, body=None, status_code=None):
        response = None
        content_type = self.determine_content_type(body)
        # This looks like stupid logic (and it still may
        # be).  If the body is a stream I need to instantiate
        # the Response with it.  I cannot "set_data" since that
        # is expected to be a string.
        if isinstance(body, StreamIterator):
            response = Response(body)
        else:
            response = Response()

            if body:
                # Serialize body if it is json content type
                if content_type == "application/json":
                    body = json.dumps(body)
                response.set_data(body)

        # Letting flask default it otherwise
        if content_type:
            response.headers["Content-Type"] = content_type

        if status_code:
            response.status_code = status_code

        self.map_links(response)
        return response

    def determine_content_type(self, body):
        content_type = None
        if isinstance(body, dict):
            content_type = "application/json"
        elif isinstance(body, StreamIterator):
            content_type = body.headers["content-type"]

        return content_type

    def map_links(self, response):
        link_list = self.link_mapper.to_response(self.context.link_list)
        for link in link_list:
            response.headers.add("Link", link)
