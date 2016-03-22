class Manager(object):
    def __init__(self, search_container):
        self.search_container = search_container

    def search(self, criteria, key_list=None):
        """
            Builds ElasticSearch query.

            Args:
                criteria(dict): Criteria to use to initiate search.
                key_list(list): List of keys to receive back from a search.

            Returns:
                list(dict): each dict represents a search "hit" with the keys specified in key_list.
        """
        # Does an empty list represent a request for all keys??
        if not key_list:
            key_list = []
