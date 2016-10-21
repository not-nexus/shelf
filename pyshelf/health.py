class Health(object):
    """
        Responsible for storing and analyzing the health of the
        API.
    """
    def __init__(self):
        self.refNames = {}
        self.elasticsearch = True

    def get_failing_ref_name_list(self):
        """
            Finds all the reference names that we are unable to
            connect to.

            Returns:
                List(basestring)
        """
        failing = []
        for name, passing in self.refNames.iteritems():
            if not passing:
                failing.append(name)

        return failing
