from shelf.cloud.cloud_exceptions import BucketNotFoundError


class ListShelvesManager(object):
    def __init__(self, shelf_list, permissions_loader):
        self.shelf_list = shelf_list
        self.permissions_loader = permissions_loader

    def list(self, token):
        authed_shelf_list = []

        for shelf in self.shelf_list:
            permissions = None

            try:
                permissions = self.permissions_loader.load(shelf, token)
            except BucketNotFoundError:
                pass

            if permissions and (permissions.get("read") or permissions.get("write")):
                authed_shelf_list.append(shelf)

        return authed_shelf_list
