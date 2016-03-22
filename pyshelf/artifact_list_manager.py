from flask import Response
import re


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
            if path[-1] != "/":
                directory_path = path + "/"
            else:
                directory_path = path

            artifact_list = storage.get_directory_contents(directory_path, recursive=False)
            if len(artifact_list) > 0:
                self.container.logger.debug("Resource {0} is assumed to be a directory.".format(directory_path))
                artifact_list = self._remove_private_artifacts(list(artifact_list))
                response = Response()
                link_list = self._format_link_list(artifact_list, path)
                for link in link_list:
                    response.headers.add("Link", link)
                response.status_code = 204
            else:
                stream = storage.get_artifact(path)
                response = Response(stream)
                link = self._format_link(stream.key)
                url = "/{0}/artifact/{1}/_meta".format(self.container.bucket_name, path)
                link_list = [link, self._build_link(url, "metadata", "metadata")]
                for link in link_list:
                    response.headers.add("Link", link)
                response.headers["Content-Type"] = stream.headers["content-type"]

        return response

    def _remove_private_artifacts(self, artifact_list):
        refined_list = []
        for artifact in artifact_list:
            match = re.search("^_", artifact.name)
            if not match:
                refined_list.append(artifact)
        return refined_list

    def _format_link(self, artifact, child=False):
        title = artifact.name
        url = "/{0}/artifact/{1}".format(self.container.bucket_name, title)
        rel = "self"
        if child:
            rel = "child"
        return self._build_link(url, rel, title)

    def _build_link(self, url, rel, title):
        return "{0}; rel={1}; title={2}".format(url, rel, title)

    def _format_link_list(self, artifact_list, parent_path):
        link_list = []
        for artifact in artifact_list:
            child = parent_path != artifact.name
            link_list.append(self._format_link(artifact, child))

        return link_list
