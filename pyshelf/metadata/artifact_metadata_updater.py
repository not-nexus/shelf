class ArtifactMetadataUpdater(object):
    def __init__(self, cloud_portal, metadata_initializer, identity):
        """
            Args:
                cloud_portal(pyshelf.metadata.cloud_portal.CloudPortal)
                metadata_initializer(pyshelf.metadata.initializer.Initializer)
                identity(pyshelf.resource_identity.ResourceIdentity)
        """
        self.cloud_portal = cloud_portal
        self.metadata_initializer = metadata_initializer
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
        metadata = self.cloud_portal.load(self.identity.cloud_metadata)

        if self.metadata_initializer.needs_update(metadata):
            metadata = self.metadata_initializer.update(self.identity, metadata)
            self.cloud_portal.update(self.identity.cloud_metadata, metadata)

        self._metadata = metadata
