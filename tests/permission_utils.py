import json


VALID_KEY = "190a64931e6e49ccb9917c7f32a29d19"
MD5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"

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

def get_meta_item():
    return {
            "tag2":{
                    "name": "tag2", 
                    "value": "test", 
                    "immutable": False 
                }
           }

def get_meta():
    return { 
            "tag":{
                    "name": "tag", 
                    "value": "test", 
                    "immutable": False 
                },
            "tag1":{
                    "name": "tag1", 
                    "value": "test1", 
                    "immutable": True 
                }
            }


def get_meta_body():
    return [ 
                {
                    "name": "md5Hash", 
                    "value": MD5, 
                    "immutable": True 
                },
                {
                    "name": "tag", 
                    "value": "test", 
                    "immutable": False 
                },
                {
                    "name": "tag1", 
                    "value": "test1", 
                    "immutable": True 
                }
           ]

def send_meta():
    return json.dumps(get_meta())

def send_meta_item():
    return json.dumps(get_meta_item())

def send_meta_changed():
    dic = get_meta()
    dic["tag1"]["value"] = "changed value"
    return json.dumps(dic)

def auth_header(is_valid=True):
    if is_valid:
        auth = VALID_KEY
    else:
        auth = "not a real key"
    return {"Authorization": auth}
