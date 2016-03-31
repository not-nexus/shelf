pyshelf
=======

[![Build Status](https://travis-ci.org/kyle-long/pyshelf.svg?branch=master)](https://travis-ci.org/kyle-long/pyshelf)
[![codecov.io](https://codecov.io/github/kyle-long/pyshelf/coverage.svg?branch=master)](https://codecov.io/github/kyle-long/pyshelf?branch=master)

A REST API for AWS S3 meant to be an interface to immutable artifact storage.

It is suggested that you use [gunicorn](http://gunicorn.org/) for running in production but we provide a simple script to run it
for development purposes in `bin/main.py`.

Current Support
---------------

We are still in heavy development. So far you are only able to upload and download artifacts.  You can see a full list of support
in [docs](docs/README.md)

Configuration
-------------

It is required that a config.yaml exist in the root of the repository.  This will provide information for connecting to AWS.

    buckets:
        bucket_name:
            accessKey: XXXXXXXXXXXXXXXXXXXX
            secretKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        bucket_name_2:
            accessKey: XXXXXXXXXXXXXXXXXXXX
            secretKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    elasticSearchHost:
        - localhost:9200

Development
-----------

Clone the repository.  Then source utils/init-environment

     source utils/init-environment

This will install a virtualenv in `venv` and install all required dependencies.  It will also add the root of the repository to $PYTHONPATH
enabling you to run commands from there.

In order for the Elasticsearch tests to run it requires a local running instance of Elasticsearch for integration testing.

Then you can run main.py to test changes with

     ./bin/main.py
