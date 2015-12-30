import yaml
import fnmatch
import os
import re


class PermissionsValidator(object):
    def __init__(self, container):
        self.container = container
        self._permissions = None
        self._permissions_loaded = False
        self.authorization_token = None
        self.name = "UNKNOWN"

    @property
    def permissions(self):
        """
            Returns:
                permissions(dict|None) -    A dictionary of the data in the key file if it
                                            was found to exist
        """
        if not self._permissions and not self._permissions_loaded:
            # No point in trying multiple times in a single request
            self._permissions_loaded = True
            authorization = self.container.request.headers.get("Authorization")
            self.authorization_token = authorization
            if authorization:
                with self.container.create_master_bucket_storage() as storage:
                    raw_permissions = storage.get_artifact_as_string("_keys/" + authorization)

                if raw_permissions:
                    self._permissions = yaml.load(raw_permissions)

                    if self._permissions.get("name"):
                        self.name = self._permissions["name"]
                    else:
                        self.container.logger.warning("Name was not set in authorization token.")

        return self._permissions

    def allowed(self):
        allowed = False
        if self.permissions:
            method = self.container.request.method
            path = self.container.request.path
            key_req = re.search('^\/artifact\/*', path)
            if method == "POST" or method == "PUT" and key_req:
                write = self.permissions.get("write")
                allowed = self._get_access(write)
            if method == "GET" and key_req:
                read = self.permissions.get("read")
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
        if path.endswith('/_meta'):
            path = re.sub('/_meta', '', path)
        if re.search('\/_meta\/', path):
            ar = path.split('/_meta/')
            path = ar[0]

        path = re.sub("/artifact", "", path)
        dir_path = os.path.dirname(path)
        dir_path = os.path.join(dir_path, '')
        for p in permissions:
            if fnmatch.fnmatch(path, p) or fnmatch.fnmatch(dir_path, p):
                return True
        return access
