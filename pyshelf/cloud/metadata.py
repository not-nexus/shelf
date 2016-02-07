from pyshelf.cloud.cloud_exceptions import MetadataNotFoundError


class Metadata(object):
    def __init__(self, container, artifact):
        self.container = container
        self.artifact = artifact
        self.storage = self._load(self.artifact)

    def _load(self, artifact):
        pass

    def __getattr__(self, key):
        if key not in self.storage.keys():
            raise MetadataNotFoundError(key)

        return self.storage[key]
