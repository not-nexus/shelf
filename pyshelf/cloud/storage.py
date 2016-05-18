from boto.s3.connection import S3Connection
from boto.s3.key import Key
from pyshelf.cloud.stream_iterator import StreamIterator
from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError, BucketNotFoundError, DuplicateArtifactError


class Storage(object):
    def __init__(self, access_key, secret_key, bucket_name, logger):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.logger = logger
        self.key_map = {}

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
                artifactName(string): Full path to an object that you wish
                    to download.

            Returns:
                pyshelf.cloud.stream_iterator.StreamIterator: A object that
                    implements a generator interface so can be passed
                    directly into a response so long as the framework supports it.
        """
        key = self._get_key(artifact_name)
        self.logger.debug(
            "Creating instance of pyshelf.cloud.stream_iterator.StreamIterator. Artifact {0}".format(artifact_name))
        stream = StreamIterator(key)
        return stream

    def upload_artifact(self, artifact_name, file_storage):
        """
            Uploads an artifact. If directory does not exist in path it will be created.

            Args:
                artifact_name(string): Full path to upload artifact to.
                file_storage(werkzeug.datastructures.FileStorage): File to be uploaded.

        """
        bucket = self._get_bucket(self.bucket_name)

        if bucket.get_key(artifact_name) is not None:
            raise DuplicateArtifactError(artifact_name)

        key = Key(bucket, artifact_name)
        self.logger.debug("Commencing upload of {0}".format(artifact_name))
        key.set_contents_from_file(file_storage)

    def get_artifact_as_string(self, path):
        """
            Just gets the content of the artifact instead of
            streaming it to a file pointer.  This shouldn't
            be used unless artifact is small enough to easily
            fit into memory

            Arguments:
                path(string): The path to the artifact you want to get.
        """
        key = self._get_key(path)
        return key.get_contents_as_string()

    def set_artifact_from_string(self, path, data):
        """
            Creates or updates artifact from a string.

            Args:
                path(string): The path to the artifact to update/create.
                data(string): Data to set contents of artifact from.
        """
        try:
            key = self._get_key(path)
        except ArtifactNotFoundError:
            bucket = self._get_bucket(self.bucket_name)
            key = Key(bucket, path)
        key.set_contents_from_string(data)

    def get_etag(self, path):
        """
            Gets md5Hash of file.

            Args:
                path(string): The path to the artifact.

            Returns:
                string: md5Hash of artifact.
        """
        key = self._get_key(path)
        return key.etag[1:-1]

    def get_directory_contents(self, path, recursive):
        """
            Gets the contents of a directory.

            Args:
                path(string): The path of the directory.
                recursive(boolean):

            Returns:
                list of s3.boto.key.Key
        """
        if path == "/":
            path = ""

        if recursive:
            result_list = self._get_bucket(self.bucket_name).list(prefix=path)
        else:
            result_list = self._get_bucket(self.bucket_name).list(prefix=path, delimiter="/")

        keys = list(result_list)
        return keys

    def _get_key(self, artifact_name):
        if artifact_name in self.key_map:
            return self.key_map

        bucket = self._get_bucket(self.bucket_name)
        self.logger.debug("Attempting to get artifact {0}".format(artifact_name))
        key = bucket.get_key(artifact_name)
        if key is None:
            self.logger.error("Artifact {0} does not exist in bucket {0}".format(artifact_name, self.bucket_name))
            raise ArtifactNotFoundError(artifact_name)

        self.key_map[artifact_name] = key
        return key

    def _get_bucket(self, bucket_name):
        self.logger.debug("Attempting to get bucket {0}".format(bucket_name))
        bucket = self.conn.lookup(self.bucket_name)
        if bucket is None:
            self.logger.error("Bucket {0} does not exist".format(bucket_name))
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
