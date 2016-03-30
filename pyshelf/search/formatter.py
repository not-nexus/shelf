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
        self.tilde_search = {}

    @property
    def results(self):
        """
            Filtered and sorted results.
        """
        self._results = self._sort_results(self._filter_results())
        return self._results

    def _filter_version_search(self, item_name, item_value):
        """
            This ensures when a version search is done that any results that are
            less then the version that is passed in are dropped from the result set.

            Args:
                item_name
        """
        if not self.tilde_search:
            for criteria in self.search_criteria:
                if criteria["search_type"] == SearchType.VERSION:
                    self.tilde_search[criteria["field"]] = criteria["value"]

        return item_name in self.tilde_search.keys() and \
            LooseVersion(item_value) < LooseVersion(self.tilde_search[item_name])

    def _filter_results(self):
        """
            Filters search_results into a consumable format and returns it.

            Returns:
                 List[dict]: formatted and filtered results. Each list element represents a search hit and
                            each dictionary within represents a metadata item.
        """
        wrapper = []

        for hit in self.search_results.hits:
            filtered = {}
            add = True

            for item in hit.items:
                if self._filter_version_search(item.name, item.value):
                    add = False

                if self.key_list:

                    if item["name"] in self.key_list:
                        filtered.update({item["name"]: item})
                else:
                    filtered.update({item["name"]: item})

            if add:
                wrapper.append(filtered)

        return wrapper

    def _sort_results(self, formatted_results):
        """
            Sorts results based on sort criteria.

            Args:
                formatted_results(List[dict]): Result set as formatted by self._filter_results.

            Returns:
                List[dict]: sorted results.
        """
        for criteria in self.sort_criteria:
            kwargs = {}
            if SortType.DESC == criteria["sort_type"]:
                kwargs["reverse"] = True

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                formatted_results.sort(key=lambda k: LooseVersion(k[criteria["field"]]["value"]), **kwargs)
            else:
                formatted_results.sort(key=lambda k: k[criteria["field"]]["value"], **kwargs)

        return formatted_results
