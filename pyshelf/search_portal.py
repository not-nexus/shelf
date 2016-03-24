from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


class SearchPortal(object):
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.search_manager

    def search(self, criteria):
        """
            Searches ElasticSearch metadata documents.

            Args:
                criteria(dict): Criteria to use to initiate search.

            Format of criteria:
        """
        results = self.search_manager.search(criteria)
        # Here is where I would use the refactored artifact list manager to store links on context
