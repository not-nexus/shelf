IMPORTANT NOTE
==============

Due to some shared memory issues we have disabled `failingStorage`, `passingStorage` and `search`. We are only leaving the documentation here for when we enable it again.

Health
======

You can check the health of shelf by using the health endpoint.

**IMPORTANT NOTE**: This endpoint ONLY verifies that external dependencies work. This means connection and authentication to the search(elasticsearch) and cloud(AWS S3) layers. This was a conscious decision. We do not plan to add any more robust checks in the future since the health check must be fast and we don't want to maintain something that becomes needlessly complex.

Note: The way the [health endpoint was designed](../architectural-desicions.md) health is recorded when failures or successes happen instead of each time that the health endpoint is called. That means that it is possible (for instance in the event of an AWS outage and recovery) that the health endpoint would report failing when it was actually passing or vise versa. These types of discrepancies are cleaned up naturally the next time the search or cloud layer is invoked for a particular bucket.

Response Properties
-------------------

* `status`: The overall health of the service.
* `failingStorage`: Shows which storages (S3 buckets) we are unable to access.
* `search`: Shows if search is functional (we can connect to elasticsearch).
* `passingStorage`: A list of storages (S3 buckets) we were able to access.

Status
------

The status is a property in the response body and as a special `X-Status` header. It will be set to one of three values.

* `OK` - Everything is accessible.
* `WARNING` - We failed to connect to some storages(S3 buckets) but less than 20% of them.
* `CRITICAL` - We failed to connect to search(elasticsearch) or we failed to access more than 20% of storages(S3 buckets).

Usage
-----

At any time you can get the health of the service via a `GET` or `HEAD` request. This endpoint does *not* require authentication.

     GET /health HTTP/1.1

If the health check is successful, a 200 will be returned.

     HTTP/1.0 200 OK
     Content-Type: application/json
     X-Status: OK
     Content-Length: 104

     {
        "status": "OK",
        "failingStorage": [],
        "search": true,
        "passingStorage": [
            "storage1",
            "storage2",
            "storage3"
        ]
     }

If `status` is set to anything other than `OK` a `503` will be returned.

    HTTP/1.0 503 SERVICE UNAVAILABLE
    Content-Type: application/json
    X-Status: CRITICAL
    Content-Length: 104

    {
        "failingStorage": [
            "storage1"
        ],
        "passingStorage": [
            "storage2",
            "storage3"
        ],
        "search": false,
        "status": "CRITICAL"
    }
