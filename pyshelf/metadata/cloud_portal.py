import copy
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError


class CloudPortal(object):
    def __init__(self, container):
        """
            Args:
                container(pyshelf.metadata.container.Container)
        """
        self.codec = container.yaml_codec
        self.mapper = container.mapper
        self.container = container

    def update(self, cloud_identifier, metadata):
        """
            Updates the metadata in the cloud which is the
            source of truth.

            Args:
                cloud_identifier(basestring): Something that can
                    identify the file in the cloud.  Right now that
                    will be a path to the file in S3 that stores the
                    metadata
                metadata(schemas/metadata.json)
        """
        # So that we don't get unintended side effects
        contents = copy.deepcopy(metadata)
        contents = dict(contents)
        contents = self.mapper.to_cloud(contents)
        contents = self.codec.serialize(contents)
        with self.container.create_cloud_storage() as storage:
            storage.set_artifact_from_string(cloud_identifier, contents)

    def load(self, cloud_identifier):
        """
            Loads metadata from the cloud.

            Returns
                dict
        """
        with self.container.create_cloud_storage() as storage:
            meta = None

            try:
                raw_meta = storage.get_artifact_as_string(cloud_identifier)
                meta = self.codec.deserialize(raw_meta)
            except ArtifactNotFoundError:
                pass

            # I don't do this inside the except because
            # if an empty string is returned as the metadata
            # then it will deserialize to None instead of
            # an empty dict.
            if not meta:
                meta = {}

            meta = self.mapper.to_response(meta)

        return meta
