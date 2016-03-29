from elasticsearch_dsl.query import Q
from elasticsearch_dsl import Search
from pyshelf.search.wrapper import Wrapper as SearchWrapper
from pyshelf.search.type import Type as SearchType
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag
from pyshelf.search.metadata import Metadata
from distutils.version import LooseVersion


class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container
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
        search = self._build_query(SearchWrapper(criteria))
        query = Search(using=self.host).index(Metadata._doc_type.index).query(search.query)
        self.search_container.logger.debug(query.to_dict())
        search.results = query.execute()
        search = self._filter_results(search, key_list)
        search = self._sort_results(search)

        return search.formatted_results

    def _sort_results(self, search):
        """
            Sorts results based on sort criteria.

            Args:
                search(pyshelf.search.wrapper.Wrapper): Wrapper object that encapsulates search properties.

            Returns:
                pyshelf.search.wrapper.Wrapper: Wrapper object that encapsulate shelf specific search properties.
        """
        # It is necessary to reverse the array so the first sort takes precedence
        for criteria in search.sort_criteria:
            kwargs = {}
            if SortType.DESC == criteria["sort_type"]:
                kwargs["reverse"] = True

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                search.formatted_results.sort(key=lambda k: LooseVersion(k[criteria["field"]]["value"]), **kwargs)
            else:
                search.formatted_results.sort(key=lambda k: k[criteria["field"]]["value"], **kwargs)

        return search

    def _filter_results(self, search, key_list=None):
        """
            Filters results into a consumable format.

            Args:
                search(pyshelf.search.wrapper.Wrapper): Wrapper object that encapsulates search properties.
                key_list(list): List of keys to return. None assumes all keys are required

            Returns:
                pyshelf.search.wrapper.Wrapper: Wrapper object that encapsulate shelf specific search properties.
        """
        wrapper = []

        for hit in search.results.hits:
            filtered = {}
            add = True

            for item in hit.items:
                if search.tilde_filter(item.name, item.value):
                    add = False

                if key_list:

                    if item["name"] in key_list:
                        filtered.update({item["name"]: item})
                else:
                    filtered.update({item["name"]: item})

            if add:
                wrapper.append(filtered)

        search.formatted_results = wrapper

        return search

    def _build_query(self, search):
        """
            Builds query based on search criteria encapsulated by the search object.

            Args:
                search(pyshelf.search.wrapper.Wrapper): Wrapper object that encapsulates search properties.

            Returns:
                pyshelf.search.wrapper.Wrapper: Wrapper object that encapsulate shelf specific search properties.
        """
        search.query = Q()
        for criteria in search.search_criteria:

            # The double underscores (items__name) represents a nested field (items.name) in Elasticsearch_dsl
            nested_query = Q(SearchType.MATCH, items__name=criteria["field"])

            if criteria["search_type"] == SearchType.VERSION:
                formatted = ".".join(criteria["value"].split(".")[:-1])
                if formatted:
                    formatted += ".*"
                    search.tilde_search[criteria["field"]] = criteria["value"]
                    nested_query &= Q(SearchType.WILDCARD, items__value=formatted)
                else:
                    nested_query &= Q("range", items__value={"gte": criteria["value"]})
            else:
                nested_query &= Q(criteria["search_type"], items__value=criteria["value"])
            search.query &= Q("nested", path="items", query=nested_query)

        return search
