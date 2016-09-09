from pyshelf.resource_identity import ResourceIdentity
from urlparse import urlparse
from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch
from tests.metadata.factory import Factory


class Comparator(object):
    def __init__(self, test, es_connection_string, logger):
        self._es_connection_parts = urlparse(es_connection_string)
        self.logger = logger
        self.test = test
        self._es_connection = None
        self._factory = None

    @property
    def factory(self):
        if not self._factory:
            self._factory = Factory(self.logger)

        return self._factory

    @property
    def es_connection(self):
        if not self._es_connection:
            self._es_connection = Elasticsearch(self._es_connection_parts.netloc)

        return self._es_connection

    @property
    def index(self):
        return self._es_connection_parts.path[1:]

    def compare(self, resource_url):
        identity = ResourceIdentity(resource_url)
        cloud_portal = self.factory.create_cloud_portal(identity.bucket_name)
        cloud_metadata = cloud_portal.load(identity.cloud_metadata)
        if not cloud_metadata:
            self.fail("Failed to find metadata in cloud for {0}".format(identity.cloud_metadata))
        # Make extra sure our data will show up
        self.es_connection.indices.refresh(index=self.index)
        metadata = Metadata.get(index=self.index, using=self.es_connection, id=identity.search, ignore=404)
        if not metadata:
            self.test.fail("Failed to find metadata in search for {0}".format(identity.search))

        metadata = self._map_es_metadata(metadata)
        self.test.asserts.json_equals(cloud_metadata, metadata)

    def _map_es_metadata(self, metadata):
        metadata = metadata.to_dict()["property_list"]

        new_metadata = {}
        for metadata_property in metadata:
            new_metadata[metadata_property["name"]] = metadata_property

        return new_metadata
