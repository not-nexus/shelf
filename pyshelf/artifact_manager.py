from pyshelf.metadata.artifact_metadata_updater import ArtifactMetadataUpdater


class ArtifactManager(object):
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

    def upload_artifact(self, path, file_storage):
        """
            Uploads artifact and assigns links to context.

            Args:
                path(string): path or name of artifact.
                file_storage(werkzeug.datastructures.FileStorage): file from request.
        """
        with self.container.create_bucket_storage() as storage:
            identity = self.container.resource_identity_factory.from_cloud_identifier(path)
            storage.upload_artifact(path, file_storage)
            updater = ArtifactMetadataUpdater(
                self.container.metadata.bucket_container.cloud_portal,
                self.container.metadata.bucket_container.initializer,
                identity)
            updater.run()
            self.link_manager.assign_single(path)
