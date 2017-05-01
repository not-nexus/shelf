Testing
=======

Running the functional and unit tests requires a local running instance of Elasticsearch. Our test base points to localhost:9200 for Elasticsearch.

Install Elasticsearch
---------------------

We have developed towards Elasticsearch 5.1.1 as that is currently the latest version AWS utilizes.


#### Install as Service on Debian System

    curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.1.1.deb && sudo dpkg -i --force-confnew elasticsearch-5.1.1.deb && sudo service elasticsearch restart

[Or simply download Elasticsearch 5.1.1](https://www.elastic.co/downloads/past-releases/elasticsearch-5-1-1)


Run Tests
---------

    pyproctor

    # Run tests with a coverage report.
    pyproctor --coverage --source=shelf/


Other Tests
-----------

For our particular implementation of Shelf we have a utility for running functional test, which can be found [here](https://github.com/connected-world-services/shelf-functional-tests).

