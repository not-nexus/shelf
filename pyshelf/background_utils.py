import logging


def configure_file_logger(name, filename, log_level):
    logger = logging.getLogger(name)
    handler = logging.FileHandler(filename)
    formatter = logging.Formatter(fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger
