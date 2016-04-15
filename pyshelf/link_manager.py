import os.path


class LinkManager(object):
    def __init__(self, container):
        """
            Args:
                container(pyshelf.container.Container)
        """
        self.container = container
        self.bucket_name = self.container.bucket_name
        self.context = self.container.context
        self.request = self.container.request
        self.path_builder = self.container.artifact_path_builder

    def assign_listing(self, artifact_path_list):
        """
            Builds list of artifact links and assigns it to pyshelf.context.Context.link_list

            Args:
                artifact_path_list(List(string)): List of artifacts paths.
        """
        link_list = []
        for artifact_path in artifact_path_list:
            rel_type = "child"
            if self.path_builder.build(artifact_path) == self.request.path:
                rel_type = "self"

            link_list.append({
                "path": artifact_path,
                "type": rel_type
            })

        self.context.link_list = link_list

    def assign_single(self, artifact):
        """
            Assigns individual link to pyshelf.context.Context.link_list.

            Args:
                artifact(pyshelf.cloud.stream_iterator.StreamIterator): artifact
        """
        link_list = [
            {
                "path": artifact.key.name,
                "type": "self"
            },
            {
                "path": os.path.join(artifact.key.name, "_meta"),
                "type": "metadata",
                "title": "metadata"
            }
        ]

        self.context.link_list = link_list
