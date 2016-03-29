from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.metadata import Metadata
from distutils.version import LooseVersion


class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container
        self.tilde_search = None
        self.host = self.search_container.elastic_search

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
                        "sort_type": SortType.ASC,
                        "flag_list": [
                            SortFlag.VERSION
                        ]
                    }
                ]
            }
        """
        query = Search(using=self.host).index(Metadata._doc_type.index).query(self._build_query(criteria["search"]))
        self.search_container.logger.debug(query.to_dict())
        results = query.execute()
        filtered_results = self._filter_results(results.hits, key_list)
        formated_results = self._sort_results(filtered_results, criteria.get("sort"))

        return formated_results

    def _sort_results(self, filtered_results, sort_criteria=None):
        """
            Sorts results based on sort criteria.

            Args:
                filtered_results(list(dict)): list of dictionaries representing hits from Elasticsearch.

            Returns:
                list(dict): Sorts the filtered results that are passed in.
        """
        if not sort_criteria:
            return filtered_results

        # It is necessary to reverse the array so the first sort takes precedence
        for criteria in reversed(sort_criteria):
            kwargs = {}
            if SortType.DESC == criteria["sort_type"]:
                kwargs["reverse"] = True

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
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
            add = True

            for item in hit.items:
                if item.name in self.tilde_search.keys() and LooseVersion(item.value) < \
                        LooseVersion(self.tilde_search[item.name]):
                    add = False

                if key_list:

                    if item["name"] in key_list:
                        filtered.update({item["name"]: item})
                else:
                    filtered.update({item["name"]: item})

            if add:
                wrapper.append(filtered)

        return wrapper

    def _build_query(self, search_criteria):
        """
            Builds query based on search criteria.

            Args:
                search_criteria(list(dict)): each dictionary represents a search. Formatted as above.

            Returns:
                elasticsearch_dsl.query.Q: This object represents an Elasticsearch query.
        """
        self.tilde_search = {}
        query = Q()
        for criteria in search_criteria:
            nested_query = Q(SearchType.MATCH, items__name=criteria["field"])

            if criteria["search_type"] == SearchType.TILDE:
                formatted = ".".join(criteria["value"].split(".")[:-1])
                if formatted:
                    formatted += ".*"
                    self.tilde_search[criteria["field"]] = criteria["value"]
                    nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
                else:
                    nested_query &= Q("range", items__value={"gte": criteria["value"]})
            else:
                nested_query &= Q(criteria["search_type"], items__value=criteria["value"])
            query &= Q("nested", path="items", query=nested_query)

        return query
