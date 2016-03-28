class Mapper(object):
    def to_response(self, metadata):
        new_metadata = {}

        for key, value in metadata.iteritems():
            value["name"] = key
            new_metadata[key] = self.create_response_item(key, value["value"], value["immutable"])

        return new_metadata

    def to_cloud(self, metadata):
        new_metadata = {}
        for key, value in metadata.iteritems():
            new_metadata[key] = self.create_cloud_item(value["value"], value["immutable"])

        return new_metadata

    def create_cloud_item(self, value, immutable):
        return {
            "value": value,
            "immutable": immutable
        }

    def create_response_item(self, name, value, immutable):
        return {
            "name": name,
            "value": value,
            "immutable": immutable
        }
