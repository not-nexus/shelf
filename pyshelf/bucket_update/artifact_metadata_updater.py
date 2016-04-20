class ArtifactMetadataUpdater(object):
    def __init__(self, container, identity):
        """
            Args:
                container(pyshelf.metadata.bucket_container.BucketContainer)
                identity(pyshelf.resource_identity.ResourceIdentity)
        """
        self.container = container
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
        cloud_portal = self.container.cloud_portal
        initializer = self.container.initializer

        metadata = cloud_portal.load(self.identity.cloud_metadata)

        if initializer.needs_update(metadata):
            metadata = initializer.update(self.identity, metadata)
            cloud_portal.update(self.identity.cloud_metadata, metadata)

        self._metadata = metadata
