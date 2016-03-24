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
                dict: each element in the outer dict represents a search "hit" with the returned keys specified in key_list.

        Example of criteria:

            {
                "search": {
                    "version": {
                        "value": "1.1",
                        "search_type": SearchType.TILDE
                    }
                },
                "sort": {
                    "version": {
                        "sort_type": SortType.VERSION
                        "flag_list": [
                            SortType.ASC
                        ]
                    }
                }
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

        fields = sort_criteria.keys()

        for field in fields:
            if SortType.DESC in sort_criteria[field]["flag_list"]:
                if sort_criteria[field].get("sort_type") == SortType.VERSION:
                    newlist = sorted(filtered_results, key=lambda k: LooseVersion(k[field]["value"]), reverse=True)
                else:
                    newlist = sorted(filtered_results, key=lambda k: k[field]["value"], reverse=True)

            else:
                if sort_criteria[field].get("sort_type") == SortType.VERSION:
                    newlist = sorted(filtered_results, key=lambda k: LooseVersion(k[field]["value"]))
                else:
                    newlist = sorted(filtered_results, key=lambda k: k[field]["value"])
        return newlist

    def _filter_results(self, hits, key_list=None):
        """
            Filters results into a consumable format.
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

        for key, val in search_criteria.iteritems():
            nested_query = Q(SearchType.MATCH, items__name=key)

            if val["search_type"] == SearchType.TILDE:
                formatted = ".".join(val["value"].split(".")[:-1])

                if formatted:
                    formatted += ".*"
                formatted += "*"

                nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
            else:
                nested_query &= Q(val["search_type"], items__value=val["value"])

            query &= Q("nested", path="items", query=nested_query)

        return query
