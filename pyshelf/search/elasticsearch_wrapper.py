from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth
from urlparse import urlparse


class ElasticsearchWrapper(object):
    def __init__(self, connection_string, access_key=None, secret_key=None, region=None):
        self.connection_string = connection_string
        self._index = None
        self._es_url = None
        self._connection = None
        self._parse_url()
        self._init_connection(access_key, secret_key, region)

    @property
    def index(self):
        if not self._index:
            self._index = self._parsed_url.path[1:]

        return self._index

    @property
    def es_url(self):
        if not self._es_url:
            self._es_url = self._parsed_url.scheme + "://" + self._parsed_url.netloc

        return self._es_url

    @property
    def connection(self):
        return self._connection

    def _parse_url(self):
        """
            Parses connection string.
        """
        self._parsed_url = urlparse(self.connection_string)

        if not self._parsed_url.scheme:
            self._parsed_url.scheme = "https"

    def _init_connection(self, access_key=None, secret_key=None, region=None):
        """
            Configures Elasticsearch connection object.
        """
        use_ssl = True
        kwargs = {}

        if self._parsed_url.scheme == "http":
            use_ssl = False

        if access_key and secret_key and region:
            auth = AWSRequestsAuth(aws_access_key=access_key,
                       aws_secret_access_key=secret_key,
                       aws_host=self._parsed_url.netloc,
                       aws_region=region,
                       aws_service="es")
            kwargs = {
                "http_auth": auth,
                "use_ssl": use_ssl,
                "connection_class": RequestsHttpConnection
            }

        self._connection = Elasticsearch(self.es_url, **kwargs)
