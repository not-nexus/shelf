from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.type import Type as SearchType
import re
from pyshelf.metadata.keys import Keys as MetadataKeys
from pyshelf.resource_identity import ResourceIdentity


class SearchParser(object):
    def from_request(self, request_criteria, path):
        """
            Turns the given request into search criteria that can be consumed by pyshelf.search module.

            Args:
                request_criteria(dict): Search and sort criteria from the request.
                path(string): Path to search.

            Returns:
                dict: search and sort criteria that will be consumed by search layer
        """
        search_criteria = []
        sort_criteria = []

        # CODE_REVIEW: Instead of doing this if else thing can you make a
        # function to default to a list and then always treat the result
        # as a list?
        if isinstance(request_criteria["search"], list):
            for search in request_criteria["search"]:
                search_criteria.append(self._format_search_criteria(search))
        else:
            search_criteria.append(self._format_search_criteria(request_criteria["search"]))

        # CODE_REVIEW: I'm thinking this is outside the scope of the
        # SearchParser.  The SearchParser should somewhat stupidly
        # just parse what it is handed.  What if we had another source
        # that wouldn't have a path?  I think these types of rules are
        # better added to a manager whose responsibility is specific to
        # a request to an API.
        path_search = "{0}={1}*".format(MetadataKeys.PATH, path)
        search_criteria.append(self._format_search_criteria(path_search))

        # CODE_REVIEW: Should add this type of functionality to the
        # list defaulting function.
        if request_criteria.get("sort"):

            # CODE_REVIEW: Again, defaulting list thing.
            if isinstance(request_criteria["sort"], list):
                for sort in request_criteria["sort"]:
                    sort_criteria.append(self._format_sort_criteria(sort))
            else:
                sort_criteria.append(self._format_sort_criteria(request_criteria["sort"]))

        formatted_criteria = {"search": search_criteria, "sort": sort_criteria}

        return formatted_criteria

    # CODE_REVIEW: This should be moved elsewhere.  It doesn't parse
    # a the search request data structure.  I think the SearchPortal
    # could do this instead, or a separate class used by the SearchPortal
    def list_artifacts(self, results, limit=None):
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

    def _format_search_criteria(self, search_string):
        """
            Formats search criteria from search string

            Args:
                search_string(string): Search string from request, ex: "version~=1.1"

            Returns:
                dict: search criteria dictionary
        """
        search_criteria = {}
        # CODE_REVIEW: Can we escapse "~" as well?
        version_search = "\~\="
        # Match star unless it is escaped with \
        wildcard_search = r"[^\\]\*"
        split_char = "="

        # CODE_REVIEW: I think we may want to do this
        # slightly different.  Right now we define a
        # "split_char" and it will be "=" unless it can
        # find ~= anywhere in the string.  Instead I think
        # it should be the first occurance of "=" that defines
        # what the search.  In other words...
        #
        # lol=blah~=blah
        #
        # Ends up being "lol": "blah~=blah" instead of
        # "lol=blah": "blah".
        if re.search(version_search, search_string):
            search_criteria["search_type"] = SearchType.VERSION
            split_char = "~="
        else:

            if re.search(wildcard_search, search_string):
                search_criteria["search_type"] = SearchType.WILDCARD
            else:
                search_criteria["search_type"] = SearchType.MATCH

        # CODE_REVIEW: Why not `search_string.split(split_char, 1)` ?
        # Then you wouldn't need to slice the returned tuple.
        #
        # This may change based on previous code review comments anyways.
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
            # CODE_REVIEW: Can we make VER and alias for VERSION?
            elif hasattr(SortFlag, string):
                flag_list.append(string)
            else:
                # CODE_REVIEW: Can we instead enforce the first value
                # to be the field?  In this way I wouldn't be able to
                # search a field called "VERSION"
                sort_criteria["field"] = string

        if flag_list:
            sort_criteria["flag_list"] = flag_list

        if not sort_criteria.get("sort_type"):
            sort_criteria["sort_type"] = SortType.ASC

        return sort_criteria
