from pyshelf.search.sort_base import SortBase


class SortFlag(SortBase):
    VERSION = "VERSION"

    #Aliases for all sort flags where the key is the appropriate name.
    ALIASES = {
        "VERSION": [
            "VER",
            "VERSION"
        ]
    }

    @classmethod
    def get_alias(cls, flag):
        return super(SortFlag, cls).get_sort_alias(flag, SortFlag.ALIASES)
