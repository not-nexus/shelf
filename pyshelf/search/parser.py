class Parser(object):
    def from_request(self, request):
        """
            Turns the given request into search criteria that can be consumed by pyshelf.search module.

            Args:
                request(flask.Request): Raw search request.

            Returns:
                dict: search criteria that will be consumed by search layer
        """
        pass
