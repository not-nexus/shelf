import yaml
from fnmatch import fnmatch
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError


class PermissionsValidator(object):
    REQUIRES_WRITE = ["POST", "PUT", "DELETE"]
    REQUIRES_READ = ["GET", "HEAD"]

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
                permissions(dict|None): A dictionary of the data in the key file if it was found to exist.
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
        """
            Determines if the key associated with the request has permission to perform the request action.

            Returns:
                bool: user has access when True.
        """
        allowed = False
        if self.permissions:
            method = self.container.request.method
            path = self.container.request.path

            # Note: at this point searches only require the existance of any permissions for a bucket.
            # TODO: Perhaps implement separate listing permissions for searching to make search permissions explicit.
            if "/_search" in path:
                allowed = True
            elif method in PermissionsValidator.REQUIRES_WRITE and "/artifact/" in path:
                write = self.permissions.get("write")
                allowed = self._get_access(write)
            elif method in PermissionsValidator.REQUIRES_READ and "/artifact/" in path:
                read = self.permissions.get("read")
                allowed = self._get_access(read)

        return allowed

    def _get_access(self, permissions):
        """
            Determines if key associated with request has proper access.

            Args:
                permissions(dict): Permissions loaded from _keys directory of requested bucket.

            Returns:
                bool: sufficient permissions.
        """
        access = False
        dir_path = self.container.resource_identity.artifact_path
        artifact_path = self.container.resource_identity.cloud

        for p in permissions:
            if fnmatch(artifact_path, p) or fnmatch(dir_path, p):
                return True
        return access
