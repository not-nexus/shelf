from pyshelf.cloud.storage import Storage

class Factory(object):
    def __init__(self, config):
        self.config = config

    def create_storage(self, bucket_name):
        c = self.config
        # Although bucketName exists in the config provided it is not
        # required and is not used because we want the ability to change
        # buckets when we want.
        return Storage(c["accessKey"], c["secretKey"], bucket_name)
