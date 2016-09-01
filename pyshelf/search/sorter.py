from distutils.version import LooseVersion
from pyshelf.search.sort_type import SortType
from pyshelf.search.sort_flag import SortFlag


class Sorter(object):
    def sort(self, data, sort_criteria):
        """
            Sorts results based on sort criteria.

            Args:
                data(List[dict]): Data to sort using given sort criteria.

            Returns:
                List[dict]: sorted results.
        """
        # Function that sorts results. Returns None if field being sorted on does not exist.
        # This causes results without the field that is being sorted by to be at the end
        # of the sort results on a DESC sort and beginning of ASC sort.
        # Used def as opposed to lambda because of my linter complained about assigning a lambda.
        def sort_result(result):
            return result.get(criteria["field"], {}).get("value")

        # Criteria for sorting is reversed so the order is respected.
        # Basically the method we are using to search must started with the last
        # sort first so the first sort take precedence.
        sort_criteria.reverse()

        for criteria in sort_criteria:
            reverse = False
            if SortType.DESC == criteria["sort_type"]:
                reverse = True

            if criteria.get("flag_list") and SortFlag.VERSION in criteria.get("flag_list"):
                data.sort(key=lambda k: LooseVersion(sort_result(k)), reverse=reverse)
            else:
                data.sort(key=sort_result, reverse=reverse)

        return data
