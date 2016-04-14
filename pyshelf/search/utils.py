from pyshelf.search.elasticsearch_wrapper import ElasticsearchWrapper


def default_to_list(value):
    """
        Encapsulates non-list objects in a list for easy parsing.

        Args:
            value(object): value to be returned as is if it is a list or encapsulated in a list if not.
    """
    if not isinstance(value, list) and value is not None:
        value = [value]
    elif value is None:
        value = []

    return value


def configure_es_connection(connection_string, access_key=None, secret_key=None, region=None):
    """
        Configures Elasticsearch connection. Returns a tuple with Elasticsearch object and Elasticsearch index.

        Args:
            connection_string(string| None)
            access_key(string | None)
            secret_key(string | None)
            region(string | None)

        Returns:
            pyshelf.search.elasticsearch_wrapper.ElastcisearchWrapper
    """
    return ElasticsearchWrapper(connection_string, access_key, secret_key, region)
