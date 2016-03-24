from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


class SearchPortal(object):
    def __init__(self, search_container):
        self.search_container = search_container
        self.search_manager = SearchManager(self.search_container)

    def search(self, criteria):
        """
            Searches ElasticSearch metadata documents.

            Args:
                criteria(dict): Criteria to use to initiate search.

            Format of criteria:
        """
        results = self.search_manager.search(criteria)
        # Here is where I would use the refactored artifact list manager to store links on context
