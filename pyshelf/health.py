class Health(object):
    """
        Responsible for storing and analyzing the health of the
        API.
    """
    def __init__(self, config):
        """
            Args:
                config(schemas/config.json) Must conform to schema with one additional rule:
                    refName is required to be set.
        """
        self.config = config
        self.refNames = {}
        self.elasticsearch = True

    def _get_ref_name_list(self):
        all_list = [x["refName"] for x in self.config["buckets"]]

        return all_list

    def get_failing_ref_name_list(self):
        """
            Finds all the reference names that we are unable to
            connect to.

            Returns:
                List(basestring)
        """
        ref_name_list = []
        for name, passing in self.refNames.iteritems():
            if not passing:
                ref_name_list.append(name)

        return ref_name_list

    def get_passing_ref_name_list(self):
        """
            Finds ALL passing reference names (representing storage for artifacts).

            This function is optimistic and will assume that buckets that have not
            yet been accessed are also passing.

            Returns:
                List(basestring)
        """
        failing_list = self.get_failing_ref_name_list()
        all_list = self._get_ref_name_list()
        passing_set = set(all_list) - set(failing_list)

        # So that everything returns a list.
        return list(passing_set)
