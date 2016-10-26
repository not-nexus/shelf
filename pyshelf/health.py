from pyshelf.health_status import HealthStatus


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
        all_list = [x["referenceName"] for x in self.config["buckets"]]

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

    def get_status(self):
        """
            Determines the HealthStatus based off of some rules defined here.

            1. Status is CRITICAL if search is not working or if we cannot
            connect to 20% or more of the storages.
            2. Status is WARNING if we cannot connect to less than 20% of buckets
            but more than 0%.
            3. Status is OK otherwise.
        """
        status = HealthStatus.OK
        failing_list = self.get_failing_ref_name_list()
        all_list = self._get_ref_name_list()

        failing_count = len(failing_list)

        percent_failing = float(failing_count) / float(len(all_list)) * 100

        if percent_failing > 0 and self.elasticsearch:
            if percent_failing < 20:
                status = HealthStatus.WARNING
            else:
                status = HealthStatus.CRITICAL
        elif not self.elasticsearch:
            status = HealthStatus.CRITICAL

        return status
