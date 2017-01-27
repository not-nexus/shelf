Configuration
=============

A `config.yaml` file must exist at the root of the repository. See [the schema](../schemas/config.json) to find all possible properties and what they are used for.

Note:
* The bucket `referenceName` acts as an alias for referencing the bucket. If a `referenceName` is added it must be used to reference the bucket.
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
        hookCommand: ./your/script.sh
