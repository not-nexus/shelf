from shelf.cloud.storage import Storage
from shelf import utils
from shelf.cloud.cloud_exceptions import BucketConfigurationNotFound


class Factory(object):
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def create_storage(self, bucket_name):
        # Although bucketName exists in the config provided it is not
        # required and is not used because we want the ability to change
        # buckets when we want.
        bc = utils.get_bucket_config(self.config, bucket_name)

        if bc is None:
            self.logger.warning("Access keys for {0} are not in your config.".format(bucket_name))
            raise BucketConfigurationNotFound(bucket_name)

        storage = Storage(bc["accessKey"], bc["secretKey"], bc["name"], self.logger)

        return storage
