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
        self.portal = self.container.cloud_portal
        self._metadata = None

    @property
    def metadata(self):
        """
            Can be used like a dict

            Returns pyshelf.metadata.wrapper.Wrapper
        """
        if not self._metadata:
            data = self.load()
            self._metadata = Wrapper(data)

        return self._metadata

    def load(self):
        """
            Loads metadata from the cloud.

            Returns
                dict
        """
        data = self.portal.load(self.identity.cloud_metadata)
        if self.initializer.needs_update(data):
            data = self.initializer.update(data)
            self.cloud_portal.update(self.identity.cloud_metadata, data)

        return data
