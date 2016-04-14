from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager
from pyshelf.search.connection import Connection


class Container(object):
    def __init__(self, logger, elastic_config):
        self.config = elastic_config
        self.logger = logger

        # Services
        self._update_manager = None
        self._manager = None
        self._connection = None

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self.connection)

        return self._update_manager

    @property
    def manager(self):
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def connection(self):
        if not self._connection:
            self._connection = Connection(self.config["connectionString"],
                    self.config.get("accessKey"), self.config.get("secretKey"), self.config.get("region"))

        return self._connection
