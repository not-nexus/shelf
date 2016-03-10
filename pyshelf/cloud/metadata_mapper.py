from pyshelf.cloud.cloud_exceptions import MetadataNotFoundError, ImmutableMetadataError
import os
import yaml
import copy


class MetadataMapper(object):
    def __init__(self, container, artifact_path):
        self.container = container
        self.path = None
        self._metadata = self._load_metadata(artifact_path)

    def set_metadata(self, data, key=None):
        """
            Sets metadata item or entire metadata.

            Args:
                data(dict): Metadata to set.
                key(basestring)=None: Key of item to set.
        """
        if key:
            if not self._is_immutable(key):
                self._metadata[key] = data
        else:
            self._update_metadata(data)
        self._write_metadata()

    def create_metadata_item(self, data, key):
        """
            Creates metadata item if it doesn't exist.

            Args:
                data(dict): Metadata to set.
                key(basestring): Key of item to set.

            Return:
                boolean: Whether created or not
        """
        if not self._metadata.get(key):
            self._metadata[key] = data
            self._write_metadata()
            return True

        return False

    def item_exists(self, key):
        """
            Checks if item is in metadata.

            Args:
                key(basestring): Key of item.
        """
        return key in self._metadata

    def get_metadata(self, key=None):
        """
            Gets entire metadata set or specific item.

            Args:
                key(basestring)=None: Key of item to return.

            Returns:
                dict: returns entire metadata set or specific item
                      from set.
        """
        if key:
            item = self._metadata.get(key)

            if not item:
                raise MetadataNotFoundError(key)
            return item
        else:
            return self._metadata

    def remove_metadata(self, key):
        """
            Removes mutable metadata.

            Args:
                key(basestring): Key of item to remove.
        """
        if not self._is_immutable(key):
            del self._metadata[key]
        self._write_metadata()

    def _update_metadata(self, data):
        """
            Updates mutable metadata and ignores immutable.
        """
        old_meta = copy.deepcopy(self._metadata)
        for key, val in old_meta.iteritems():
            new_meta = data.get(key)

            if new_meta:
                if not self._is_immutable(key, quiet=True):
                    self._metadata[key] = new_meta
                data.pop(key)
            else:
                if not self._is_immutable(key, quiet=True):
                    del self._metadata[key]

        if len(data) > 0:
            self._metadata.update(data)

    def _write_metadata(self):
        if self._metadata:
            meta = copy.deepcopy(self._metadata)
            meta.pop("md5Hash", None)
            with self.container.create_master_bucket_storage() as storage:
                yaml.add_representer(unicode, lambda dumper,
                        value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))
                storage.set_artifact_from_string(self.path, yaml.dump(self._metadata, default_flow_style=False))

    def _load_metadata(self, artifact_path):
        """
            Loads entirety of metadata for an artifact which can be accessed
            via MetadataMapper.get_metadata(). To access a particular part of
            the metadata MetadataMapper.get_metadata(<key>).
        """
        path, artifact_name = os.path.split(artifact_path)
        meta_name = self._format_name(artifact_name)
        self.path = "{}/{}".format(path, meta_name)
        meta = None

        with self.container.create_master_bucket_storage() as storage:
            if storage.artifact_exists(self.path):
                raw_meta = storage.get_artifact_as_string(self.path)
                meta = yaml.load(raw_meta)

            if not meta:
                meta = {}

            meta["md5Hash"] = self._format_hash(storage.get_etag(artifact_path))
            return meta

    def _format_hash(self, etag):
        meta = {
            "name": "md5Hash",
            "value": etag,
            "immutable": True
        }
        return meta

    def _is_immutable(self, key, quiet=False):
        item = self._metadata.get(key)
        if item and item["immutable"]:
            if quiet:
                return True
            raise ImmutableMetadataError(key)
        else:
            return False

    def _format_name(self, name):
        """ Central spot for metadata file name format. """
        return "_metadata_{}.yaml".format(name)

    def __getattr__(self, key):
        """ Not sure that this makes sense for this object. """
        if key not in self._metadata.keys():
            raise MetadataNotFoundError(key)

        return self._metadata[key]
