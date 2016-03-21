

class Manager(object):
    def __init__(self, container):
        self.container = container

    def search(self, criteria, key_list=None):
        if not key_list:
            key_list = []
        # searches elasticsearch
        #
        # returns a list of dicts that only have the
        # keys specified in key list
