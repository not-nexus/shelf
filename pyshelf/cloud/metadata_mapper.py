from pyshelf.cloud.cloud_exceptions import MetadataNotFoundError
import os
import yaml


class MetadataMapper(object):
    def __init__(self, container, artifact):
        self.container = container
        self.artifact = artifact
        self.path = None
        self._metadata = self._load_metadata(self.artifact)

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
            self._metadata = self._update_metadata(data)
        self._write_metadata()

    def create_metadata_item(self, data, key):
        """
            Creates metadata item if it doesn't exist.

            Args:
                data(dict): Metadata to set.
                key(basestring): Key of item to set.
        """
        if not self._metadata.get(key):
            self._metadata[key] = data
            self._write_metadata()

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
        for key, val in self._metadata.iteritems():
            new_meta = data.get(key)

            if new_meta:
                if not self._is_immutable(key):
                    self._metadata[key] = new_meta
                data.pop(key)
            else:
                if not self._is_immutable(key):
                    del self._metadata[key]

        if len(data) > 0:
            self._metadata.update(data)

    def _write_metadata(self):
        if self._metadata:
            if self._metadata.get("md5Hash"):
                self._metadata.pop("md5Hash")
            with self.container.create_master_bucket_storage() as storage:
                storage.set_artifact_from_string(self.path, yaml.dump(self._metadata))


    def _load_metadata(self, artifact):
        """
            Loads entirety of metadata for an artifact which can be accessed
            via MetadataMapper.get_metadata(). To access a particular part of
            the metadata MetadataMapper.get_metadata(<key>).
        """
        path, artifact_name = os.path.split(artifact)
        meta_name = self._format_name(artifact_name)
        self.path = "{}/{}".format(path, meta_name)

        with self.container.create_master_bucket_storage() as storage:
            raw_meta = storage.get_artifact_as_string(self.path)
            meta = yaml.load(raw_meta)
            if meta:
                meta["md5Hash"] = self._format_hash(storage.get_etag(artifact))
                self.container.logger.debug("Loading metadata: {}".format(meta))
            else:
                meta = {}
                meta["md5Hash"] = self._format_hash(storage.get_etag(artifact))
                self.container.logger.debug("Metadata is empty. Adding file hash")
            return meta

    def _format_hash(self, etag):
        meta = {
                   "name": "md5Hash",
                   "value": etag,
                   "immutable": True
               }
        return meta

    def _is_immutable(self, key):
        item = self._metadata.get(key)
        if item:
            immutable = item["immutable"]
        else:
            immutable = False
        return immutable

    def _format_name(self, name):
        """ Central spot for metadata file name format. """
        return "_metadata_{}".format(name)

    def __getattr__(self, key):
        """ Not sure that this makes sense for this object. """
        if key not in self._metadata.keys():
            raise MetadataNotFoundError(key)

        return self._metadata[key]
