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
            if path[-1] != "/":
                directory_path = path + "/"
            else:
                directory_path = path

            artifact_list = storage.get_directory_contents(directory_path, recursive=False)
            if len(artifact_list) > 0:
                self.container.logger.debug("Resource {0} is assumed to be a directory.".format(directory_path))
                link_list = []
                for artifact in artifact_list:
                    rel_type = "child"
                    if artifact.name == path:
                        rel_type = "self"

                    link_list.append({
                        "path": artifact.name,
                        "type": rel_type
                    })
                response = Response()
                link_list = self.container.link_mapper.to_response(link_list)
                for link in link_list:
                    response.headers.add("Link", link)
                response.status_code = 204
            else:
                stream = storage.get_artifact(path)
                response = Response(stream)
                link_list = [
                    {
                        "path": stream.key.name,
                        "type": "self"
                    },
                    {
                        "path": path + "/_meta",
                        "type": "metadata",
                        "title": "metadata"
                    }

                ]
                link_list = self.container.link_mapper.to_response(link_list)
                for link in link_list:
                    response.headers.add("Link", link)
                response.headers["Content-Type"] = stream.headers["content-type"]

        return response
