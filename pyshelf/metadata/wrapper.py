class Wrapper(dict):
    def is_immutable(self, key):
        item = self.get(key)
        if item and item["immutable"]:
            return True
        else:
            return False
