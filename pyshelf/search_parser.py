from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.type import Type as SearchType
import re
from pyshelf.metadata.keys import Keys as MetadataKeys


class SearchParser(object):
    def from_request(self, request_criteria):
        """
            Turns the given request into search criteria that can be consumed by pyshelf.search module.

            Args:
                request_criteria(dict): Search and sort criteria from the request.

            Returns:
                dict: search and sort criteria that will be consumed by search layer
        """
        search_criteria = []
        sort_criteria = []

        if isinstance(request_criteria["search"], list):
            for search in request_criteria["search"]:
                search_criteria.append(self._format_search_criteria(search))
        else:
            search_criteria.append(self._format_search_criteria(request_criteria["search"]))

        if isinstance(request_criteria["sort"], list):
            for sort in request_criteria["sort"]:
                sort_criteria.append(self._format_sort_criteria(sort))
        else:
            sort_criteria.append(self._format_sort_criteria(request_criteria["sort"]))

        return {"search": search_criteria, "sort": sort_criteria, "limit": request_criteria.get("limit")}

    def list_artifacts(self, results):
        """
            Creates a list of paths from the search results.

            Args:
                results(List[dict]): Formatted search results.

            Returns:
                list: Each element represents the path to an artifact.
        """
        artifact_list = []

        for result in results:
            artifact_list.append(result[MetadataKeys.PATH])

        return artifact_list

    def _format_search_criteria(self, search_string):
        """
            Formats search criteria from search string

            Args:
                search_string(string): Search string from request, ex: "version~=1.1"

            Returns:
                dict: search criteria dictionary
        """
        search_criteria = {}
        tilde_search = "\~\="
        wildcard_search = "\*\="

        if re.search(tilde_search, search_string):
            search_criteria["search_type"] = SearchType.VERSION
            split_char = "~="
        elif re.search(wildcard_search, search_string):
            search_criteria["search_type"] = SearchType.WILDCARD
            split_char = "*="
        else:
            search_criteria["search_type"] = SearchType.MATCH
            split_char = "="

        search_criteria["field"], search_criteria["value"] = search_string.partition(split_char)[0::2]
        return search_criteria

    def _format_sort_criteria(self, sort_string):
        """
            Formats sort criteria from sort string

            Args:
                sort_string(string): Sort string from request, ex: "version, VERSION, ASC"

            Returns:
                dict: sort criteria dictionary
        """
        sort_criteria = {}
        flag_list = []

        for string in sort_string.split(","):
            string = string.strip()

            if hasattr(SortType, string):
                sort_criteria["sort_type"] = string
            elif hasattr(SortFlag, string):
                flag_list.append(string)
            else:
                sort_criteria["field"] = string

        if flag_list:
            sort_criteria["flag_list"] = flag_list

        return sort_criteria
