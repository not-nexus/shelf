from boto.s3.connection import S3Connection
from boto.s3.key import Key
import re
import ast
from pyshelf.cloud.stream_iterator import StreamIterator
import pyshelf.cloud.metadata_mapper as meta_mapper 
from pyshelf.cloud.cloud_exceptions import \
    ArtifactNotFoundError, BucketNotFoundError, DuplicateArtifactError, InvalidNameError, MetadataNotFoundError


class Storage(object):
    def __init__(self, access_key, secret_key, bucket_name, logger):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.logger = logger

    def connect(self):
        self.logger.debug("Attempting to establish connection")
        self.conn = S3Connection(self.access_key, self.secret_key)

    def close(self):
        self.logger.debug("Closing connection")
        self.conn.close()

    def get_artifact(self, artifact_name):
        """
            Returns an object that can be used as a generator.
            This should be used when streaming large files
            directly to the client.

            http://technology.jana.com/2015/03/12/using-flask-and-boto-to-create-a-proxy-to-s3/

            Args:
                artifactName(basestring): Full path to an object that you wish
                    to download.

            Returns:
                pyshelf.cloud.stream_iterator.StreamIterator: A object that
                    implements a generator interface so can be passed
                    directly into a response so long as the framework supports it.
        """
        key = self._get_key(artifact_name)
        self.logger.debug(
            "Creating instance of pyshelf.cloud.stream_iterator.StreamIterator. Artifact {}".format(artifact_name))
        stream = StreamIterator(key)
        return stream

    def upload_artifact(self, artifact_name, fp):
        """
            Uploads an artifact. If directory does not exist in path it will be created.

            Args:
                artifact_name(basestring): Full path to upload artifact to
                fp(file): File to be uploaded

        """
        a = "/{}".format(artifact_name)
        match = re.search('\/_', a)
        if match:
            raise InvalidNameError(artifact_name)
        bucket = self._get_bucket(self.bucket_name)
        if bucket.get_key(artifact_name) is not None:
            raise DuplicateArtifactError(artifact_name)
        key = Key(bucket, artifact_name)
        self.logger.debug("Commencing upload of {}".format(artifact_name))
        key.set_contents_from_file(fp)

    def delete_artifact(self, artifact_name):
        key = self._get_key(artifact_name)
        key.delete()

    def get_artifact_as_string(self, path):
        """
            Just gets the content of the artifact instead of
            streaming it to a file pointer.  This shouldn't
            be used unless artifact is small enough to easily
            fit into memory

            Arguments:
                path(basestring): The path to the artifact you want to get.
        """
        key = self._get_key(path)
        return key.get_contents_as_string()

    def get_artifact_metadata(self, path):
        """
            Gets artifact metadata.

            Args:
                path(basestring): Full path to artifact.
            Returns:
                list: returns a list of metadata that is parsed by MetadataMapper.
        """
        key = self._get_key(path)
        return meta_mapper.format_for_client(key.metadata)

    def get_artifact_metadata_item(self, path, item):
        """
            Gets item from artifact metadata.

            Args:
                path(basestring): Full path to artifact.
                item(basestring): Key of the metadata item.
            Returns:
                list: returns metadata item.
        """
        key = self._get_key(path)
        meta = key.get_metadata(item)
        if meta is None:
            raise MetadataNotFoundError(item)
        return meta_mapper.format_for_client(meta)

    def set_artifact_metadata(self, path, meta):
        """
            Sets artifact metadata.

            Args:
                path(basestring): Full path to artifact.
                meta(list): List of metadata to set on artifact.
        """
        key = self._get_key(path)
        self._update_meta(key, meta)

    def set_metadata_item(self, path, item, meta, overwrite):
        """
            Sets an item in artifact metadata.

            Args:
                path(basestring): Full path to artifact.
                item(basestring): Key of the metadata item.
                meta(dict): Metadata
                overwrite(boolean): Whether or not to overwrite
                                    metadata if it is not immutable.
            Returns:
                Boolean value which denotes whether the item was created
                or not.
        """
        key = self._get_key(path)
        meta_item = key.get_metadata(item)
        create = meta_item is None
        if overwrite:
            self._update_meta(key, meta)
        else:
            if create:
                self._update_meta(key, meta)
        return create

    def delete_metadata_item(self, path, item):
        """
            Deletes an item from artifact metadata.

            Args:
                path(basestring): Full path to artifact.
                item(basestring): Key of the metadata item.
        """
        key = self._get_key(path)
        meta_item = key.get_metadata(item)
        if meta_item is None:
            raise MetadataNotFoundError(item)
        else:
            meta_item = ast.literal_eval(meta_item)
            immutable = meta_item.get("immutable")
            if not immutable:
                meta = key.metadata
                del meta[item]
                self._set_meta(key, meta)

    def _get_etag(self, key):
        meta = meta_mapper.get_hash(key.etag[1:-1])
        return meta
    
    def _set_meta(self, key, meta):
        key.metadata.update(meta)
        key2 = key.copy(self.bucket_name, key.name, meta, preserve_acl=True)
        key = key2
                
    def _update_meta(self, key, meta):
        meta = meta_mapper.update_meta(meta, key.metadata)
        key.metadata.update(meta)
        key2 = key.copy(self.bucket_name, key.name, meta, preserve_acl=True)
        key2.metadata = key.metadata
        key = key2
    
    def _get_key(self, artifact_name):
        bucket = self._get_bucket(self.bucket_name)
        self.logger.debug("Attempting to get artifact {}".format(artifact_name))
        key = bucket.get_key(artifact_name)
        if key is None:
            self.logger.error("Artifact {} does not exist in bucket {}".format(artifact_name, self.bucket_name))
            raise ArtifactNotFoundError(artifact_name)
        return key

    def _get_bucket(self, bucket_name):
        self.logger.debug("Attempting to get bucket {}".format(bucket_name))
        bucket = self.conn.lookup(self.bucket_name)
        if bucket is None:
            self.logger.error("Bucket {} does not exist".format(bucket_name))
            raise BucketNotFoundError(bucket_name)
        return bucket

    def __enter__(self):
        """ For use in "with" syntax"""
        self.connect()
        return self

    def __exit__(self, exception_type, exception, traceback):
        """ For use in "with" syntax"""
        self.close()
        return False
