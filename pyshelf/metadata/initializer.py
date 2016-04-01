from pyshelf.metadata.keys import Keys


class Initializer(object):
    """
        Responsible for dealing with initialization of
        metadata.  It is the single point where we

        1.) Determine what metadata should be initialized
        2.) Determine if metadata needs to be initialized
    """
    def __init__(self, container):
        """
            Args:
                container(pyshelf.metadata.container.Container)
        """
        self.container = container
        self.mapper = self.container.mapper
        self.identity = self.container.resource_identity

    def needs_update(self, metadata):
        """
            Determines if we should reinitialize the provided
            metadata

            Args:
                metadata(schemas/metadata.json)

            Returns:
                boolean
        """
        required = [
            Keys.MD5,
            Keys.PATH,
            Keys.NAME
        ]

        for key in required:
            if key not in metadata:
                return True

        return False

    def update(self, metadata):
        """
            Updates the metadata to have the required keys.
            Note: This does not update it in the cloud.

            Args:
                metadata(schemas/metadata.json)

            Returns:
                metadata(schemas/metadata.json): But updated
        """
        with self.container.create_cloud_storage() as storage:
            etag = storage.get_etag(self.identity.cloud)
            metadata[Keys.MD5] = self.mapper.create_response_property(Keys.MD5, etag, True)

        metadata[Keys.PATH] = self.mapper.create_response_property(Keys.PATH, self.identity.artifact_path, True)
        metadata[Keys.NAME] = self.mapper.create_response_property(Keys.NAME, self.identity.artifact_name, True)

        return metadata
