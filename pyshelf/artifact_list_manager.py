from pyshelf.cloud.stream_iterator import StreamIterator
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
            if path[-1] == "/":
                self.container.logger.debug("Artifact with path {} is a directory.".format(path))
                child_list = storage.get_directory_contents(path)
                links = []
                for child in child_list:
                    title = child.name
                    path = "/artifact/" + title
                    rel = "child"
                    if child.name == path:
                        rel = "self"
                    links.append(self._format_link(path=path, rel=rel, title=title))
                response = Response()
                response.headers["Link"] = ",".join(links)
                response.status_code = 204

            else:
                stream = storage.get_artifact(path)
                response = Response(stream)
                response.headers["Content-Type"] = stream.headers["content-type"]

        return response

    def _format_link(self, **kwargs):
        link = "<{path}>; rel={rel}; title={title}".format(**kwargs)
        return link
