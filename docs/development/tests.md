Testing
=======

Running the functional and unit tests requires a local running instance of Elasticsearch. Our test base points to localhost:9200 for Elasticsearch.

Note: We have developed towards Elasticsearch 5.1 as that is currently the latest version AWS utilizes.

To run the tests:

    pyproctor

To run the tests with a coverage report:

    pyproctor --coverage --source=shelf/

Currently we run some manual tests when a new version is deployed. Examples:
* Run all standard operations. Simple upload and download. Put bulk metadata and item. Get the metadata and metadata property. Then finally we search on the metadata.

* Run large file upload (we prefer to do this from the same availability zone and region as our API)

        dd if=/dev/urandom of=random.img count=1024 bs=5M
        curl -H "Authorization: XXXX" -F "file=@./random.img" api.shelf.example.com/bucket/artifact/random.img

* Run upload and abruptly cancel mid-upload
