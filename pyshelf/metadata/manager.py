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
        # TODO: Use this line when we have it
        # self.update_manager = self.container.search.update_manager
        self.identity = self.container.resource_identity
        self.portal = self.container.cloud_portal
        self.initializer = self.container.initializer
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
            self.portal.update(self.identity.cloud_metadata, data)

        return data

    def write(self):
        self.portal.update(self.identity.cloud_metadata, self.metadata)

    def try_update(self, data):
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
        return Result()

    def try_update_item(self, key, value):
        """
            Args:
                key(string)
                value(mixed)

            Returns:
                pyshelf.metadata.result.Result
        """
        result = Result()
        result = self._try_update_item_with_result(key, value, result)
        return result

    def try_create_item(self, key, value):
        """
            Args:
                key(string)
                value(mixed)

            Returns:
                pyshelf.metadata.result.Result
        """
        result = Result()
        if None is not self.metadata.get(key):
            result.add_error(ErrorCode.DUPLICATE)
        else:
            result = self._try_update_item_with_result(key, value, result)

        return result

    def try_delete_item(self, key):
        result = Result()
        if self.metadata.is_immutable(key):
            result.add_error(ErrorCode.IMMUTABLE)
        else:
            del self.metadata[key]
            self.write()

        return result

    def _try_update_item_with_result(self, key, value, result):
        if not self.metadata.is_immutable(key):
            self.metadata[key] = value
            self.write()
            result.value = value
        else:
            result.add_error(ErrorCode.IMMUTABLE)

        return result
