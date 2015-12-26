def get_permissions_all():
    return """
        name: 'Andy Gertjejansen'
        token: '190a64931e6e49ccb9917c7f32a29d19'
        write:
          - '/*'
        read:
          - '/*'"""


def get_permissions_readonly():
    return """
        name: 'Andy Gertjejansen'
        token: '190a64931e6e49ccb9917c7f32a29d19'
        write:
          - ''
        read:
          - '/*'"""


def get_permissions_func_test():
    return """
        name: 'Andy Gertjejansen'
        token: '190a64931e6e49ccb9917c7f32a29d19'
        write:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'
        read:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'"""


def auth_header(is_valid=True):
    if is_valid:
        auth = "190a64931e6e49ccb9917c7f32a29d19"
    else:
        auth = "not a real key"
    return {"Authorization": auth}
