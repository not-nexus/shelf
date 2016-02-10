import json


MD5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"


def get_meta_item():
    return {
                "name": "tag2",
                "value": "test",
                "immutable": False
            }


def get_meta():
    return {
            "tag": {
                    "name": "tag",
                    "value": "test",
                    "immutable": False
                    },
            "tag1": {
                    "name": "tag1",
                    "value": "test1",
                    "immutable": True
                    },
            "md5Hash": {
                    "name": "md5Hash",
                    "value": MD5,
                    "immutable": True
                    }
            }


def get_md5Hash():
    return get_meta()["md5Hash"]


def send_meta():
    d = get_meta()
    d.pop("md5Hash")
    return json.dumps(d)


def send_meta_item():
    return json.dumps(get_meta_item())


def send_meta_changed():
    d = get_meta()
    d["tag1"]["value"] = "changed value"
    return json.dumps(d)
