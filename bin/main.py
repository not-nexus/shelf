#!/usr/bin/env python
from pyshelf.app import app
import pyshelf.configure as configure
import os

if __name__ == "__main__":
    config_path = os.path.dirname(os.path.realpath(__file__)) + "/../config.yaml"
    configure.app(app, config_path)
    log_level_name = app.config.get("logLevel", "DEBUG")
    configure.logger(app.logger, log_level_name)
    app.run(port=8080)
