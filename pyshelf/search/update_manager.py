from pyshelf.search.metadata import Metadata
from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from elasticsearch.helpers import scan, bulk
from pyshelf.search.type import Type as SearchType
from pyshelf.metadata.keys import Keys as MetadataKeys


class UpdateManager(object):
    def __init__(self, logger, es_connection, index):
        self.logger = logger
        self.connection = es_connection
        self.index = index

    def remove_unlisted_documents(self, ex_key_list):
        """
            Removes any documents with keys not enumerated in the ex_key_list.

            Args:
                ex_key_list(list): List of keys that should remain in the Elasticsearch collection.

            Returns:
                int: Number of documents deleted from Elasticsearch.
        """
        # Using an invert operator here to create a bool query with a "must not occurence type" with an ids query.
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-bool-query.html
        query = ~Q("ids", type=Metadata._doc_type.name, values=ex_key_list)
        query = Search(using=self.connection).index(self.index).query(query).to_dict()

        return self._bulk_delete(query)

    def remove_unlisted_documents_per_bucket(self, ex_key_list, bucket_name):
        """
            Removes any documents with keys not enumerated in the ex_key_list associated with the supplied bucket.

            Args:
                ex_key_list(list): List of keys that should remain in the Elasticsearch collection.
                bucket_name(string): Used to filter document so only old documents in this bucket are pruned.

            Returns:
                int: Number of documents deleted from Elasticsearch.
        """
        # Formats bucket name for artifactPath wildcard search
        bucket_url = "/{0}/*".format(bucket_name)
        query = ~Q("ids", type=Metadata._doc_type.name, values=ex_key_list)

        # Query for docs in particular bucket which requires us to match artifactPath.
        nested_query = Q(SearchType.MATCH, property_list__name=MetadataKeys.PATH)
        nested_query &= Q(SearchType.WILDCARD, property_list__value=bucket_url)
        query &= Q("nested", path="property_list", query=nested_query)
        query = Search(using=self.connection).index(self.index).query(query).to_dict()

        return self._bulk_delete(query)

    def _bulk_delete(self, query):
        """
            Deletes all results returned by provided query.

            Args:
                query(dict): dictionary representing Elasticsearch query.

            Returns:
                int: number of documents deleted from Elasticsearch.
        """
        self.logger.debug("Executing the following query for removing old documents from {0} index: {1}"
                .format(self.index, query))

        # Doing a bulk operation here via the elasticsearch library.
        # With elasticsearch_dsl there is no way to do a bulk delete.
        # scan is a simple way to iterate through all results and delete each one
        # http://elasticsearch-py.readthedocs.org/en/master/helpers.html#scan
        # In summation we do a query for all ids not in the ex_key_list and iterate through and delete all results.
        # Based on my research this was the easiest way to perform this operation.
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
        stats = bulk(self.connection, operations, refresh=True)
        return stats[0]

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
