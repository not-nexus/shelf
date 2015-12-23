import yaml


class PermissionsValidator(object):
    def __init__(self, container):
        self.container = container

    def allowed(self):
        allowed = False
        authorization = self.container.request.headers.get("Authorization")
        if authorization:
            # TODO : Fix this to actually auth against a real
            # token stored in S3
            # Super fake auth right now.
            with self.container.create_master_bucket_storage() as storage:
                raw_permissions = storage.get_permissions_key(authorization)
                if raw_permissions:
                    permissions = yaml.load(raw_permissions)    
                    if authorization.lower() == permissions.get("token"):
                        allowed = True

        return allowed
