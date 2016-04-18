class ArtifactListManager(object):
    def __init__(self, container):
        self.container = container
        self.link_manager = self.container.link_manager

    def get_artifact(self, path):
        """
            Gets artifact or artifact list information.

            Args:
                path(string): path or name of artifact.

            Returns:
                pyshelf.cloud.StreamIterator|None
        """
        content = None
        with self.container.create_bucket_storage() as storage:
            if path[-1] != "/":
                directory_path = path + "/"
            else:
                directory_path = path

            artifact_list = storage.get_directory_contents(directory_path, recursive=False)
            if len(artifact_list) > 0:
                self.container.logger.debug("Resource {0} is assumed to be a directory.".format(directory_path))
                artifact_path_list = [artifact.name for artifact in artifact_list]
                self.link_manager.assign_listing(artifact_path_list)
            else:
                content = storage.get_artifact(path)
                self.link_manager.assign_single(content.key.name)

        return content
