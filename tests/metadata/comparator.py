from pyshelf.metadata.yaml_codec import YamlCodec
from pyshelf.metadata.mapper import Mapper
from pyshelf.metadata.cloud_portal import CloudPortal
from pyshelf.resource_identity import ResourceIdentity
from urlparse import urlparse
from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch
from pyshelf.cloud.storage import Storage


class Comparator(object):
    def __init__(self, es_connection_string, logger):
        self._es_connection_parts = urlparse(es_connection_string)
        self.logger = logger
        self._fake_container = None
        self._es_connection = None
        self._cloud_portal = None

    @property
    def fake_container(self):
        if not self._fake_container:
            # Trailing comma in the tuple is important otherwise it is interpretted
            # as a grouping and just returns the type "object"
            self._fake_container = type("FakeMetadataContainer", (object,), {})()
            self._fake_container.yaml_codec = YamlCodec()
            self._fake_container.mapper = Mapper()
            self._fake_container.create_cloud_storage = lambda: Storage(None, None, "test", self.logger)

        return self._fake_container

    @property
    def es_connection(self):
        if not self._es_connection:
            self._es_connection = Elasticsearch(self._es_connection_parts.netloc)

        return self._es_connection

    @property
    def index(self):
        return self._es_connection_parts.path[1:]

    @property
    def cloud_portal(self):
        if not self._cloud_portal:
            self._cloud_portal = CloudPortal(self.fake_container)

        return self._cloud_portal

    def compare(self, resource_url):
        identity = ResourceIdentity(resource_url)
        cloud_metadata = self.cloud_portal.load(identity.cloud_metadata)
        # Make extra sure our data will show up
        self.es_connection.indices.refresh(index=self.index)
        metadata = Metadata.get(index=self.index, using=self.es_connection, id=identity.search, ignore=404)
        metadata = metadata.to_dict()["property_list"]
        # TODO: This obviously will fail.  At the moment I can't get anything to come back from elasticsearch
        import pprint # NOCOMMIT
        pprint.pprint(metadata) # NOCOMMIT
        assert metadata == cloud_metadata
