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
            # removes /<bucket>/artifact and removes the artifact_name at the end
            artifact_path_part_list = []
            if len(self._part_list) > 4:
                artifact_path_part_list = self._part_list[3:-1]
                self._artifact_path = "/" + os.path.join(*artifact_path_part_list)
            else:
                self._artifact_path = "/"

        return self._artifact_path

    @property
    def artifact_name(self):
        if not self._artifact_name:
            self._artifact_name = self._part_list[-1]

        return self._artifact_name

    @property
    def cloud(self):
        return os.path.join(self.artifact_path, self.artifact_name)

    @property
    def search(self):
        if not self._search:
            to_hash = self.bucket_name + ":" + self.artifact_path + ":" + self.artifact_name
            self._search = hashlib.sha256(to_hash).hexdigest()

        return self._search

    @property
    def cloud_metadata(self):
        if not self._cloud_metadata:
            self._cloud_metadata = os.path.join(self.artifact_path, "_metadata_{0}.yaml".format(self.artifact_name))

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

            if None is not index:
                break

        return index
