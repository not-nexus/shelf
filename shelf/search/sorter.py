from distutils.version import LooseVersion
from shelf.search.sort_type import SortType
from shelf.search.sort_flag import SortFlag


class Sorter(object):
    def sort(self, data, sort_criteria):
        """
            Sorts results based on sort criteria.

            Args:
                data(List[dict]): Data to sort using given sort criteria.
                sort_criteria(schemas/sort-criteria.json): sort criteria.

            Returns:
                List[dict]: sorted results.
        """
        # Function that sorts results. Returns None if field being sorted on does not exist.
        # This causes results without the field that is being sorted by to be at the end
        # of the sort results on a DESC sort and beginning of ASC sort.
        # Used def as opposed to lambda because of my linter complained about assigning a lambda.
        def standard_sort(result):
            item = result.get(criteria["field"], {})
            value = item.get("value")

            return value

        # This sort only differs in two ways from the above. Rather then returning the default
        # `None` it returns "0" as this creates the proper sort order. Secondly, it uses
        # distutils.version.LooseVersion to facilitate the version sort.
        def version_sort(result):
            value = str(standard_sort(result))

            if value is None:
                value = "0"

            value = str(value)
            loose_version = LooseVersion(value)

            return loose_version

        # Criteria for sorting is reversed so the order is respected.
        # Basically the method we are using to search must started with the last
        # sort first so the first sort take precedence.
        sort_criteria.reverse()

        for criteria in sort_criteria:
            reverse = False
            if SortType.DESC == criteria["sort_type"]:
                reverse = True

            sort_func = standard_sort

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                sort_func = version_sort

            data.sort(key=sort_func, reverse=reverse)

        return data
