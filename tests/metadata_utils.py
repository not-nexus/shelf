MD5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"


def get_meta_item():
    return {
        "name": "tag2",
        "value": "test",
        "immutable": False
    }


def get_meta(name="test", path="/test/artifact/test", version="1"):
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
        },
        "artifactName": {
            "name": "artifactName",
            "value": name,
            "immutable": True
        },
        "artifactPath": {
            "name": "artifactPath",
            "value": path,
            "immutable": True
        },
        "version": {
            "name": "version",
            "value": version,
            "immutable": False
        }
    }


def get_meta_elastic(name="test", path="/test/artifact/test", version="1"):
    return get_meta(name, path, version).values()


def get_md5Hash():
    return get_meta()["md5Hash"]


def send_meta():
    d = get_meta()
    d.pop("md5Hash")
    d.pop("artifactName")
    d.pop("artifactPath")
    for key, val in d.iteritems():
        if key == "name":
            val.pop(key)
    return d


def send_meta_changed():
    d = get_meta()
    d["tag1"]["value"] = "changed value"
    return d
