from pyshelf.metadata.wrapper import Wrapper
from pyshelf.metadata.result import Result
from pyshelf.metadata.error_code import ErrorCode
import copy


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
        self.update_manager = self.container.update_manager
        self.identity = self.container.resource_identity
        self.portal = self.container.bucket_container.cloud_portal
        self.initializer = self.container.bucket_container.initializer
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
            data = self.initializer.update(self.identity, data)
            self.portal.update(self.identity.cloud_metadata, data)

        return data

    def write(self):
        """
            Updates the cloud to contain the metadata set on this instance.
        """
        self.portal.update(self.identity.cloud_metadata, self.metadata)
        formatted_metadata = self.container.mapper.to_response(self.metadata)
        self.update_manager.update(self.identity.search, formatted_metadata)

    def try_update(self, data):
        """
            Overwrites the metadata with the data provided.  The only
            caveat is that if you try to set metadata that is immutable
            it will be ignored.

            Args:
                data(schemas/metadata.json)

            Returns:
                pyshelf.metadata.result.Result
        """
        self.container.mapper.from_response(data)
        old_meta = copy.deepcopy(self.metadata)
        for key, val in old_meta.iteritems():
            new_meta = data.get(key)

            if new_meta:
                if not self.metadata.is_immutable(key):
                    self.metadata[key] = new_meta
                data.pop(key)
            else:
                if not self.metadata.is_immutable(key):
                    del self.metadata[key]

        if len(data) > 0:
            self.metadata.update(data)

        # assuming success if it hasn't thrown an exception
        self.write()
        return Result()

    def try_update_property(self, key, value):
        """
            Updates a single metadata property

            Args:
                key(string)
                value(schemas/metadata-property.json)

            Returns:
                pyshelf.metadata.result.Result
        """
        result = Result()
        result = self._try_update_property_with_result(key, value, result)
        return result

    def try_create_property(self, key, value):
        """
            Creates a single metadata property.  Will error if the
            property already exists.

            Args:
                key(string)
                value(schemas/metadata-property.json)

            Returns:
                pyshelf.metadata.result.Result
        """
        result = Result()
        if self.metadata.get(key):
            result.add_error(ErrorCode.DUPLICATE)
        else:
            result = self._try_update_property_with_result(key, value, result)

        return result

    def try_delete_property(self, key):
        """
            Deletes a single metadata property.

            Args:
                key(string): Name of the metadata property

            Returns:
                pyshelf.metadata.result.Result
        """
        result = Result()
        if self.metadata.is_immutable(key):
            result.add_error(ErrorCode.IMMUTABLE)
        else:
            del self.metadata[key]
            self.write()

        return result

    def _try_update_property_with_result(self, key, value, result):
        if not self.metadata.is_immutable(key):
            self.container.mapper.from_response_property(value)
            self.metadata[key] = value
            self.write()
            result.value = value
        else:
            result.add_error(ErrorCode.IMMUTABLE)

        return result
