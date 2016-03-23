from mock import Mock
from pyshelf.search.container import Container as SearchContainer


class SearchTestWrapper(object):
    def __init__(self):
        self.config = {
            "elasticSearchHost": ["localhost:9200"],
            "test": {
                "accessKey": "test",
                "secretKey": "test",
            }
        }
        self.logger = Mock()
        self._search_container = None

    @property
    def search_container(self):
        if not self._search_container:
            self._search_container = SearchContainer(self.logger, self.config)

        return self._search_container
