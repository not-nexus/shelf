import yaml


class Manager(object):
    def __init__(self, container):
        self.container = container
        # TODO: Use this line when we have it
        # self.update_manager = self.container.search.update_manager
        self.identity = self.container.resource_identity
        self.mapper = self.container.mapper
        self._metadata = None

    @property
    def metadata(self):
        if not self._metadata:
            self._metadata = self.load()

        return self._metadata

    def load(self):
        with self.container.create_cloud_storage as storage:
            metadata_id = self.identity.cloud_metadata
            raw_meta = storage.get_artifact_as_string(metadata_id)
            meta = yaml.load(raw_meta)

            if not meta:
                meta = {}

        return meta
