import logging
import utils

class RequestLogFilter(logging.Filter):
    def filter(self, record):
        container = utils.get_container()
        record.url = ""
        record.request_id = ""

        if container:
            record.url = "- %s " % container.request.url
            record.request_id = "- %s " % container.request_id

        return True
