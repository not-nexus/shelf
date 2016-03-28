import os.path
import hashlib


class ResourceIdentity(object):
    def __init__(self, resource_url, bucket_name=None, artifact_path=None):
        if resource_url[0] != "/":
            resource_url = "/" + resource_url

        # To get rid of redundant separators
        self.resource_url = os.path.normpath(resource_url)
        self._bucket_name = bucket_name
        self._artifact_path = artifact_path

        self._parse(self.resource_url)
        self._search = None
        self._cloud_metadata = None
        self._artifact_name = None

    @property
    def bucket_name(self):
        if not self._bucket_name:
            self._bucket_name = self._part_list[1]

        return self._bucket_name

    @property
    def artifact_path(self):
        if not self._artifact_path:
            # removes /<bucket>/artifact
            self._artifact_path = "/" + os.path.join(*self._part_list[3:])

        return self._artifact_path

    @property
    def artifact_name(self):
        if not self._artifact_name:
            self._artifact_name = self._part_list[-1]

        return self._artifact_name

    @property
    def cloud(self):
        return self.artifact_path

    @property
    def search(self):
        if not self._search:
            self._search = hashlib.sha256(self.bucket_name + ":" + self.artifact_path).hexdigest()

        return self._search

    @property
    def cloud_metadata(self):
        if not self._cloud_metadata:
            self._cloud_metadata = os.path.join(self.artifact_path, "_meta")

        return self._cloud_metadata

    def _parse(self, resource_url):
        part_list = resource_url.split("/")
        # Finds the first occurance of the special type
        index = self._try_index(part_list, ["_search", "_meta"])

        if index:
            self.type = part_list[index]
            part_list = part_list[:index]

        self._part_list = part_list

    def _try_index(self, part_list, key_list):
        index = None
        for key in key_list:
            try:
                index = part_list.index(key)
            except ValueError:
                pass

            if index:
                break

        return index
