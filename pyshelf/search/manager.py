from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.formatter import Formatter as SearchFormatter
from pyshelf.search.type import Type as SearchType
from elasticsearch import Elasticsearch


class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container
        self.connection = Elasticsearch(self.search_container.es_url)
        self.index = self.search_container.es_index

    def search(self, criteria, key_list=None):
        """
            Builds ElasticSearch query.

            Args:
                criteria(schemas.search-layer-criteriai.json): Criteria to use to initiate search.
                key_list(list): List of keys to receive back from a search.

            Returns:
                dict: each element in the outer dict represents a search "hit"
                      with the returned keys specified in key_list.
        """
        query = self._build_query(criteria.get("search"))
        query = Search(using=self.connection).index(self.index).sort("_uid").query(query)
        self.search_container.logger.debug("Executing the following search query: {0}".format(query.to_dict()))
        search_results = query.execute()
        search_formatter = SearchFormatter(criteria, search_results, key_list)
        formatted_results = search_formatter.get_formatted_results()

        return formatted_results

    def _build_query(self, search_criteria):
        """
            Builds query based on search criteria encapsulated by the search object.

            Args:
                search_criteria(schemas.search-criteria.json): Criteria by which to search.

            Returns:
                elasticsearch_dsl.Query: Object representing an Elasticsearch query.
        """
        query = Q()
        for criteria in search_criteria:

            # The double underscores represents a nested field in Elasticsearch_dsl.
            # Ex. property_list__name => property_list.name (keyword args can be used as well).
            nested_query = Q(SearchType.MATCH, property_list__name=criteria["field"])

            if criteria["search_type"] == SearchType.VERSION:
                formatted = criteria["value"].rsplit(".", 1)
                value = formatted[0]
                if len(formatted) > 1:
                    value += ".*"
                    nested_query &= Q(SearchType.WILDCARD, property_list__value=value)
                else:
                    nested_query &= Q("range", property_list__value={"gte": value})
            else:
                nested_query &= Q(criteria["search_type"], property_list__value=criteria["value"])
            query &= Q("nested", path="property_list", query=nested_query)

        return query
