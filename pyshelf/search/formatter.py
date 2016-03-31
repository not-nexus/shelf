from distutils.version import LooseVersion
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.type import Type as SearchType


class Formatter(object):
    def __init__(self, criteria, key_list=None):
        """
            Formats search results from Elasticsearch based on the given criteria.

            Args:
                criteria(dict): This contains the search and sort criteria as outlined on
                                pyshelf.search.manager.Manager.search.
                key_list(list): list of keys to include in filtered results if list is not passed
                                all fields will be returned.
        """
        self.search_criteria = criteria.get("search")
        # Sort criteria must be reversed to ensure first sort criteria takes precedence
        self.sort_criteria = reversed(criteria.get("sort", []))
        self.key_list = key_list
        self.version_search = self._get_version_search()

    def get_formatted_results(self, search_results):
        """
            Filters and formats elasticsearch search results.

            Args:
                search_results(List[elasticsearch_dsl.result.Result]): List of search results.

            Returns:
                List[dict]: Formatted results.
        """
        filtered_results = self._filter_metadata(search_results)
        filtered_results = self._filter_metadata_properties(filtered_results)
        return self._sort_results(filtered_results)

    def _get_version_search(self):
        """
            Determines if a version search has been requested and stores the
            field and value if so for future result filtering.
        """
        version_search = {}

        for criteria in self.search_criteria:
            if criteria["search_type"] == SearchType.VERSION:
                version_search[criteria["field"]] = criteria["value"]

        return version_search

    def _is_version_search(self, item_name):
        """
            This ensures the current search is a version search and the
            item name is the field that requires sorting.

            Args:
                item_name: Name of metadata property.

            Returns:
                boolean: Whether current search is a version search and the metadata property
                is to be sorted on.
        """
        return self.version_search.get(item_name) is not None

    def _sufficient_version(self, metadata_property):
        """
            This ensures when a version search is done that any results that are
            less then the version that is passed in are dropped from the result set.

            Args:
                metadata_property: Metadata property that is to be sorted as a version.

            Returns:
                boolean: Whether result version is equal to or greater then the searched version.
        """
        item_version = LooseVersion(metadata_property.value)
        searched_version = LooseVersion(self.version_search[metadata_property.name])

        return searched_version <= item_version

    def _filter_metadata(self, search_results):
        """
            Filters search_results into a consumable format and returns it.

            Args:
                search_results(List[elasticsearch_dsl.result.Result]): List of search results.

            Returns:
                 List[dict]: formatted and filtered results. Each list element represents a search hit and
                            each dictionary within represents a metadata item.
        """
        filtered_list = []

        for metadata in search_results.hits:
            add = True
            filtered = {}

            for metadata_property in metadata.items:
                if self._is_version_search(metadata_property.name):
                    if not self._sufficient_version(metadata_property):
                        add = False
                        break

                filtered[metadata_property.name] = metadata_property

            if add:
                filtered_list.append(filtered)

        return filtered_list

    def _filter_metadata_properties(self, filtered_results):
        """
            Filters metadata properties based on key_list.

            Args:
                filtered_results(List[dict]): List of dicts representing metadata docs.

            Returns:
                List[dict]: Metadata with properties filtered out as defined by key_list.
        """
        if self.key_list:
            for metadata in filtered_results:

                for key in metadata.keys():

                    if key not in self.key_list:
                        metadata.pop(key)

        return filtered_results

    def _sort_results(self, formatted_results):
        """
            Sorts results based on sort criteria.

            Args:
                formatted_results(List[dict]): Result set as formatted by self._filter_metadata.

            Returns:
                List[dict]: sorted results.
        """
        # Always sorts first to ensure predictably ordered results
        formatted_results.sort()

        for criteria in self.sort_criteria:
            reverse = False
            if SortType.DESC == criteria["sort_type"]:
                reverse = True

            val = lambda k: k[criteria["field"]]["value"]

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                formatted_results.sort(key=lambda k: LooseVersion(val(k)), reverse=reverse)
            else:
                formatted_results.sort(key=val, reverse=reverse)

        return formatted_results
