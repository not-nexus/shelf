class Manager(object):
    def __init__(self, container):
        self.container = container
        # TODO: Use this line when we have it
        # self.update_manager = self.container.search.update_manager
        self.identity = self.container.resource_identity
        self.mapper = self.container.mapper

    def load(self):
        pass
