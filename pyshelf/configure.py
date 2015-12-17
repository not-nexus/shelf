import logging
import sys
from pyshelf.request_log_filter import RequestLogFilter
import yaml


def app(app):
    with open("config.yaml", "r") as f:
        content = f.read()
        config = yaml.load(content)

    required = {
        "accessKey": config.get("accessKey"),
        "secretKey": config.get("secretKey"),
        "bucketName": config.get("bucketName")
    }

    if not all(required.values()):
        raise ValueError("config.yaml did not have all required settings: " + ", ".join(required.keys()))

    app.config.update(config)


def logger(logger, log_level_name):
    log_level_name = log_level_name.upper()
    log_level = logging.getLevelName(log_level_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s %(request_id)s%(url)s- %(message)s")
    handler.setFormatter(formatter)
    handler.addFilter(RequestLogFilter())
    logger.addHandler(handler)
    logger.setLevel(log_level)
