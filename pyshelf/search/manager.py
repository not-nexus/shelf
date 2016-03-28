from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.metadata import Metadata
from distutils.version import LooseVersion


class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container

    def search(self, criteria, key_list=None):
        """
            Builds ElasticSearch query.

            Args:
                criteria(dict): Criteria to use to initiate search. Example below.
                key_list(list): List of keys to receive back from a search.

            Returns:
                dict: each element in the outer dict represents a search "hit"
                      with the returned keys specified in key_list.

        Example of criteria:

            {
                "search": [
                    {
                        "field": "version",
                        "value": "1.1",
                        "search_type": SearchType.TILDE
                    }
                ],
                "sort": [
                    {
                        "field": "version",
                        "sort_type": SortType.VERSION,
                        "flag_list": [
                            SortType.ASC
                        ]
                    }
                ]
            }
        """
        query = Search().index(Metadata._doc_type.index).query(self._build_query(criteria["search"]))
        results = query.execute()
        filtered_results = self._filter_results(results.hits, key_list)
        formated_results = self._sort_results(filtered_results, criteria.get("sort"))

        return formated_results

    def _sort_results(self, filtered_results, sort_criteria=None):
        """
            Sorts results based on sort criteria.
        """
        if not sort_criteria:
            return filtered_results

        for criteria in sort_criteria:
            kwargs = {}
            if SortType.DESC in criteria["flag_list"]:
                kwargs.update({"reverse": True})

            if criteria.get("sort_type") == SortType.VERSION:
                filtered_results.sort(key=lambda k: LooseVersion(k[criteria["field"]]["value"]), **kwargs)
            else:
                filtered_results.sort(key=lambda k: k[criteria["field"]]["value"], **kwargs)

        return filtered_results

    def _filter_results(self, hits, key_list=None):
        """
            Filters results into a consumable format.

            Args:
                hits(list(elasticsearch_dsl.Result): List of result objects as returned from Response.hits
                key_list(list): List of keys to return. None assumes all keys are requeired

            Returns:
                list(dict): Formats result list to a list of dictionaries. Each element of the list representing a hit.
        """
        wrapper = []

        for hit in hits:
            filtered = {}

            for item in hit.items:
                if key_list:

                    if item["name"] in key_list:
                        filtered.update({item["name"]: item})
                else:
                    filtered.update({item["name"]: item})
            wrapper.append(filtered)

        return wrapper

    def _build_query(self, search_criteria):
        """
            Builds query based on search criteria.
        """
        query = Q()
        for criteria in search_criteria:
            nested_query = Q(SearchType.MATCH, items__name=criteria["field"])

            if criteria["search_type"] == SearchType.TILDE:
                formatted = ".".join(criteria["value"].split(".")[:-1])
                if formatted:
                    formatted += ".*"
                formatted += "*"
                nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
            else:
                nested_query &= Q(criteria["search_type"], items__value=criteria["value"])
            query &= Q("nested", path="items", query=nested_query)

        return query
