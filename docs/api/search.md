Search
======

###pyshelf api supports searching artifact metadata which will return a link header for each search result.

####Searching requires a POST request with criteria (schemas/search-request-criteria). The following is an explantation of search criteria.
####Note:
    * The only requirement is the search portion of the criteria.

####Search criteria:
    * We currently support equality, wildcard, and version searches.
    * Equality search syntax: `"field=value"`
    * Wildcard search syntax: `"field=valu*"` where the `*` represents the 0 or more characters and can be placed anywhere left of operator.
    * Version search syntax: `"field~=1.1"` where search results >= 1.1 but < 2. Another example: `"field~=1.1.2"` results >= 1.1.2 but < 1.2
    * We support escaping special characters. Ex. `"field\~=value"` or `"field=valu\*" or even `"fi\~\=eld=val\=ue"` All searches would be equality searches.

####Sort criteria:
    * We support sort types and sort flags.
    * Sort types supported are ASC and DESC (with aliases ASCENDING and DESCENDING respectively).
    * Sort flag supported is VERSION (with alias VER).
    * This version flag uses distutils.version.LooseVersion library (where 1.19 > 1.2). [distutils.version](https://docs.python.org/2/distutils/apiref.html#module-distutils.version)
    * The sort criteria must start with the field name and be followed by sort flags and sort type.
    * The default sort type is ascending. If multiple sort types are supplied the last one will be used.
    * With multi-sorts the first sort takes precedence and the following sorts only take effect when a tie on the first sort occurs.

####Limit:
    * A limit can be set on the number of results returned back by the api.
    * Note: the method of sort effects which artifacts are contained within the limit.

####Artifact Path:
    * This api exposes two search endpoints.
        * Search from the root of an S3 bucket:  **/<bucket-name>/artifact/\_search**
        * Search from a partial path: **/<bucket-name>/artifact/<path>/\_search**
    * Both endpoints contain an implicit search. Ex. `"artifactPath=/bucket-name/artifact/\*"` or `"artifactPath=/bucket-name/artifact/path\*"`
        * Take note of the wildcard character. The partial path search will be recursive.
    * artifactPath is a default portion of an artifacts metadata which is always searched.

#### Example of criteria with single search and sort with a limit on number of results.

    {
        "search": "version=1.*",
        "sort": "version, VERSION",
        "limit": 1
    }

#### Example of criteria with multiple searches and sorts.
    {
        "search": [
            "version~=1.1",
            "bob=bob"
        ],
        "sort": [
            "version, VERSION, ASC",
            "bob, DESC"
        ]
    }


The following is an example of a simple search request that will search the root of the S3 bucket. We are also sorting the results by the artifact path.

    POST /bucket-name/artifact/_search
    Authorization: supersecrettoken

    {
        "search": "artifactName=test",
        "sort": "version, VERSION",
    }

We are searching for any artifact named test in the requested bucket. Here is the response:

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: /bucket-name/artifact/test; rel=child; title=test
    Link: /bucket-name/artifact/dir/test; rel=child; title=dir/test
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT

Here is an example of a search with multiple sort criteria.

    POST /bucket-name/artifact/application-dir/_search
    Authorization: supersecrettoken

    {
        "search": "version~=1.1",
        "sort": [
            "version, VERSION, DESC",
            "buildNumber, DESC"
        ]
    }

I want to point out the sort will give us a link to the highest verion and with the highest build number first.
* We will assume the following about these artifacts in the response:
    * Artifact "a" is version=1.19 & buildNumber=25
    * Artifact "b" is version=1.19 & buildNumber=24
    * Artifact "c" is version=1.1 & buildNumber=100
    * Artifact "d" is version=1.1 & buildNumber=99

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: /bucket-name/artifact/application-dir/a; rel=child; title=application-dir/a
    Link: /bucket-name/artifact/application-dir/b; rel=child; title=application-dir/b
    Link: /bucket-name/artifact/application-dir/c; rel=child; title=application-dir/c
    Link: /bucket-name/artifact/application-dir/d; rel=child; title=application-dir/d
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT
