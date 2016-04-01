class Mapper(object):
    def to_response(self, metadata):
        """
            Although this happens to also be the response format, this
            is actually also the internal structure we need.

            TODO: Rename this to something more appropriate?

            Args:
                metadata(dict): Clouds structure for metadata

            Returns:
                schemas/metadata.json
        """
        new_metadata = {}

        for key, value in metadata.iteritems():
            value["name"] = key
            new_metadata[key] = self.create_response_property(key, value["value"], value["immutable"])

        return new_metadata

    def to_cloud(self, metadata):
        """
            Maps from the internal structure we use for metadata to
            the clouds format.

            Args:
                metadata(schemas/metadata.json)

            Returns:
                dict: The clouds format for metadata
        """
        new_metadata = {}
        for key, value in metadata.iteritems():
            new_metadata[key] = self.create_cloud_property(value["value"], value["immutable"])

        return new_metadata

    def create_cloud_property(self, value, immutable):
        """
            Creates a cloud metadata property

            Args:
                value(mixed)
                immutable(boolean)
        """
        return {
            "value": value,
            "immutable": immutable
        }

    def create_response_property(self, name, value, immutable):
        """
            Creates a single metadata property internal structure

            Args:
                name(string)
                value(mixed)
                immutable(boolean)

            Returns:
                schemas/metadata-property.json
        """
        return {
            "name": name,
            "value": value,
            "immutable": immutable
        }
