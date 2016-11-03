import logging
from shelf.get_container import get_container


class RequestLogFilter(logging.Filter):
    def filter(self, record):
        container = get_container()
        record.url = ""
        record.request_id = ""
        record.user = ""

        if container:
            record.url = "- {0} ".format(container.request.url)
            record.request_id = "- {0} ".format(container.request_id)
            record.user = "- {0} ".format(container.permissions_validator.name)

        return True
