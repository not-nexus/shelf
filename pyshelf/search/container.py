from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager
from urlparse import urlparse
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch


class Container(object):
    def __init__(self, logger, elastic_config):
        self.config = elastic_config
        self.logger = logger
        self._update_manager = None
        self._manager = None
        self._es_connection = None
        self._using_aws = None
        self._es_url = ""
        self._es_index = None
        self.configure_es_connection()

    @property
    def es_url(self):
        """
            es_url contains Elasticsearch connection string without the path.
            This includes the scheme, the host, and the port.
        """
        return self._es_url

    @property
    def es_index(self):
        return self._es_index

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self.es_connection, self.es_index)

        return self._update_manager

    @property
    def manager(self):
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def es_connection(self):
        return self._es_connection

    @property
    def using_aws(self):
        return bool(self.config.get("aws"))

    def configure_es_connection(self):
        """
            Configures Elasticsearch connection based on provided config.
        """
        parsed_url = urlparse(self.config.get("connectionString"))

        if parsed_url.scheme:
            self._es_url += parsed_url.scheme + "://"

        self._es_url += parsed_url.netloc
        self._es_index = parsed_url.path[1:]
        auth = None

        if self.using_aws:
            auth = AWS4Auth(
                self.config["accessKey"],
                self.config["secretKey"],
                self.config["region"], "es")

        self._es_connection = Elasticsearch(self._es_url, http_auth=auth)
