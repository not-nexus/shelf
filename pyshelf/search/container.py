from pyshelf.search.update_manager import UpdateManager
from pyshelf.search.manager import Manager
from pyshelf.search import utils


class Container(object):
    def __init__(self, logger, elastic_config):
        self.config = elastic_config
        self.logger = logger
        self._update_manager = None
        self._manager = None
        self._elastic_wrapper = utils.configure_es_connection(self.config["connectionString"],
                self.config.get("accessKey"), self.config.get("secretKey"), self.config.get("region"))

    @property
    def update_manager(self):
        if not self._update_manager:
            self._update_manager = UpdateManager(self.logger, self._elastic_wrapper)

        return self._update_manager

    @property
    def manager(self):
        if not self._manager:
            self._manager = Manager(self)

        return self._manager

    @property
    def elastic_wrapper(self):
        return self._elastic_wrapper
