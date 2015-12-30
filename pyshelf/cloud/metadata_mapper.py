import ast
import json


class MetadataMapper(object):
    
    def format_for_boto(self, meta):
        formatted_meta = json.loads(meta)
        return formatted_meta

    def format_for_client(self, meta):
        formatted_meta = []
        if isinstance(meta, dict):
            for key, value in meta.iteritems():
                formatted_meta.append(ast.literal_eval(value))
        else:
            formatted_meta = ast.literal_eval(meta)
        return formatted_meta

    def update_meta(self, new_meta, old_meta):
        meta = {}
        for key, value in old_meta.iteritems():
            value = dict(ast.literal_eval(value))
            if value['immutable']:
                meta[key] = value
            if not value['immutable'] and new_meta[key]:
                meta[key] = new_meta[key]
        for key in new_meta:
            if not key in meta:
                meta[key] = new_meta[key]
        return meta 
