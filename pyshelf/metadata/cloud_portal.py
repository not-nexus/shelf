import copy


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
        # So that we don't get unintended side effects
        contents = copy.deepcopy(metadata)
        contents = self.codec.serialize(contents)
        contents = self.mapper.to_cloud(contents)
        with self.container.create_bucket_storage() as storage:
            storage.set_artifact_from_string(cloud_identifier, contents)

    def load(self, cloud_identifier):
        """
            Loads metadata from the cloud.

            Returns
                dict
        """
        with self.container.create_cloud_storage() as storage:
            raw_meta = storage.get_artifact_as_string(cloud_identifier)
            meta = self.codec.deserialize(raw_meta)

            if not meta:
                meta = {}

            meta = self.mapper.to_response(meta)

        return meta
