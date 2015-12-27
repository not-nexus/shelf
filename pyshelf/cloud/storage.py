from boto.s3.connection import S3Connection
from boto.s3.key import Key
import re
from pyshelf.cloud.stream_iterator import StreamIterator
from pyshelf.cloud.cloud_exceptions import \
    ArtifactNotFoundError, BucketNotFoundError, DuplicateArtifactError, InvalidNameError, ImmutableMetaError


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
        self.logger.debug("Completed upload of {}".format(artifact_name))

    def delete_artifact(self, artifact_name):
        key = self._get_key(artifact_name)
        if key is None:
            raise ArtifactNotFoundError(artifact_name)
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
                metadata(dict) of artifact.
        """
        key = self._get_key(path)
        return key.metadata

    def set_artifact_meta(self, path, meta):
        """
            Sets artifact metadata.

            Args:
                path(basestring): Full path to artifact.
                meta(dict): Dictionary of metadata to set on artifact.
        """
        key = self._get_key(path)
        immutable = key.get_metadata("immutable")
        if immutable.to_lower() == "true":
            raise ImmutableMetaError()
        key.update_metadata(meta)

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
        # TODO : Properly handle exceptions.  For now they will
        # fly
        self.close()
        return False
