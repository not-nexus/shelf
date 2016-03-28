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
        self._part_list = self._load_part_list(self.resource_url)
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

    def _load_part_list(self, resource_url):
        part_list = resource_url.split("/")
        special_type = part_list[-1]
        if special_type == "_search" or special_type == "_meta":
            part_list = part_list[:-1]
            self.type = special_type
        else:
            self.type = None

        return part_list
