from pyshelf.cloud.storage import Storage
from pyshelf.cloud.cloud_exceptions import CloudStorageException
from pyshelf.error_code import ErrorCode


class Factory(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def create_storage(self, bucket_name):
        c = self.config
        # Although bucketName exists in the config provided it is not
        # required and is not used because we want the ability to change
        # buckets when we want.
        if not c.get("buckets").get(bucket_name):
            raise CloudStorageException("Access keys for {0} are not in your config.".format(bucket_name),
                    ErrorCode.INTERNAL_SERVER)
        return Storage(c["buckets"][bucket_name]["accessKey"], c["buckets"][bucket_name]["secretKey"],
                bucket_name, self.logger)
