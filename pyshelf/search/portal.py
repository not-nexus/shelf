from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


class Portal(object):
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.manager

    def search(self, criteria):
        """
            Searches ElasticSearch metadata documents.

            Args:
                criteria(dict): Criteria to use to initiate search.
        """
        results = self.search_manager.search(criteria)
        # Here is where I would use the refactored artifact list manager to store links on context
