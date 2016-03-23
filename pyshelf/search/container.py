from elasticsearch import Elasticsearch


class Container(object):
    def __init__(self, logger, config):
        self.logger = logger
        self.config = config
        self._hosts = None

    @property
    def hosts(self):
        if not self._hosts:
            self._hosts = self.config.get("elasticSearchHost")

        return self._hosts
