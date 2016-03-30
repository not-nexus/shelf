from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.formatter import Formatter as SearchFormatter
from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata
from elasticsearch import Elasticsearch


class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container
        self.connection = Elasticsearch(self.search_container.es_host)

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
                        "search_type": SearchType.VERSION
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
        query = self._build_query(criteria.get("search"))
        query = Search(using=self.connection).index(self.search_container.es_index).query(query)
        self.search_container.logger.debug("Executing the following search query: {0}".format(query.to_dict()))
        search_results = query.execute()
        search_formatter = SearchFormatter(criteria, search_results, key_list)

        return search_formatter.results

    def _build_query(self, search_criteria):
        """
            Builds query based on search criteria encapsulated by the search object.

            Args:
                search_criteria(dict): Criteria by which to search.

            Returns:
                elasticsearch_dsl.Query: Object representing an Elasticsearch query.
        """
        query = Q()
        for criteria in search_criteria:

            # The double underscores (items__name) represents a nested field (items.name) in Elasticsearch_dsl
            nested_query = Q(SearchType.MATCH, items__name=criteria["field"])

            if criteria["search_type"] == SearchType.VERSION:
                formatted = ".".join(criteria["value"].split(".")[:-1])
                if formatted:
                    formatted += ".*"
                    nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
                else:
                    nested_query &= Q("range", items__value={"gte": criteria["value"]})
            else:
                nested_query &= Q(criteria["search_type"], items__value=criteria["value"])
            query &= Q("nested", path="items", query=nested_query)

        return query
