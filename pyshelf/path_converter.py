import os.path
import re


class PathConverter(object):
    """
        It is the responsibility of this class to take a
        particular identifier and turn it into our resource
        path for our API.

        Note: This class will always return the resource_url for a corresponding
        artifact.  This is important to note for metadata since you will not
        get back the resource for the metadata but the resource for the artifact
        that the metadata is associated with.
    """
    def __init__(self, artifact_path_builder):
        """
            Args:
                artifact_path_builder(pyshelf.artifact_path_builder.ArtifactPathBuilder)
        """
        self.artifact_path_builder = artifact_path_builder

    def from_cloud(self, path):
        """
            Creates our resource path for this cloud identifier

            Args:
                path(basestring)

            Returns:
                basestring
        """
        resource_url = self.artifact_path_builder.build(path)
        return resource_url

    def from_cloud_metadata(self, path):
        """
            Converts a cloud metadata path to our resource identifier.

            Args:
                path(basestring)

            Returns:
                basestring
        """

        head, tail = os.path.split(path)
        new_name = re.sub("^_metadata_", "", tail)
        new_name = re.sub(".yaml$", "", new_name)
        artifact_path = os.path.join(head, new_name)
        resource_path = self.from_cloud(artifact_path)
        return resource_path
