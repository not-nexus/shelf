import yaml
import fnmatch
import os
import re
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError


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
                with self.container.create_bucket_storage() as storage:
                    try:
                        raw_permissions = storage.get_artifact_as_string("_keys/" + authorization)
                    except ArtifactNotFoundError:
                        raw_permissions = None
                        self._permissions_loaded = True

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
            if method == "POST" or method == "PUT" or method == "DELETE" and "/artifact/" in path:
                write = self.permissions.get("write")
                allowed = self._get_access(write)
            if method == "GET" and "/artifact/" in path:
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
        # IMO this needs some serious refactoring. Pretty ugly, it started out simple and grew to its current state
        access = False
        path = self.container.request.path
        if path.endswith('/_meta'):
            path = re.sub('/_meta', '', path)
        if path.endswith('/_search'):
            path = re.sub('/_search', '', path)
        if re.search('\/_meta\/', path):
            ar = path.split('/_meta/')
            path = ar[0]

        prefix = "/{0}/artifact".format(self.container.bucket_name)
        path = re.sub(prefix, "", path)
        dir_path = os.path.dirname(path)
        dir_path = os.path.join(dir_path, '')
        for p in permissions:
            if fnmatch.fnmatch(path, p) or fnmatch.fnmatch(dir_path, p):
                return True
        return access
