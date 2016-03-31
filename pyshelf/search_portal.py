from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


class SearchPortal(object):
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.search_manager
        self.search_parser = self.container.search_parser

    def search(self, criteria):
        """
            Using pyshelf.search_parser.SearchParser the portal parses the search and sort criteria
            into the proper format for pyshelf.search.manager.Manager to consume.

            Args:
                criteria(dict): Search and sort criteria formatted as show below.

            Format of criteria:
                {
                    "search": [
                        "version~=1.1"
                    ],
                    "sort": [
                        "version, VERSION, ASC",
                        "bob,DESC"
                    ],
                    "limit": 1
                }

                Or if there is only a single sort/search

                {
                    "search": "version~=1.1",
                    "sort": "version, VERSION, ASC",
                    "limit": 1
                }
        """
        formatted_criteria = self.search_parser.from_request(criteria)
        results = self.search_manager.search(formatted_criteria)
        limit = criteria.get("limit")

        if limit:
            results = results[:limit]

        return results
