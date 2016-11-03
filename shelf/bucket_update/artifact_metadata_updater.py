class ArtifactMetadataUpdater(object):
    def __init__(self, bucket_container, identity):
        """
            Args:
                bucket_container(pyshelf.metadata.bucket_container.BucketContainer)
                identity(pyshelf.resource_identity.ResourceIdentity)
        """
        self.bucket_container = bucket_container
        self.identity = identity
        self._metadata = None

    @property
    def metadata(self):
        """
            Returns:
                schemas/metadata.json|None: None if run was not executed.
        """
        return self._metadata

    def run(self):
        """
            Populates the metadata property. It will also ensure that the
            metadata is in a usable state.  In other words, all required
            properties are populated.
        """
        portal = self.bucket_container.cloud_portal
        initializer = self.bucket_container.initializer

        metadata = portal.load(self.identity.cloud_metadata)

        metadata = initializer.update(self.identity, metadata)
        portal.update(self.identity.cloud_metadata, metadata)

        self._metadata = metadata
