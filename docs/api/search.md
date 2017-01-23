Search
======

Our api supports searching artifact metadata which will return a link header for each search result.


Search criteria
---------------

* We currently support equality, wildcard, and version searches.
* Equality search syntax: `"field=value"`
* Wildcard search syntax: `"field=valu*"` where the `*` represents the 0 or more characters.
* Version search syntax: `"field~=1.1"` where search results >= 1.1 but < 2.


Escaping Special Characters
---------------------------

As you can see \*, ~, and = are special characters within search criteria. We support escaping of these characters for literal evaluation. These characters must be escaped with double backslashes to be valid JSON. Here is an example:

    {
        "search": "artifactPath=myOddPath\\*"
    }


Sort criteria
-------------

* We support sort types and sort flags.
* Sort types supported are ASC and DESC
    * with aliases ASCENDING and DESCENDING respectively
* Sort flag supported is VERSION (with alias VER).
* This version flag uses distutils.version.LooseVersion library (where 1.19 > 1.2).
    * More info: https://docs.python.org/2/distutils/apiref.html#module-distutils.version
* The sort criteria must start with the field name.
* The default sort type is ascending. If multiple sort types are given the last is used.
* With multi-sorts the first sort takes precedence.
* If a property that does not exist is sorted on it is treated as `None`.
    * Ex. if you sort on `buildNumber` and a result returned does not have a `buildNumber`
    metadata property, this artifact will be returned first on an `ASC` search and last on a
    `DESC` search.


Limit
-----

* A limit can be set on the number of results returned back by the api.
* Note: the method of sort effects which artifacts are contained within the limit.


Artifact Path
-------------

* This api exposes two search endpoints.
    * Search from the root of an S3 bucket:  **/\<bucket-name\>/artifact/\_search**
    * Search from a partial path: **/\<bucket-name\>/artifact/\<path\>/\_search**

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
    Link: </bucket-name/artifact/test>; rel="item"; title="artifact"
    Link: </bucket-name/artifact/dir/test>; rel="item"; title="artifact"
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

* We will assume the following about the artifacts being searched:
    * Artifact "a" is version=1.19 & buildNumber=25
    * Artifact "b" is version=1.19 & buildNumber=24
    * Artifact "c" is version=1.1 & buildNumber=100
    * Artifact "d" is version=1.1 & buildNumber=99

<b></b>

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: </bucket-name/artifact/application-dir/a>; rel="item"; title="artifact"
    Link: </bucket-name/artifact/application-dir/b>; rel="item"; title="artifact"
    Link: </bucket-name/artifact/application-dir/c>; rel="item"; title="artifact"
    Link: </bucket-name/artifact/application-dir/d>; rel="item"; title="artifact"
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT

For more examples see [advanced search examples](advanced-search-examples.md).

