from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.type import Type as SearchType
from pyshelf.search.metadata import Metadata


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
                list(dict): each dict represents a search "hit" with the keys specified in key_list.

        Example of criteria:

            }
                "version": {
                    "searchType": SearchType.EQUAL
                    "value": "1.9"
                }
           }
        """
        # Does an empty list represent a request for all keys??
        if not key_list:
            key_list = []

        query = Q()
        for key, val in criteria.iteritems():
            search_type = val["searchType"]
            if search_type == SearchType.TILDE:
                val["value"] = ".".join(val["value"].split(".")[:-1]) + ".?"
                search_type = SearchType.WILDCARD

            nested_query = Q(SearchType.MATCH, items__name=key) & Q(search_type, items__value=val["value"])
            query &= Q("nested", path="items", query=nested_query)

        results = Search().index(Metadata._doc_type.index).query(query).execute()
        return results
