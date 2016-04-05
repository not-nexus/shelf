class SortFlag(object):
    VERSION = "VERSION"

    ALIASES = {
        "VERSION": VERSION,
        "VER": VERSION
    }

    @classmethod
    def get_alias(cls, alias):
        """
            Determines if passed in flag is a SortFlag or an alias of a SortFlag.
            Args:
                alias(string): pyshelf.search.sort_flag.SortFlag alias.

            Returns:
                pyshelf.search.sort_flag.SortFlag or None: returns None if invalid alias.
        """
        return SortFlag.ALIASES.get(alias)
