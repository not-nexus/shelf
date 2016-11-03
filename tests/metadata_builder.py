from shelf.metadata.keys import Keys
from copy import deepcopy
from shelf.resource_identity import ResourceIdentity
from shelf.metadata.mapper import Mapper


class MetadataBuilder(object):
    DEFAULT = {
        Keys.MD5: {
            "immutable": True,
            "name": Keys.MD5,
            "value": Keys.MD5,
        },
        Keys.PATH: {
            "immutable": True,
            "name": Keys.PATH,
            "value": Keys.PATH,
        },
        Keys.NAME: {
            "immutable": True,
            "name": Keys.NAME,
            "value": Keys.NAME,
        },
    }

    def __init__(self, data=None):
        if not data:
            data = MetadataBuilder.DEFAULT

        self.data = deepcopy(data)
        self._identity = None

    @property
    def identity(self):
        if not self._identity:
            raise AttributeError("identity was not assigned on this MetadataBuilder.  Have you called resource_url()?")

        return self._identity

    @property
    def mapper(self):
        if not self._mapper:
            self._mapper = Mapper()

        return self._mapper

    def property(self, key, value, immutable=False):
        """
            Upserts a metadata value
        """
        self.data[key] = {
            "immutable": immutable,
            "name": key,
            "value": value
        }
        return self

    def version(self, value="1"):
        return self.property("version", value)

    def resource_url(self, resource_url):
        identity = ResourceIdentity(resource_url)
        self._identity = identity
        self.data[Keys.PATH]["value"] = identity.resource_path
        self.data[Keys.NAME]["value"] = identity.artifact_name
        return self

    def to_cloud(self):
        return self.mapper.to_cloud(self.data)

    def copy(self):
        builder = deepcopy(self)
        return builder
