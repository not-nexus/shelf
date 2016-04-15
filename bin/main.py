#!/usr/bin/env python
from pyshelf.app import app
from pyshelf.configure import configure_app
configure_app(app)

if __name__ == "__main__":
    app.run(port=8080)
