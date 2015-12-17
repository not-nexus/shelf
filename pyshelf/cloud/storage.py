from boto.s3.connection import S3Connection
from boto.s3.key import Key
import os

class Storage(object):
    def __init__(self, accessKey, secretKey):
        self.accessKey = accessKey     
        self.secretKey = secretKey
        self.conn = S3Connection(self.accessKey, self.secretKey) 
        self.articlePath = os.path.expanduser('~') + '/tmp/'

    def get_artifact(self, bucketName, artifactName):
        bucket = self.conn.get_bucket(bucketName)
        key = bucket.get_key(artifactName)
        dir = self.articlePath + artifactName
        fp = open(dir, 'w+')
        key.get_file(fp)


    def upload_artifact(self, bucketName, artifactName, fp):
        bucket = self.conn.get_bucket(bucketName)           
        key = Key(bucket, artifactName)
        key.set_contents_from_file(fp)

    def delete_artifact(self, bucketName, artifactName):
        bucket = self.conn.get_bucket(bucketName)
        key = bucket.get_key(artifactName)
        key.delete()
