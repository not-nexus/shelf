from elasticsearch import Elasticsearch
from requests_aws4auth import AWS4Auth
from urlparse import urlparse


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

        Returns:
            Tuple(elasticsearch.Elasticsearch, string)
    """
    parsed_url = urlparse(connection_string)
    es_url = ""

    if parsed_url.scheme:
        es_url += parsed_url.scheme + "://"

    es_url += parsed_url.netloc
    es_index = parsed_url.path[1:]
    auth = None

    if access_key and secret_key and region:
        auth = AWS4Auth(
            access_key,
            secret_key,
            region, "es")

    return (Elasticsearch(es_url, http_auth=auth), es_index)
