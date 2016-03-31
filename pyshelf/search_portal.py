from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


class SearchPortal(object):
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.search_manager
        self.search_parser = self.container.search_parser
        self.link_manager = self.container.link_manager

    def search(self, criteria):
        """
            Searches based on criteria defined in request and assigns links to response
            for each search hit.

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
        artifact_list = self.search_parser.list_artifacts(results, criteria.get("limit"))
        self.link_manager.assign_listing(artifact_list)

    def _limit_results(self, search_results, limit=None):
        """
            Limits the search results to number passed. If limit is None
            all results are returned.

            Args:
                search_results(List[dict]): Search results.
                limit(int | None): Number to limit result set to.

            Returns:
                List[dict]: spliced list of results.
        """
        if limit:
            search_results = search_results[:limit]

        return search_results
