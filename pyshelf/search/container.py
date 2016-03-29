from elasticsearch_dsl.connections import connections
from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager


class Container(object):
    def __init__(self, config, logger):
        self.logger = logger
        self.config = config
        self._hosts = None
        self._update_manager = None
        self._search_manager = None
        self.default_elastic_connection()

    @property
    def hosts(self):
        if not self._hosts:
            self._hosts = self.config.get("elasticSearchHost")

        return self._hosts

    def default_elastic_connection(self):
        connections.create_connection("default", hosts=self.hosts)

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self)

        return self._search_manager
