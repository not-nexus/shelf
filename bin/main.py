#!/usr/bin/env python
from pyshelf.app import app
import pyshelf.configure as configure

if __name__ == "__main__":
    configure.app(app)
    log_level_name = app.config.get("logLevel", "DEBUG")
    configure.logger(app.logger, log_level_name)
    app.run(port=8080)
