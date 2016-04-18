from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.aws_auth import AWSRequestsAuth
from urlparse import urlparse


class Connection(Elasticsearch):
    def __init__(self, connection_string, access_key=None, secret_key=None, region=None):
        self.connection_string = connection_string
        self._es_index = None
        self._es_host = None
        self._es_port = None
        self._parse_url()
        self._init_connection(access_key, secret_key, region)

    @property
    def es_index(self):
        if not self._es_index:
            self._es_index = self._parsed_url.path[1:]

        return self._es_index

    @property
    def es_host(self):
        if not self._es_host:
            self._es_host = self._parsed_url.hostname

        return self._es_host

    @property
    def es_port(self):
        if not self._es_port:
            # If no port is given then Elasticsearch-py defaults it to 9200
            port = self._parsed_url.netloc.rsplit(":", 1)

            if len(port) > 1:
                self._es_port = int(port[1])

        return self._es_port

    def _parse_url(self):
        """
            Parses connection string.
        """
        self._parsed_url = urlparse(self.connection_string)

        if not self._parsed_url.scheme:
            self._parsed_url.scheme = "http"

    def _init_connection(self, access_key=None, secret_key=None, region=None):
        """
            Configures Elasticsearch connection object.
        """
        ssl = False
        auth = None

        if self._parsed_url.scheme == "https":
            ssl = True

        if access_key and secret_key and region:
            auth = AWSRequestsAuth(aws_access_key=access_key,
                       aws_secret_access_key=secret_key,
                       aws_host=self.es_host,
                       aws_region=region,
                       aws_service="es")

        hosts = [{"host": self.es_host, "port": self.es_port}]
        super(Connection, self).__init__(hosts=hosts, http_auth=auth, use_ssl=ssl,
                verify_certs=ssl, connection_class=RequestsHttpConnection)
