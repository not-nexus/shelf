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
            if authorization.lower() == "supersecuretoken":
                allowed = True

        return allowed
