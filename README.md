pyshelf
=======

[![Build Status](https://travis-ci.org/kyle-long/pyshelf.svg?branch=master)](https://travis-ci.org/kyle-long/pyshelf)
[![codecov.io](https://codecov.io/github/kyle-long/pyshelf/coverage.svg?branch=master)](https://codecov.io/github/kyle-long/pyshelf?branch=master)

A REST API for AWS S3 meant to be an interface to immutable artifact storage.

It is suggested that you use [gunicorn](http://gunicorn.org/) for running in production but we provide a simple script to run it
for development purposes in `bin/main.py`.

Current Support
---------------

We are still in heavy development. You can see a full list of support in [docs](docs/README.md)

Configuration
-------------

It is required that a config.yaml exist in the root of the repository.  This will provide information for connecting to AWS.

Note:
* The bucket reference name acts as an alias for referencing the bucket. If a reference name is added it must be used to reference the bucket.
* If you are using Elasticsearch via AWS the region portion of the Elasticsearch config is required and the AWS keys are only required when the Elasticsearch Domain access policy requires keys.
* `upperSearchResultLimit` is another optional Elasticsearch config option. It defaults to 10000 if not set. It limits the number of search results returned. We currently do not support pagination.

        buckets:
            -
                name: bucket-name
                referenceName: bn
                accessKey: XXXXXXXXXXXXXXXXXXXX
                secretKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            -
                name: bucket_name_2
                accessKey: XXXXXXXXXXXXXXXXXXXX
                secretKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        elasticsearch:
            connectionString: http://localhost:9200/index
            region: us-east-1
            accessKey: XXXXXXXXXXXXXXXXXXXX
            secretKey: XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
            upperSearchResultLimit: 50000

Permissions
-----------

The API uses basic access authentication which requires an `Authorization` header with a token.

The API will look in the requested bucket for a directory at the root of the bucket named `_keys`.
It will then search for a file with the name of the token that was supplied. The permissions are stored in this file in YAML format.

Example

We are attempting to get artifact named test from test-bucket with token 12345

    curl -H "Authorization: 12345" shelf.example.com/test-bucket/artifact/test

The API will look for the following file:

    test-bucket/_keys/12345

The permissions are as follows:

    name: John Doe
    token: 12345
    write:
        - "/**"
    read:
        - "/**"

As you can see this individual is granted access as they have full read and write access.
You can also grant specific access using the following glob syntax.

    -"/test/*"
    -"/test/file"


Development
-----------

Clone the repository.  Then source utils/init-environment

     source utils/init-environment

This will install a virtualenv in `venv` and install all required dependencies.  It will also add the root of the repository to $PYTHONPATH
enabling you to run commands from there.

Then you can run main.py to test changes with

     ./bin/main.py

Testing
-------

Running the functional and unit tests requires a local running instance of Elasticsearch. Our test base points to localhost:9200 for Elasticsearch.

Note: We have developed towards Elasticsearch 1.5.2 as that is the version AWS utilizes.

To run the tests:

    pyproctor

To run the tests with a coverage report:

    pyproctor --coverage --source=pyshelf/

Currently we run some manual tests when a new version is deployed. Examples:
* Run all standard operations. Simple upload and download. Put bulk metadata and item. Get the metadata and metadata property. Then finally we search on the metadata.

* Run large file upload (we prefer to do this from the same availability zone and region as our API)

        dd if=/dev/urandom of=random.img count=1024 bs=5M
        curl -H "Authorization: XXXX" -F "file=@./random.img" api.shelf.example.com/bucket/artifact/random.img

* Run upload and abruptly cancel mid-upload
