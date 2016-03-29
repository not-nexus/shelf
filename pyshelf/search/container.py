from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager
from elasticsearch import Elasticsearch


class Container(object):
    def __init__(self, logger, elastic_search_host):
        self.logger = logger
        self.elastic_search_host = elastic_search_host
        self._elastic_search = None
        self._hosts = None
        self._update_manager = None
        self._search_manager = None

    @property
    def elastic_search(self):
        if not self._elastic_search:
            self._elastic_search = Elasticsearch(self.elastic_search_host)

        return self._elastic_search

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self.elastic_search)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self)

        return self._search_manager
