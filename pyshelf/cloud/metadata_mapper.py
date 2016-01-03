import ast


def format_for_client(meta):
    formatted_meta = []
    if isinstance(meta, dict):
        for key, value in meta.iteritems():
            formatted_meta.append(ast.literal_eval(value))
    else:
        formatted_meta = ast.literal_eval(meta)
    return formatted_meta

def update_meta(new_meta, old_meta):
    meta = {}
    for key, value in old_meta.iteritems():
        value = dict(ast.literal_eval(value))
        if value['immutable']:
            meta[key] = value
        if not value['immutable'] and new_meta.get(key) is not None:
            meta[key] = new_meta[key]
    for key in new_meta:
        if key not in meta:
            meta[key] = new_meta[key]
    return meta

def format_hash(etag):
    meta = {
                "name": "md5Hash",
                "value": etag,
                "immutable": True
           }
    return meta
