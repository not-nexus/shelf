from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager as SearchManager
from urlparse import urlparse


class Container(object):
    def __init__(self, logger, connection_string):
        self.logger = logger
        parsed_url = urlparse(connection_string)
        self._es_url = parsed_url.scheme + "://" + parsed_url.netloc
        self._es_index = parsed_url.path[1:]
        self._update_manager = None
        self._search_manager = None

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
            self._update_manager = UpdateManager(self.logger, self.es_url, self.es_index)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = SearchManager(self)

        return self._search_manager
