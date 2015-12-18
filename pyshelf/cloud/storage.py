from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
from pyshelf.cloud.stream_iterator import StreamIterator

class Storage(object):
    def __init__(self, access_key, secret_key, bucket_name):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.articlePath = os.path.expanduser('~') + '/tmp/'

    def connect(self):
        self.conn = S3Connection(self.access_key, self.secret_key)

    def close(self):
        self.conn.close()

    def get_artifact(self, artifact_name):
        key = self._get_key(artifact_name)
        dir = self.articlePath + artifactName
        fp = open(dir, 'w+')
        key.get_file(fp)

    def get_artifact_stream(self, artifact_name):
        """
            Returns an object that can be used as a generator.
            This should be used when streaming large files
            directly to the client.

            http://technology.jana.com/2015/03/12/using-flask-and-boto-to-create-a-proxy-to-s3/

            Args:
                bucketName(basestring): The name of the cloud storage bucket
                    (S3 right now) that we want to connect to
                artifactName(basestring): Full path to an object that you wish
                    to download.

            Returns:
                pyshelf.cloud.stream_iterator.StreamIterator: A object that 
                    implements a generator interface so can be passed 
                    directly into a response so long as the framework supports it.
        """
        key = self._get_key(artifact_name)
        stream = StreamIterator(key)
        return stream

    def upload_artifact(self, artifact_name, fp):
        bucket = self.conn.get_bucket(self.bucket_name)
        key = Key(bucket, artifact_name)
        key.set_contents_from_file(fp)

    def delete_artifact(self, artifact_name):
        bucket = self.conn.get_bucket(self.bucket_name)
        key = bucket.get_key(artifact_name)
        key.delete()

    def _get_key(self, artifact_name):
        bucket = self.conn.get_bucket(self.bucket_name)
        key = bucket.get_key(artifact_name)
        return key

    def __enter__(self):
        """ For use in "with" syntax"""
        self.connect()

    def __exit__(self, exception_type, exception, traceback):
        """ For use in "with" syntax"""
        # TODO : Properly handle exceptions.  For now they will
        # fly
        self.close()
        return False
