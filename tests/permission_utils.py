VALID_TOKEN = "190a64931e6e49ccb9917c7f32a29d19"
READ_ONLY_TOKEN = "READONLY"
FULL_TOKEN = "FULLON"


def get_permissions_all():
    return """
        name: 'Andy Gertjejansen'
        token: {0}
        write:
          - '/*'
        read:
          - '/*'""".format(VALID_TOKEN)


def get_permissions_readonly():
    return """
        name: 'Andy Gertjejansen'
        token: {0}
        read:
          - '/*'""".format(READ_ONLY_TOKEN)


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
          - '/dir/dir2/dir3/*'""".format(VALID_TOKEN)


def get_permissions(token):
    if token == VALID_TOKEN:
        return get_permissions_func_test()
    elif token == READ_ONLY_TOKEN:
        return get_permissions_readonly()

    return get_permissions_all()


def auth_header(token):
    return {
        "Authorization": token
    }
