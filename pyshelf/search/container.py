from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager
from urlparse import urlparse


class Container(object):
    def __init__(self, logger, connection_string):
        self.logger = logger
        self._es_index = urlparse(connection_string).path[1:]
        self._connection_string = connection_string.rsplit("/", 1)[0]
        self._update_manager = None
        self._search_manager = None

    @property
    def connection_string(self):
        return self._connection_string

    @property
    def es_index(self):
        return self._es_index

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self.connection_string)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self)

        return self._search_manager
