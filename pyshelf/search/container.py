from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager
from urlparse import urlparse
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch
from pyshelf.search import utils


class Container(object):
    def __init__(self, logger, elastic_config):
        self.config = elastic_config
        self.logger = logger
        self._update_manager = None
        self._manager = None
        self._es_connection, self._es_index = utils.configure_es_connection(self.config["connectionString"],
                self.config.get("accessKey"), self.config.get("secretKey"), self.config.get("region"))

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
