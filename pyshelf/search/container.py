from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager
from urlparse import urlparse


class Container(object):
    def __init__(self, logger, connection_string):
        self.logger = logger
        self._es_index = urlparse(connection_string).path[1:]
        self._es_host = connection_string.rsplit("/", 1)[0]
        self._update_manager = None
        self._search_manager = None

    @property
    def es_host(self):
        return self._es_host

    @property
    def es_index(self):
        return self._es_index

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self.es_host, self.es_index)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self)

        return self._search_manager
