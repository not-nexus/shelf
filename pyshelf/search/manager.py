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
                dict: each element in the outer dict represents a search "hit" with the returned keys specified in key_list.

        Example of criteria:

            }
                "version": {
                    "searchType": SearchType.EQUAL
                    "value": "1.9"
                }
           }
        """
        query = Q()
        for key, val in criteria.iteritems():
            search_type = val["searchType"]
            if search_type == SearchType.TILDE or search_type == SearchType.WILDCARD_TILDE:
                val["value"] = ".".join(val["value"].split(".")[:-1]) + ".?"
                search_type = SearchType.WILDCARD

            nested_query = Q(SearchType.MATCH, items__name=key) & Q(search_type, items__value=val["value"])
            query &= Q("nested", path="items", query=nested_query)

        results = Search().index(Metadata._doc_type.index).query(query).execute()

        wrapper = {}
        for hit in results.hits:
            filtered = []

            for item in hit.items:
                if key_list:
                    if item["name"] in key_list:
                        filtered.append(item)
                else:
                    filtered.append(item)

            wrapper[hit.meta.id] = filtered

        return wrapper
