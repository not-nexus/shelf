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
                response = Response()
                response.headers["Link"] = self._format_link_list(list(child_list), path)
                response.status_code = 204

            else:
                stream = storage.get_artifact(path)
                response = Response(stream)
                response.headers["Link"] = self._format_link(stream.key)
                response.headers["Content-Type"] = stream.headers["content-type"]

        return response

    def _format_link(self, artifact, child=False):
        title = artifact.name
        url = "/artifact/" + title
        rel = "self"
        if child:
            rel = "child"
        return "{0}; rel={1}; title={2}".format(url, rel, title)

    def _format_link_list(self, artifact_list, parent_path):
        link_list = []
        for artifact in artifact_list:
            child = parent_path != artifact.name
            link_list.append(self._format_link(artifact, child))

        return ", ".join(link_list)
