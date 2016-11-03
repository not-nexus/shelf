class StreamIterator(object):
    """
        Just a wrapper for the boto.s3.key.Key generator
        functionality.  This is to provide a clean interface
        so that replacing boto in the future would be easier.
    """
    def __init__(self, key):
        self.key = key
        self.key.open_read()

    def next(self):
        return self.key.next()

    def __iter__(self):
        return self

    @property
    def headers(self):
        return dict(self.key.resp.getheaders())
