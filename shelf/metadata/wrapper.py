class Wrapper(dict):
    """
        Simple wrapper for a dict that provides some
        extra functionaity.  This is NOT json serializable
        but it should be easy to convert to a regular
        dictionary with

        dict(wrapper)
    """
    def is_immutable(self, key):
        """
            Checks if the property is immutable.

            Args:
                key(basestring)

            Returns:
                boolean
        """
        item = self.get(key)
        if item and item["immutable"]:
            return True
        else:
            return False
