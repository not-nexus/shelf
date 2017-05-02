import multiprocessing


class Runner(object):
    """
        Responsible for creating processes that will take care of
        updating the search index per bucket.
    """
    def __init__(self, container, search_update_function):
        """
            Args:
                container(shelf.bulk_update.container.Container)
        """
        self.container = container
        self.config = container.config
        self.search_update_function = search_update_function

    def run(self, requested_bucket_list=None):
        """
            Kicks off the process of running updates for the buckets
            provided.  If a bucket_list is not provided it is assumed
            you would like all buckets to be updated.

            Args:
                requested_bucket_list(List(basestring)): Each item being
                    the name of a bucket.
        """
        bucket_list = self._find_bucket_list(requested_bucket_list)
        for bucket_config in bucket_list:
            bucket_config.update({
                "elasticsearch": self.config["elasticsearch"],
                "logLevel": self.config["logLevel"],
                "chunkSize": self.config["chunkSize"],
                "bulkUpdateLogDirectory": self.config["bulkUpdateLogDirectory"]
            })
            self.container.logger.info("Starting process for bucket {0}".format(bucket_config["referenceName"]))
            self._run_process(bucket_config)

    @property
    def all_bucket_list(self):
        return self.config["buckets"]

    def _run_process(self, config):
        """
            This method exists mostly for mocking.
        """
        process = multiprocessing.Process(target=self.search_update_function, args=(config,))
        process.start()

    def _find_bucket_list(self, requested_bucket_list=None):
        bucket_list = []
        for bucket in self.all_bucket_list:
            # This is because I would like the bucket data to be in a particular
            # format
            if not requested_bucket_list or bucket["referenceName"] in requested_bucket_list:
                bucket_list.append(bucket)

        return bucket_list
