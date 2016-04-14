from pyshelf.metadata.keys import Keys as MetadataKeys
from pyshelf.resource_identity import ResourceIdentity
from pyshelf.search import utils
from pyshelf.error_code import ErrorCode
from jsonschema import ValidationError


class SearchPortal(object):
    """
        This class is the link between the request/view and the search layer.
    """
    def __init__(self, container):
        self.container = container
        self.search_manager = self.container.search.manager
        self.search_parser = self.container.search_parser
        self.link_manager = self.container.link_manager
        self.resource_id = self.container.resource_identity
        self.schema_validator = self.container.schema_validator

    def search(self, criteria):
        """
            Searches based on criteria defined in request and assigns links to response
            for each search hit.

            Args:
                criteria(schemas/search-request-criteria.json): Search and sort criteria formatted as show below.
        """
        try:
            self.schema_validator.validate("schemas/search-request-criteria.json", criteria)
        except ValidationError as e:
            msg = self.schema_validator.format_error(e)
            self.container.context.add_error(ErrorCode.INVALID_SEARCH_CRITERIA, msg)
            return

        search_path = "{0}={1}*".format(MetadataKeys.PATH, self.resource_id.resource_path)
        criteria["search"] = utils.default_to_list(criteria.get("search"))
        criteria["sort"] = utils.default_to_list(criteria.get("sort"))
        criteria["search"].append(search_path)

        formatted_criteria = self.search_parser.from_request(criteria)
        results = self.search_manager.search(formatted_criteria)
        artifact_list = self._list_artifacts(results, criteria.get("limit"))
        self.link_manager.assign_listing(artifact_list)

    def _list_artifacts(self, results, limit=None):
        """
            Creates a list of paths from the search results.

            Args:
                results(List[dict]): Formatted search results.
                limit(int | None): limit number of records

            Returns:
                list: Each element represents the path to an artifact.
        """
        artifact_list = []

        if limit:
            results = results[:limit]

        for result in results:
            resource_id = ResourceIdentity(result[MetadataKeys.PATH]["value"])
            artifact_list.append(resource_id.cloud[1:])

        return artifact_list
