import logging
import sys
from pyshelf.request_log_filter import RequestLogFilter
import yaml


def app_config(existing_config, config_path):
    with open(config_path, "r") as f:
        content = f.read()
        config = yaml.load(content)

    if not config.get("buckets"):
        raise ValueError("config.yaml requires buckets heading for list of buckets with associated keys.")

    for key, val in config.get("buckets").iteritems():
        required = {
            "accessKey": val.get("accessKey"),
            "secretKey": val.get("secretKey")
        }
        _validate_dict(required)

    required = {"elasticSearchConnectionString": config.get("elasticSearchConnectionString")}
    _validate_dict(required)

    existing_config.update(config)


def _validate_dict(required):
    if not all(required.values()):
        raise ValueError("config.yaml did not have all required settings: " + ", ".join(required.keys()))


def logger(logger, log_level_name):
    log_level_name = log_level_name.upper()
    log_level = logging.getLevelName(log_level_name)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s %(user)s%(request_id)s%(url)s- %(message)s")
    handler.setFormatter(formatter)
    handler.addFilter(RequestLogFilter())
    logger.addHandler(handler)
    logger.setLevel(log_level)
