VALID_KEY = "190a64931e6e49ccb9917c7f32a29d19"


def get_permissions_all():
    return """
        name: 'Andy Gertjejansen'
        token: {}
        write:
          - '/*'
        read:
          - '/*'""".format(VALID_KEY)


def get_permissions_readonly():
    return """
        name: 'Andy Gertjejansen'
        token: {}
        write:
          - ''
        read:
          - '/*'""".format(VALID_KEY)


def get_permissions_func_test():
    return """
        name: 'Andy Gertjejansen'
        token: {}
        write:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'
        read:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'""".format(VALID_KEY)


def get_meta(immutable=False):
    return {"key": "value", "key1": "value", "immutable": immutable}


def auth_header(is_valid=True):
    if is_valid:
        auth = VALID_KEY
    else:
        auth = "not a real key"
    return {"Authorization": auth}
