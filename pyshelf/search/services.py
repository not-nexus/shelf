from pyshelf.search.manager import Manager
from pyshelf.search.container import Container as SearchContainer


class Services(object):
    def __init__(self, logger, config):
        self.search_container = SearchContainer(logger, config)
        self._update_manager = None
        self._search_manager = None

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.search_container)

        return self._update_manager

    @property
    def search_manager(self):
        if not self._search_manager:
            self._search_manager = Manager(self.search_container)

        return self._update_manager
