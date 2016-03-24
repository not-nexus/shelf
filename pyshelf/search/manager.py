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
        query = Search().index(Metadata._doc_type.index).query(self._build_query(criteria))
        results = query.execute()

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

    def _build_query(self, criteria):
        query = Q()

        for key, val in criteria.iteritems():
            nested_query = Q(SearchType.MATCH, items__name=key)

            if val["searchType"] == SearchType.TILDE:
                minor_versions = val["value"] + ".*"
                nested_query &= Q(SearchType.WILDCARD, items__value=minor_versions) | Q(SearchType.MATCH, items__value=val["value"])
            else:
                nested_query &= Q(val["searchType"], items__value=val["value"])

            query &= Q("nested", path="items", query=nested_query)

        return query
