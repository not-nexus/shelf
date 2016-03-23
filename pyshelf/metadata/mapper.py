class Mapper(object):
    def to_response(self, metadata):
        new_metadata = {}

        for key, value in metadata.iteritems():
            value["name"] = key
            new_metadata[key] = value

        return new_metadata

    def to_cloud(self, metadata):
        new_metadata = {}
        for key, value in metadata.iteritems():
            del value["name"]
            new_metadata[key] = value

        return new_metadata
