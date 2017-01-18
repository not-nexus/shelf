from shelf.search.sort_type import SortType
from shelf.search.sort_flag import SortFlag
from shelf.search.type import Type as SearchType
import re


class SearchParser(object):
    def from_request(self, request_criteria):
        """
            Turns the given request into search criteria that can be consumed by shelf.search module.

            Args:
                request_criteria(schemas/search-request-criteria.json): Criteria from request.

            Returns:
                schemas/search-layer-criteria.json: search and sort criteria that will be consumed by search layer
        """
        search_criteria = []
        sort_criteria = []

        for search in request_criteria["search"]:
            search_criteria.append(self._format_search_criteria(search))

        for sort in request_criteria["sort"]:
            sort_criteria.append(self._format_sort_criteria(sort))

        formatted_criteria = {"search": search_criteria, "sort": sort_criteria}

        return formatted_criteria

    def _format_search_criteria(self, search_string):
        """
            Formats search criteria from search string

            Args:
                search_string(string): Search string from request, ex: "version~=1.1"

            Returns:
                schemas/search-criteria.json: search criteria dictionary
        """
        search_criteria = {}
        # Regex's match unless characters is preceded with \
        version_search = r"(?<!\\)\~="
        wildcard_search = r"(?<!\\)\*"
        equality_search = r"(?<!\\)\="
        split_char = equality_search

        # Search the search_string for potential tilde and does a negative lookbehind for \
        # If tilde exists and \ does precede it, it is a match and thus a version search
        if re.search(version_search, search_string):
            search_criteria["search_type"] = SearchType.VERSION
            split_char = version_search
        else:

            if re.search(wildcard_search, search_string):
                search_criteria["search_type"] = SearchType.WILDCARD
            else:
                search_criteria["search_type"] = SearchType.MATCH

        # Splits using re.split to ensure first occurrence of non-escaped = or ~= is split on
        search_criteria["field"], search_criteria["value"] = re.split(split_char, search_string, 1)

        # Grab the index of the end of the artifact path.
        index = len(search_criteria["value"]) - 1

        # If the search time is a version search, we need to decrement the
        # index, as version searches end with two characters.
        if search_criteria["search_type"] == SearchType.VERSION:
            index = index - 1

        # Add a "/" to the end of the given artifact path (but before).
        # This makes sure that if you're searching a directory, the search
        # won't also match an artifact with the same name as the directory.
        search_criteria["value"] = search_criteria["value"][:index] + "/" + search_criteria["value"][index:]

        return search_criteria

    def _format_sort_criteria(self, sort_string):
        """
            Formats sort criteria from sort string

            Args:
                sort_string(string): Sort string from request, ex: "version, VERSION, ASC"

            Returns:
                schemas/sort-criteria.json: sort criteria dictionary
        """
        sort_criteria = {}
        flag_list = []
        sort_list = sort_string.split(",")
        # The field is always first in the sort string.
        sort_criteria["field"] = sort_list.pop(0).strip()

        for sort_string in sort_list:
            sort_string = sort_string.strip()
            sort_type = SortType.get_alias(sort_string)
            sort_flag = SortFlag.get_alias(sort_string)

            # Only one shelf.search.sort_type.SortType can be used at once.
            # We decided grabbing the last one makes the most sense if there are multiple.
            if sort_type:
                sort_criteria["sort_type"] = sort_type
            elif sort_flag:
                flag_list.append(sort_flag)

        if flag_list:
            sort_criteria["flag_list"] = flag_list

        if not sort_criteria.get("sort_type"):
            sort_criteria["sort_type"] = SortType.ASC

        return sort_criteria
