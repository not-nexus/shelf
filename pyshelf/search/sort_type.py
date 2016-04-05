class SortType(object):
    ASC = "ASC"
    DESC = "DESC"

    ALIASES = {
        "ASC": ASC,
        "ASCENDING": ASC,
        "DESC": DESC,
        "DESCENDING": DESC
    }

    @classmethod
    def get_alias(cls, alias):
        """
            Determines if passed in alias is a SortType or an alias of a SortType.
            Args:
                alias(string): pyshelf.search.sort_type.SortType alias.

            Returns:
                pyshelf.search.sort_type.SortType or None: returns None if invalid alias.
        """
        return SortType.ALIASES.get(alias)
