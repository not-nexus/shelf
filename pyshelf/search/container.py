from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections


class Container(object):
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self._hosts = None
        self.default_elastic_connection()

    @property
    def hosts(self):
        if not self._hosts:
            self._hosts = self.config.get("elasticSearchHost")

        return self._hosts

    def default_elastic_connection(self):
        connections.create_connection("default", hosts=self.hosts)
