class SortBase(object):
    @classmethod
    def get_sort_alias(cls, flag, aliases):
        """
            Determines if passed in flag is a SortFlag or an alias of a SortFlag.
            Args:
                flag(string): potential sort base alias.
                aliases(Dict{list}): aliases for attributes.

            Returns:
                SortBase or None: returns None if invalid flag.
        """
        for key, val in aliases.iteritems():
            if flag.upper() in val:
                return key

        return None
