#!/usr/bin/env python
from shelf.app import app
from shelf import configure
configure.app(app)

if __name__ == "__main__":
    app.run(port=8080)
