class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container

    def search(self, criteria, key_list=None):
        """
            Builds ElasticSearch query.

            Args:
                criteria(list(dict)): Criteria to use to initiate search. Example below.
                key_list(list): List of keys to receive back from a search.

            Returns:
                list(dict): each dict represents a search "hit" with the keys specified in key_list.

        Example of criteria:

            [
                "version": {
                    "comparison": SearchType.WILDCARD_TILDE
                    "value": "1.0"
                },
                "blah": {
                    "comparison": SearchType.WILDCARD_EQUAL,
                    "value": "blah*"
                },
                # path is added based on which uri was searched
                "artifactPath": {
                    "comparison": SearchType.WILDCARD_EQUAL,
                    "value": "/lol/*"
                }
            ]
        """
        # Does an empty list represent a request for all keys??
        if not key_list:
            key_list = []
