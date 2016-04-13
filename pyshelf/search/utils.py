from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth
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

        Args:
            connection_string(string| None)
            access_key(string | None)
            secret_key(string | None)
            region(string | None)

        Returns:
            Tuple(elasticsearch.Elasticsearch, string)
    """
    parsed_url = urlparse(connection_string)

    if not parsed_url.scheme:
        parsed_url.scheme = "https"

    es_url = parsed_url.scheme + "://" + parsed_url.netloc
    es_index = parsed_url.path[1:]
    kwargs = {}

    if access_key and secret_key and region:
        auth = AWSRequestsAuth(aws_access_key=access_key,
                   aws_secret_access_key=secret_key,
                   aws_host=parsed_url.netloc,
                   aws_region=region,
                   aws_service="es")
        use_ssl = True
        if parsed_url.scheme == "http":
            use_ssl = False
        kwargs = {
            "http_auth": auth,
            "use_ssl": use_ssl,
            "connection_class": RequestsHttpConnection
        }

    return (Elasticsearch(es_url, **kwargs), es_index)
