class UpdateManager(object):
    def __init__(self, search_container):
        self.search_container = search_container

    def update(self, key, data):
        # key uniquely identifies some document
        pass

    def update_item(self, key, item_key, data):
        # update just that key
        pass
