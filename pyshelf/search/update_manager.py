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
        self.search_container.logger.debug("Attempting update of metadata: {0} in ES".format(key))
        meta_doc = self.get_metadata(key)
        meta_doc.update_all(metadata)
        meta_doc.save()
        self.search_container.logger.debug("Updated metadata document {0} in ES".format(key))

    def update_item(self, key, item):
        """
           Updates metadata item in the ElasticSearch collection.

            Args:
                key(string): Unique key that is associated with the metadata document to update.
                item(dict): Updated metadata to store in ElasticSearch.
        """
        self.search_container.logger.debug("Attempting to update metadata {0} in ES".format(key))
        meta_doc = self.get_metadata(key)
        meta_doc.update_item(item)
        meta_doc.save()
        self.search_container.logger.debug("Updated metadata {0} in ES".format(key))

    def get_metadata(self, key):
        """
            Attempts to get existing metadata and creates one if it does not exist.

            Args:
                key(string): Unique key that represents the unique id of the metadata document.

            Returns:
                pyshelf.search.metadata.Metadata
        """
        meta_doc = Metadata.get(id=key, ignore=404)

        if not meta_doc:
            meta_doc = Metadata()
            meta_doc.meta.id = key

        return meta_doc
