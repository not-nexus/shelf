import yaml


class YamlCodec(object):
    def serialize(self, metadata):
        # safe_dump so it doesn't try to represent a python
        # object in yaml and only serializes native yaml
        # types.
        #
        # default_flow_style so that it doesn't try to stick
        # inline json for smaller objects.
        contents = yaml.safe_dump(
            metadata,
            encoding="utf-8",
            indent=4,
            default_flow_style=False
        )

        return contents

    def deserialize(self, metadata):
        metadata = yaml.load(metadata)
        return metadata
