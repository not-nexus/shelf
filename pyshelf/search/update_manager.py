from pyshelf.search.metadata import Metadata
from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan, bulk


class UpdateManager(object):
    def __init__(self, logger, url, index):
        self.logger = logger
        self.connection = Elasticsearch(url)
        self.index = index

    def remove_unlisted_documents(self, ex_key_list):
        """
            Removes any documents with keys not enumerated in the ex_key_list.

            Args:
                ex_key_list(list): List of keys that should remain in the Elasticsearch collection.

            Returns:
                Number of documents deleted from Elasticsearch.
        """
        query = ~Q("ids", type=Metadata._doc_type.name, values=ex_key_list)
        query = Search(using=self.connection).index(self.index).query(query).to_dict()
        self.logger.debug("Executing the following query for removing old documents from {0} index: {1}"
                .format(self.index, query))

        operations = (
            {
                "_op_type": "delete",
                "_id": hit["_id"],
                "_index": hit["_index"],
                "_type": hit["_type"],
            } for hit in scan(
                self.connection,
                query=query,
                index=self.index,
                doc_type=Metadata._doc_type.name,
                _source=0,
            )
        )
        return bulk(self.connection, operations, refresh=True)

    def bulk_update(self, data):
        """
            This provides bulk updating functionality. It has the ability to update multiple documents.

            Args:
                data(dict): This contains metadata and the associated document key. Example below:

            Example of data format:
            {
                "key_of_doc": {
                    "artifactPath": {
                        "name": "artifactPath",
                        "value": "/wibble/wobble",
                        "immutable": False
                    },
                    ....
                },
                ....
            }
        """
        for key, val in data.iteritems():
            self.update(key, val)

    def update(self, key, metadata):
        """
            Updates the metadata in the ElasticSearch collection denoted by the supplied unique key.

            Args:
                key(string): Unique key that is associated with the metadata document to update.
                metadata(dict): Updated metadata to store in ElasticSearch.
        """
        self.logger.debug("Attempting update of metadata: {0} in ES".format(key))
        meta_doc = self._get_metadata(key)
        meta_doc.update_all(metadata)
        meta_doc.save(using=self.connection)
        self.logger.debug("Updated metadata document {0} in ES".format(key))

    def update_item(self, key, item):
        """
           Updates metadata item in the ElasticSearch collection.

            Args:
                key(string): Unique key that is associated with the metadata document to update.
                item(dict): Updated metadata to store in ElasticSearch.
        """
        self.logger.debug("Attempting to update metadata {0} in ES".format(key))
        meta_doc = self._get_metadata(key)
        meta_doc.update_item(item)
        meta_doc.save(using=self.connection)
        self.logger.debug("Updated metadata {0} in ES".format(key))

    def _get_metadata(self, key):
        """
            Attempts to get existing metadata and creates one if it does not exist.

            Args:
                key(string): Unique key that represents the unique id of the metadata document.

            Returns:
                pyshelf.search.metadata.Metadata
        """
        meta_doc = Metadata.get(id=key, index=self.index, using=self.connection, ignore=404)

        if not meta_doc:
            meta_doc = Metadata()
            meta_doc.meta.id = key
            meta_doc.meta.index = self.index

        return meta_doc
