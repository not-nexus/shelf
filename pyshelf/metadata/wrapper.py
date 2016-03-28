from pyshelf.cloud.cloud_exceptions import ImmutableMetadataError


class Wrapper(dict):
    def is_immutable(self, key):
        item = self.get(key)
        if item and item["immutable"]:
            return True
        else:
            return False

    def ensureMutable(self, key):
        if self.is_immutable(key):
            raise ImmutableMetadataError(key)
