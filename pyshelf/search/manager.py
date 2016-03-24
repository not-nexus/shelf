from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.type import Type as SearchType
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
                        "searchType": SearchType.TILDE
                    }
                },
                "sort": {
                    "version": {
                        "sortType": [SortType.VERSION, SortType.ASC]
                    }
                },
                "limit": 1
            }
        """
        query = Search().index(Metadata._doc_type.index).query(self._build_query(criteria["search"]))
        results = query.execute()

        formated_results = self._filter_results(results.hits, key_list, criteria.get("sort"), criteria.get("limit"))
        return formated_results

    def _filter_results(self, hits, key_list=None, sort_criteria=None, limit=None):
        """
            Sorts results based on sorting criteria.
        """
        wrapper = {}
        for hit in hits:
            filtered = []

            for item in hit.items:
                if key_list:
                    if item["name"] in key_list:
                        filtered.append(item)
                else:
                    filtered.append(item)

            wrapper[hit.meta.id] = filtered

        return wrapper

    def _build_query(self, search_criteria):
        """
            Builds query based on search criteria.
        """
        query = Q()

        for key, val in search_criteria.iteritems():
            nested_query = Q(SearchType.MATCH, items__name=key)

            if val["searchType"] == SearchType.TILDE:
                formatted = ".".join(val["value"].split(".")[:-1])

                if formatted:
                    formatted += ".*"
                formatted += "*"

                nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
            else:
                nested_query &= Q(val["searchType"], items__value=val["value"])

            query &= Q("nested", path="items", query=nested_query)

        return query
