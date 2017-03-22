class StreamIterator(object):
    # 250MB
    BYTE_LOG_INCREMENT = 250000000
    """
        Just a wrapper for the boto.s3.key.Key generator
        functionality.  This is to provide a clean interface
        so that replacing boto in the future would be easier.
    """
    def __init__(self, key, logger):
        """
            Args:
                key(boto.s3.key.Key)
                logger(logging.Logger)
        """
        self.key = key
        self.logger = logger
        self.key.open_read()
        self.log_count = 0
        self.total_bytes = 0
        self.request_id = ""

    def next(self):
        byteList = self.key.next()
        self.total_bytes = self.total_bytes + len(byteList)

        if self.total_bytes / StreamIterator.BYTE_LOG_INCREMENT > self.log_count:
            self.logger.info("{0} - Downloading {1}/artifact/{2}: {3} bytes".format(
                self.request_id, self.key.bucket.name, self.key.name, self.total_bytes
            ))
            self.log_count = self.log_count + 1

        return byteList

    def __iter__(self):
        return self

    @property
    def headers(self):
        return dict(self.key.resp.getheaders())
