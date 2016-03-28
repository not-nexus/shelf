from pyshelf.metadata.keys import Keys


class Initializer(object):
    def __init__(self, container):
        self.container = container
        self.mapper = self.container.mapper
        self.identity = self.container.resource_identity

    def needs_update(self, metadata):
        required = [
            Keys.MD5,
            Keys.PATH,
            Keys.NAME
        ]

        for key in required:
            if key not in metadata:
                return True

        return False

    def update(self, metadata):
        with self.container.create_storage() as storage:
            etag = storage.get_etag(self.identity.cloud_identity)
            metadata[Keys.MD5] = self.mapper.create_response_item(Keys.MD5, etag, True)

        metadata[self.PATH] = self.mapper.create_response_item(Keys.PATH, self.identity.path, True)
        metadata[Keys.NAME] = self.mapper.create_response_item(Keys.NAME, self.identity.name, True)

        return metadata
