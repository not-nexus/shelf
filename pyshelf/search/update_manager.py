from elasticsearch_dsl.connections import connections
from pyshelf.search.metadata import Metadata


class UpdateManager(object):
    def __init__(self, search_container):
        self.search_container = search_container

    def update(self, key, metadata):
        """
            Updates the metadata in the ElasticSearch collection denoted by the supplied unique key.

            Args:
                key(string): Unique key that is associated with the metadata document to update.
                metadata(dict): Updated metadata to store in ElasticSearch.
        """
        self._connect()

        meta_doc = Metadata(key=key)
        meta_doc.update(metadata)

    def update_item(self, key, item_key, item):
        """
           Updates metadata item in the ElasticSearch collection.

            Args:
                key(string): Unique key that is associated with the metadata document to update.
                item_key(string): Key of item to update.
                item(dict): Updated metadata to store in ElasticSearch.
        """
        self._connect()

        meta_doc = Metadata(key=key)
        meta_doc.add_item(item_key, item)

    def _connect(self):
        """ Sets up default and development connections based on application config. """
        connections.configure(
            default={"hosts": self.search_container.config.get("elasticSearchHost")},
            dev={"hosts": self.search_container.config.get("elasticSearchHostDev")}
        )
