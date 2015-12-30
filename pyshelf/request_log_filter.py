import logging
import pyshelf.utils as utils


class RequestLogFilter(logging.Filter):
    def filter(self, record):
        container = utils.get_container()
        record.url = ""
        record.request_id = ""
        record.user = ""

        if container:
            record.url = "- {} ".format(container.request.url)
            record.request_id = "- {} ".format(container.request_id)
            record.user = "- {} ".format(container.permissions_validator.name)

        return True
