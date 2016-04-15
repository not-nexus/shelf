#!/usr/bin/env python
from pyshelf.app import app
from pyshelf import configure
configure.app(app)

if __name__ == "__main__":
    app.run(port=8080)
