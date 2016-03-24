import os.path
import hashlib


class ResourceIdentity(object):
    def __init__(self, resource_url, bucket_name=None, path=None):
        if resource_url[0] != "/":
            resource_url = "/" + resource_url

        # To get rid of redundant separators
        self.resource_url = os.path.normpath(resource_url)
        self._bucket_name = bucket_name
        self._path = path
        self._part_list = self.resource_url.split("/")
        self._search = None

    @property
    def bucket_name(self):
        if not self._bucket_name:
            self._bucket_name = self._part_list[1]

        return self._bucket_name

    @property
    def path(self):
        if not self._path:
            self._path = "/" + os.path.join(*self._part_list[3:])

        return self._path

    @property
    def cloud(self):
        return self.path

    @property
    def search(self):
        if not self._search:
            self._search = hashlib.sha256(self.bucket_name + ":" + self.path).hexdigest()

        return self._search
