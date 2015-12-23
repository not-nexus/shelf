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
                    write = permissions.get("write")
                    read = permissions.get("read")
                    if authorization.lower() == token:
                        allowed = True

        return allowed
    

