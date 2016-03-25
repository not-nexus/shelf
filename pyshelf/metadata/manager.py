from pyshelf.metadata.wrapper import Wrapper


class Manager(object):
    """
        Responsible for maintaining metadata integrity between multiple
        places.  Not only should the metadata match but it also needs to
        be initialized with some values if it doesn't already exist.

        Although they should always match, the cloud storage is our
        source of truth.
    """
    def __init__(self, container):
        self.container = container
        # TODO: Use this line when we have it
        # self.update_manager = self.container.search.update_manager
        self.identity = self.container.resource_identity
        self.mapper = self.container.mapper
        self._metadata = None
        self.codec = self.container.yaml_codec

    @property
    def metadata(self):
        """
            Can be used like a dict

            Returns pyshelf.metadata.wrapper.Wrapper
        """
        if not self._metadata:
            self._metadata = Wrapper(self.load())

        return self._metadata

    def load(self):
        """
            Loads metadata from the cloud.

            Returns
                dict
        """
        with self.container.create_cloud_storage as storage:
            metadata_id = self.identity.cloud_metadata
            raw_meta = storage.get_artifact_as_string(metadata_id)
            meta = self.codec.deserialize(raw_meta)

            if not meta:
                meta = {}

            meta = self.mapper.to_response(meta)

        return meta
