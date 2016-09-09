VALID_KEY = "190a64931e6e49ccb9917c7f32a29d19"


def get_permissions_all():
    return """
        name: 'Andy Gertjejansen'
        token: {0}
        write:
          - '/*'
        read:
          - '/*'""".format(VALID_KEY)


def get_permissions_readonly():
    return """
        name: 'Andy Gertjejansen'
        token: {0}
        write:
          - ''
        read:
          - '/*'""".format(VALID_KEY)


def get_permissions_no_name():
    return """
        token: {0}
        write:
          - ''
        read:
          - '/*'""".format(VALID_KEY)


def get_permissions_func_test():
    return """
        name: 'Andy Gertjejansen'
        token: {0}
        write:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'
        read:
          - '/'
          - '/dir/dir2/'
          - '/dir/dir2/dir3/*'""".format(VALID_KEY)


def auth_header():
    return {"Authorization": VALID_KEY}
