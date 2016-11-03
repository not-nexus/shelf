from distutils.version import LooseVersion
from shelf.search.type import Type as SearchType


class Formatter(object):
    def __init__(self, criteria, search_results, key_list=None):
        """
            Formats search results from Elasticsearch based on the given criteria.

            Args:
                criteria(dict): This contains the search and sort criteria as outlined on
                                shelf.search.manager.Manager.search.
                search_results(List[elasticsearch_dsl.result.Result]): List of search results.
                key_list(list): list of keys to include in filtered results if list is not passed
                                all fields will be returned.
        """
        self.search_criteria = criteria.get("search")
        self.search_results = search_results
        self.key_list = key_list
        self.version_search = self._get_version_search()

    def get_formatted_results(self):
        """
            Filters and formats elasticsearch search results.

            Returns:
                List[dict]: Formatted results.
        """
        result_list = self._normalize_result_list(self.search_results.hits)
        filtered_results = self._filter_metadata(result_list)
        filtered_results = self._filter_metadata_properties(filtered_results)
        return filtered_results

    def _get_version_search(self):
        """
            Determines if a version search has been requested and stores the
            field and value if so for future result filtering.

            Returns:
                dict
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
        item_version = LooseVersion(metadata_property["value"])
        searched_version = LooseVersion(self.version_search[metadata_property["name"]])

        return searched_version <= item_version

    def _filter_metadata(self, result_list):
        """
            Filters search_results into a consumable format and returns it.

            Args:
                result_list(List[dict])

            Returns:
                 List[dict]: formatted and filtered results. Each list element represents a search hit and
                            each dictionary within represents a metadata item.
        """
        filtered_list = []

        for metadata in result_list:
            add = True
            filtered = {}

            for metadata_property in metadata["property_list"]:
                if self._is_version_search(metadata_property["name"]):
                    if not self._sufficient_version(metadata_property):
                        add = False
                        break

                filtered[metadata_property["name"]] = metadata_property

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
        filtered_list = []
        if self.key_list:

            for metadata in filtered_results:
                filtered_metadata = {}

                for key in self.key_list:
                    filtered_metadata[key] = metadata.get(key)
                    filtered_list.append(filtered_metadata)

            return filtered_list

        return filtered_results

    def _normalize_result_list(self, result_list):
        """
            Exists so we get regular dicts to use
            instead of special elasticsearch_dsl.utils.AttrDict

            Args:
                result_list(List[elasticsearch_dsl.utils.AttrDict])

            Returns:
                List[dict]
        """
        new_list = []
        for result in result_list:
            new_list.append(result.to_dict())

        return new_list
