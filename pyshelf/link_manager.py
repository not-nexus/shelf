class LinkManager(object):
    def __init__(self, container):
        self.container = container
        self.bucket_name = self.container.bucket_name
        self.context = self.container.context
        self.request = self.container.request
        self.path_builder = self.container.artifact_path_builder

    def assign_listing(self, artifact_list):
        link_list = []
        for artifact in artifact_list:
            rel_type = "child"
            if self.path_builder.build(artifact.name) == self.request.path:
                rel_type = "self"

            link_list.append({
                "path": artifact.name,
                "type": rel_type
            })

        self.context.link_list = link_list

    def assign_single(self, artifact):
        link_list = [
            {
                "path": artifact.key.name,
                "type": "self"
            },
            {
                "path": artifact.key.name + "/_meta",
                "type": "metadata",
                "title": "metadata"
            }
        ]

        self.context.link_list = link_list
