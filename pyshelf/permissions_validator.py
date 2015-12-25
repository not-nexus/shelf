import yaml
import fnmatch
import os
import re


class PermissionsValidator(object):
    def __init__(self, container):
        self.container = container

    def allowed(self):
        allowed = False
        authorization = self.container.request.headers.get("Authorization")
        if authorization:
            # TODO : Parse permissions
            with self.container.create_master_bucket_storage() as storage:
                raw_permissions = storage.get_artifact_as_string("_keys/" + authorization)
                if raw_permissions:
                    permissions = yaml.load(raw_permissions)
                    token = permissions.get("token")
                    if authorization.lower() == token:
                        method = self.container.request.method
                        path = self.container.request.path
                        key_req = re.search('^\/artifact\/*', path)
                        if method == "POST" and key_req:
                            write = permissions.get("write")
                            allowed = self._get_access(write)
                        if method == "GET" and key_req:
                            read = permissions.get("read")
                            allowed = self._get_access(read)

        return allowed

    def _get_access(self, permissions):
        """
            Parses permissions and compares it to request path to ensure user
            has proper access. To allow for read access to only specific files
            in a directory two paths are compared using fnmatch. The full path
            of the artifact and the directory of the artifact.
        """
        access = False
        path = self.container.request.path
        path = re.sub("/artifact", "", path)
        dir_path = os.path.dirname(path)
        dir_path = os.path.join(dir_path, '')
        self.container.logger.debug("Path: {} - Permissions: {}".format(path, permissions))
        for p in permissions:
            if fnmatch.fnmatch(path, p) or fnmatch.fnmatch(dir_path, p):
                return True
        return access
