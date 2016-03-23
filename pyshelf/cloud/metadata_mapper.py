from pyshelf.cloud.cloud_exceptions import MetadataNotFoundError, ImmutableMetadataError
import os
import yaml
import copy

MD5_KEY = "md5Hash"
PATH_KEY = "artifactPath"
NAME_KEY = "artifactName"


class MetadataMapper(object):
    def __init__(self, container, artifact_path):
        self.container = container
        self.path = None
        self._metadata = None
        self.artifact_path = artifact_path

    @property
    def metadata(self):
        """
            Metadata is the dictionary that represents metadata for an artifact.
            An HTTP request is made via boto when this property is accessed for the
            first time.
        """
        if not self._metadata:
            self._metadata = self._load_metadata()

        return self._metadata

    def set_metadata(self, data, key=None):
        """
            Sets metadata item or entire metadata.

            Args:
                data(dict): Metadata to set.
                key(basestring)=None: Key of item to set.
        """
        if key:
            if not self._is_immutable(key):
                self.metadata[key] = data
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
        if not self.metadata.get(key):
            self.metadata[key] = data
            self._write_metadata()
            return True

        return False

    def item_exists(self, key):
        """
            Checks if item is in metadata.

            Args:
                key(basestring): Key of item.
        """
        return key in self.metadata

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
            item = self.metadata.get(key)

            if not item:
                raise MetadataNotFoundError(key)
            return item
        else:
            return self.metadata

    def remove_metadata(self, key):
        """
            Removes mutable metadata.

            Args:
                key(basestring): Key of item to remove.
        """
        if not self._is_immutable(key):
            del self.metadata[key]
        self._write_metadata()

    def _update_metadata(self, data):
        """
            Updates mutable metadata and ignores immutable.
        """
        old_meta = copy.deepcopy(self.metadata)
        for key, val in old_meta.iteritems():
            new_meta = data.get(key)

            if new_meta:
                if not self._is_immutable(key, quiet=True):
                    self.metadata[key] = new_meta
                data.pop(key)
            else:
                if not self._is_immutable(key, quiet=True):
                    del self.metadata[key]

        if len(data) > 0:
            self.metadata.update(data)

    def _write_metadata(self):
        if self.metadata:
            meta = copy.deepcopy(self.metadata)
            meta.pop(MD5_KEY, None)
            with self.container.create_bucket_storage() as storage:
                # safe_dump so it doesn't try to represent a python
                # object in yaml and only serializes native yaml
                # types.
                #
                # default_flow_style so that it doesn't try to stick
                # inline json for smaller objects.
                contents = yaml.safe_dump(
                    self.metadata,
                    encoding="utf-8",
                    indent=4,
                    default_flow_style=False
                )

                storage.set_artifact_from_string(self.path, contents)

    def _load_metadata(self):
        """
            Loads entirety of metadata for an artifact which can be accessed
            via MetadataMapper.get_metadata(). To access a particular part of
            the metadata MetadataMapper.get_metadata(<key>).
        """
        path, artifact_name = os.path.split(self.artifact_path)
        meta_name = self._format_name(artifact_name)
        self.path = "{}/{}".format(path, meta_name)
        meta = None

        with self.container.create_bucket_storage() as storage:
            if storage.artifact_exists(self.path):
                raw_meta = storage.get_artifact_as_string(self.path)
                meta = yaml.load(raw_meta)

            if not meta:
                meta = {}

            meta[MD5_KEY] = self._format_hash(storage.get_etag(self.artifact_path))

            if PATH_KEY not in meta:
                meta[PATH_KEY] = self._format(PATH_KEY, self.artifact_path, True)

            if NAME_KEY not in meta:
                meta[NAME_KEY] = self._format(NAME_KEY, artifact_name, True)

            return meta

    def _format_hash(self, etag):
        return self._format(MD5_KEY, etag, True)

    def _format(self, key, value, immutable):
        """
            Formats a metadata item.
        """
        return {
            "name": key,
            "value": value,
            "immutable": immutable
        }

    def _is_immutable(self, key, quiet=False):
        item = self.metadata.get(key)
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
        if key not in self.metadata.keys():
            raise MetadataNotFoundError(key)

        return self.metadata[key]
