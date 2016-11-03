from copy import deepcopy


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

    def from_response_property(self, metadata_property):
        """
            Maps a metadata property from a response. At
            this point it basically defaults immutable if it is
            not there.

            Args:
                metadata_property(dict)

            Returns:
                dict
        """
        mapped_metadata_property = deepcopy(metadata_property)

        # Defaulting immutable
        if mapped_metadata_property.get("immutable") is None:
            mapped_metadata_property["immutable"] = False

        # Grabbing only the values we care about.
        mapped_metadata_property = self.create_cloud_property(
            mapped_metadata_property["value"],
            mapped_metadata_property["immutable"]
        )

        return mapped_metadata_property

    def from_response(self, metadata):
        """
            Maps bulk metadata from response.

            Args:
                metadata(Dict{dict})

            Returns:
                Dict{dict}
        """
        mapped_metadata = deepcopy(metadata)

        for key in mapped_metadata:
            mapped_metadata[key] = self.from_response_property(mapped_metadata[key])

        return mapped_metadata
