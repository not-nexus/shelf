import yaml


class PermissionsValidator(object):
    def __init__(self, container):
        self.container = container

    def allowed(self):
        allowed = False
        authorization = self.container.request.headers.get("Authorization")
        if authorization:
            # TODO : Parse permissions 
            with self.container.create_master_bucket_storage() as storage:
                raw_permissions = storage.get_permissions_key(authorization)
                if raw_permissions:
                    permissions = yaml.load(raw_permissions)    
                    token = permissions.get("token")
                    if authorization.lower() == token:
                        allowed = self._get_access(permissions) 

        return allowed
    
    def _get_access(self, permissions):
        method = self.container.request.method 
        path = self.container.request.path
        allowed = True
        if method == "POST":
            write = permissions.get("write")
            allowed = self._parse_glob(write)
        if method == "GET":
            read = permissions.get("read")
            allowed = self._parse_glob(read)
        return allowed

    def _parse_glob(self, glob):
        return True
