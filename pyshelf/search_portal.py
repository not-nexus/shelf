# CODE_REVIEW:  Can we rename this to RequestSearchPortal or add a comment
# to that effect?  This class really is a portal between a request and the
# search layer.  If we were going to use the search layer outside of a
# request context, we would not use this class
#
# Same goes with SearchParser I guess


class SearchPortal(object):
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.search_manager
        self.search_parser = self.container.search_parser
        self.link_manager = self.container.link_manager
        self.resource_id = self.container.resource_identity

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
        formatted_criteria = self.search_parser.from_request(criteria, self.resource_id.resource_path)
        results = self.search_manager.search(formatted_criteria)
        artifact_list = self.search_parser.list_artifacts(results, criteria.get("limit"))
        self.link_manager.assign_listing_path(artifact_list)
