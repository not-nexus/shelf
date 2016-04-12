import logging
import sys
from pyshelf.request_log_filter import RequestLogFilter
import yaml


def app(app, config_path):
    with open(config_path, "r") as f:
        content = f.read()
        config = yaml.load(content)

    _validate_key("buckets", config)
    _validate_key("elasticsearch", config)
    _validate_key("connectionString", config.get("elasticsearch"))

    for key, val in config.get("buckets").iteritems():
        _validate_aws_keys(val)

    if config.get("aws"):
        _validate_aws_keys(config.get("elasticsearch"))
        _validate_key("region", config.get("elasticsearch").get("region"))

    app.config.update(config)


def _validate_aws_keys(config):
    required = {
        "accessKey": config.get("accessKey"),
        "secretKey": config.get("secretKey")
    }
    if not all(required.values()):
        raise ValueError("config.yaml did not have all required settings: " + ", ".join(required.keys()))

def _validate_key(key, config):
    if not config.get(key):
        raise ValueError("config.yaml requires {0} key.".format(key))


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
