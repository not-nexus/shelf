from pyshelf.cloud.stream_iterator import StreamIterator
import os
from flask import Response


class ArtifactListManager(object):
    def __init__(self, container):
        self.container = container

    def get_artifact(self, path):
        """
            Gets artifact or artifact list information.

            Args:
                path(string): path or name of artifact.

            Returns:
                flask.Response
        """
        with self.container.create_master_bucket_storage() as storage:
            if os.path.isdir(path):
                child_list = storage.get_directory_contents(path)
                links = []
                for child in child_list:
                    links.append(self._format_link(str(child)))
                response = Response()
                response.headers["Link"] = links
                response.status_code = 204

            else:
                stream = storage.get_artifact(path)
                response = Response(stream)
                response.headers["Content-Type"] = stream.headers["content-type"]

        return response

    # Currently not used. Will be when I know the link format.
    def _format_link(self, path):
        form = "<{path}>; rel={ref}; title={title},"
        return link
