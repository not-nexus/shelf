from pyshelf.cloud.storage import Storage
from pyshelf import utils
from pyshelf.cloud.cloud_exceptions import BucketConfigurationNotFound


class Factory(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def create_storage(self, bucket_name):
        # Although bucketName exists in the config provided it is not
        # required and is not used because we want the ability to change
        # buckets when we want.
        bucket_config = utils.get_bucket_config(self.config, bucket_name)
        if bucket_config is None:
            self.logger.warning("Access keys for {0} are not in your config.".format(bucket_name))
            raise BucketConfigurationNotFound(bucket_name)

        storage = Storage(bucket_config["accessKey"], bucket_config["secretKey"], bucket_name, self.logger)

        return storage
