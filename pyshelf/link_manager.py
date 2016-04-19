import pyshelf.artifact_key_filter as filters


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
        self.path_converter = self.container.path_converter

    def assign_listing(self, path_list):
        """
            Builds list of links and assigns it to pyshelf.context.Context.link_list

            Args:
                path_list(List(string)): List of cloud paths.
        """
        artifact_path_list = filters.all_private(path_list)
        for artifact_path in artifact_path_list:

            resource_path = self.path_converter.from_cloud(artifact_path)

            rel_type = "item"
            title = "artifact"
            if resource_path[-1] == "/":
                rel_type = "collection"
                title = "a collection of artifacts"

            if resource_path == self.request.path:
                rel_type = "self"

            self._add_link(resource_path, rel_type, title)

    def _add_link(self, path, rel_type, title):

            self.context.add_link({
                "path": path,
                "type": rel_type,
                "title": title
            })

    def assign_single(self, artifact_path):
        """
            Assigns individual link to pyshelf.context.Context.link_list.

            Args:
                artifact_path(string)
        """
        identity = self.container.resource_identity_factory \
            .from_cloud_identifier(artifact_path)

        artifact_rel_type = "related"
        metadata_rel_type = "related"

        if identity.resource_url == self.request.path:
            artifact_rel_type = "self"
        else:
            metadata_rel_type = "self"

        link_list = [
            {
                "path": identity.resource_url,
                "type": artifact_rel_type,
                "title": "artifact"
            },
            {
                "path": identity.metadata,
                "type": metadata_rel_type,
                "title": "metadata"
            }
        ]

        self.context.link_list = link_list
