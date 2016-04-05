from pyshelf.search.sort_base import SortBase


class SortType(SortBase):
    ASC = "ASC"
    DESC = "DESC"

    ALIASES = {
        "ASC": [
            "ASC",
            "ASCENDING"
        ],
        "DESC": [
            "DESC",
            "DESCENDING"
        ]
    }

    @classmethod
    def get_alias(cls, flag):
        return super(SortType, cls).get_sort_alias(flag, SortType.ALIASES)
