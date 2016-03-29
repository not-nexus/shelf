from distutils.version import LooseVersion


class Wrapper(object):
    def __init__(self, criteria):
        self.search_criteria = criteria.get("search")
        # Sort criteria must be reversed to ensure first sort criteria takes precedence
        self.sort_criteria = reversed(criteria.get("sort", []))
        self.query = None
        self.results = None
        self.formatted_results = None
        self.tilde_search = {}

    def tilde_filter(self, item_name, item_value):
        return item_name in self.tilde_search.keys() and \
            LooseVersion(item_value) < LooseVersion(self.tilde_search[item_name])
