from distutils.version import LooseVersion
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.type import Type as SearchType


class Formatter(object):
    def __init__(self, criteria, search_results, key_list=None):
        """
            Formats search results from Elasticsearch based on the given criteria.

            Args:
                criteria(dict): This contains the search and sort criteria as outlined on
                                pyshelf.search.manager.Manager.search.
                search_results(List[elasticsearch_dsl.result.Result]): List of search results.
                key_list(list): list of keys to include in filtered results if list is not passed
                                all fields will be returned.
        """
        self.search_criteria = criteria.get("search")
        # Sort criteria must be reversed to ensure first sort criteria takes precedence
        self.sort_criteria = reversed(criteria.get("sort", []))
        self.key_list = key_list
        self.search_results = search_results
        self._results = None
        self.version_search = {}

    @property
    def results(self):
        """
            Filtered and sorted results.
        """
        self._results = self._sort_results(self._filter_results())
        return self._results

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
        if not self.version_search:
            for criteria in self.search_criteria:
                if criteria["search_type"] == SearchType.VERSION:
                    self.version_search[criteria["field"]] = criteria["value"]

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

    def _filter_results(self):
        """
            Filters search_results into a consumable format and returns it.

            Returns:
                 List[dict]: formatted and filtered results. Each list element represents a search hit and
                            each dictionary within represents a metadata item.
        """
        filtered_list = []

        for hit in self.search_results.hits:
            filtered = {}
            add = True

            for metadata_property in hit.items:
                if self._is_version_search(metadata_property.name):
                    if not self._sufficient_version(metadata_property):
                        add = False
                        break

                if self.key_list:

                    if metadata_property["name"] in self.key_list:
                        filtered.update({metadata_property["name"]: metadata_property})
                else:
                    filtered.update({metadata_property["name"]: metadata_property})

            if add:
                filtered_list.append(filtered)

        return filtered_list

    def _sort_results(self, formatted_results):
        """
            Sorts results based on sort criteria.

            Args:
                formatted_results(List[dict]): Result set as formatted by self._filter_results.

            Returns:
                List[dict]: sorted results.
        """
        # Always sorts first to ensure predictably ordered results
        formatted_results.sort()

        for criteria in self.sort_criteria:
            kwargs = {}
            if SortType.DESC == criteria["sort_type"]:
                kwargs["reverse"] = True

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                formatted_results.sort(key=lambda k: LooseVersion(k[criteria["field"]]["value"]), **kwargs)
            else:
                formatted_results.sort(key=lambda k: k[criteria["field"]]["value"], **kwargs)

        return formatted_results
