from pyshelf.resource_identity import ResourceIdentity


class ResourceIdentityFactory(object):
    def __init__(self, artifact_path_builder):
        self.artifact_path_builder = artifact_path_builder

    def from_resource_url(self, resource_url):
        """
            Creates a ResourceIdentity from the full
            resource url.  For example:
            /<bucket-name>/artifacts/<path>

            Args:
                resource_url(basestring)

            Returns:
                pyshelf.resource_identity.ResourceIdentity
        """
        identity = ResourceIdentity(resource_url)
        return identity

    def from_cloud_identifier(self, cloud_identifier):
        """
            Creates a ResourceIdentity from the identifier of the
            artifact in the cloud. Just the <path> part of the
            full resource url.

            Args:
                cloud_identifier(basestring)

            Returns:
                pyshelf.resource_identity.ResourceIdentity
        """
        resource_url = self.artifact_path_builder(cloud_identifier)
        identity = self.from_resource_url(resource_url)
        return identity
