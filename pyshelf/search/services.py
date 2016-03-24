from pyshelf.search.manager import Manager
from pyshelf.search.container import Container as SearchContainer


class Services(object):
    def __init__(self, logger, config):
        self.search_container = SearchContainer(logger, config)
        self._update_manager = None

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.search_container)

        return self._update_manager
