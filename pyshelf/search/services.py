from pyshelf.search.manager import Manager
from pyshelf.search.portal import Portal
from pyshelf.search.update_manager import UpdateManager


class Services(object):
    def __init__(self, container):
        self.container = container
        self._manager = None
        self._portal = None
        self._update_manager = None

    @property
    def manager(self):
        if not self._manager:
            self._manager = Manager(self.container)

        return self._manager

    @property
    def portal(self):
        if not self._portal:
            self._portal = Portal(self.container)

        return self._portal

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager()

        return self._update_manager
