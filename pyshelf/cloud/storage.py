from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os
from pyshelf.cloud.stream_iterator import StreamIterator

class Storage(object):
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey     
        self.secretKey = secretKey
        self.conn = S3Connection(self.accessKey, self.secretKey) 
        self.articlePath = os.path.expanduser('~') + '/tmp/'

    def get_artifact(self, bucketName, artifactName):
        key = self._get_key(bucketName, artifactName)
        dir = self.articlePath + artifactName
        fp = open(dir, 'w+')
        key.get_file(fp)

    def get_artifact_stream(self, bucketName, artifactName):
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
        key = self._get_key(bucketName, artifactName)
        stream = StreamIterator(key)
        return stream

    def upload_artifact(self, bucketName, artifactName, fp):
        bucket = self.conn.get_bucket(bucketName)           
        key = Key(bucket, artifactName)
        key.set_contents_from_file(fp)

    def delete_artifact(self, bucketName, artifactName):
        bucket = self.conn.get_bucket(bucketName)
        key = bucket.get_key(artifactName)
        key.delete()

    def _get_key(self, bucketName, artifactName):
        bucket = self.conn.get_bucket(bucketName)
        key = bucket.get_key(artifactName)
        return key
