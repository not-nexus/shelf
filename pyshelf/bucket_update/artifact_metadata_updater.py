class ArtifactMetadataUpdater(object):
    def __init__(self, container, identity):
        """
            Args:
                bucket_container(pyshelf.metadata.bucket_container.BucketContainer)
                identity(pyshelf.resource_identity.ResourceIdentity)
        """
        self.container = container
        self.identity = identity
        self._metadata = None

    @property
    def metadata(self):
        return self._metadata

    def run(self):
        portal = self.container.cloud_portal
        initializer = self.container.initializer
        metadata = portal.load(self.identity.cloud_metadata)

        if initializer.needs_update(metadata):
            metadata = initializer.update(self.identity, metadata)
            portal.update(self.identity.cloud_metadata, metadata)

        self._metadata = metadata
