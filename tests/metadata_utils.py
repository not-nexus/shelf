from shelf.metadata.keys import Keys


MD5 = "5eb63bbbe01eeed093cb22bb8f5acdc3"
CREATED_DATE = "2016-05-19T15:29:34Z"


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
        "createdDate": {
            "name": Keys.CREATED_DATE,
            "value": CREATED_DATE,
            "immutable": True
        },
        "md5Hash": {
            "name": Keys.MD5,
            "value": MD5,
            "immutable": True
        },
        "artifactName": {
            "name": Keys.NAME,
            "value": name,
            "immutable": True
        },
        "artifactPath": {
            "name": Keys.PATH,
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
    return get_meta()[Keys.MD5]


def send_meta():
    """
        This function is used to generate metadata that will
        be PUT back to the metadata endpoint but removes things
        that will be initialized which also happen to be
        immutable.

        See shelf.metadata.initializer.Initializer
    """
    d = get_meta()
    del d[Keys.NAME]
    del d[Keys.MD5]
    del d[Keys.PATH]
    del d[Keys.CREATED_DATE]
    return d


def send_meta_changed():
    d = get_meta()
    d["tag1"]["value"] = "changed value"
    return d
