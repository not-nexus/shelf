import ast
import json


class MetadataMapper(object):
    
    def format_for_boto(self, meta):
        formatted_meta = json.loads(meta)
        return formatted_meta

    def format_for_client(self, meta):
        formatted_meta = []
        for key, value in meta.iteritems():
            formatted_meta.append(ast.literal_eval(value))
        return formatted_meta
