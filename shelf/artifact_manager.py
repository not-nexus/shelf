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
                shelf.cloud.StreamIterator|None
        """
        content = None
        artifact_list = self.assign_artifact_links(path)

        if not artifact_list:
            with self.container.create_bucket_storage() as storage:
                content = storage.get_artifact(path)

                # For tracking purposes
                content.request_id = self.container.request_id

        return content

    def assign_artifact_links(self, path):
        """
            Assigns links for an artifact or collection or artifacts.

            Args:
                path(string): path or name of artifact.

            Returns:
                List[string]: List of artifacts for collection of artifacts.
        """
        artifact_list = []

        with self.container.create_bucket_storage() as storage:
            if path[-1] != "/":
                directory_path = path + "/"
            else:
                directory_path = path

            artifact_list = storage.get_directory_contents(directory_path, recursive=False)

            if artifact_list:
                self.container.logger.info("Resource {0} is assumed to be a directory.".format(directory_path))
                artifact_path_list = [artifact.name for artifact in artifact_list]
                self.link_manager.assign_listing(artifact_path_list)
            else:
                # Artifact requested is not a directory so we want to
                # make sure it exists before assigning the links or going further.
                # If artifact does not exists an exception will be thrown and mapped
                # to a 404 response.
                storage.artifact_exists(path)
                self.link_manager.assign_single(path)

        return artifact_list

    def upload_artifact(self, path, file_storage):
        """
            Uploads artifact and assigns links to context.

            Args:
                path(string): path or name of artifact.
                file_storage(werkzeug.datastructures.FileStorage): file from request.
        """
        with self.container.create_bucket_storage() as storage:
            storage.upload_artifact(path, file_storage)
            self.container.metadata.manager.write()
            self.link_manager.assign_single(path)
            self.container.hook_manager.notify_artifact_uploaded(self.container.resource_identity)
