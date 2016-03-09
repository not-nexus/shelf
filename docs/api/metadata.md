Metadata
========

####Pyshelf supports mutable and immutable metadata for artifacts. You can request, update, create, and delete metadata and particular metdata items.

The following is an example of updating all metadata for an artifact. This will only overwrite mutable items. The response to this request is identical to doing a GET on the same route.

    PUT /artifact/hello-world/_meta
    Authorization: supersecrettoken

    {
        "tag": {
            "immutable": true,
            "value": "never edit this stuff"
        },
         "tag1": {
            "immutable": false,
            "value": "test"
        }
    }

The following is the response from this endpoint. Again, immutable items can only be created.

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 205
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:07:50 GMT

    {
        "md5Hash": {
            "name": "md5Hash",
            "value": "cd62151eefb59da744549d26a79e2717",
            "immutable": true
        },
         "tag": {
            "immutable": true,
             "value": "never edit this stuff"
        }, "tag1": {
            "immutable": false,
            "value": "test"
        }
    }

---

The following is a request and response for all metadata for a particular artifact.

    GET /artifact/hello-world/_meta HTTP/1.1
    Authorization: supersecuretoken=

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 205
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:02:56 GMT

    {
        "md5Hash": {
            "name": "md5Hash",
            "value": "cd62151eefb59da744549d26a79e2717",
            "immutable": true
        },
         "tag": {
            "immutable": true,
             "value": "never edit this stuff"
        }, "tag1": {
            "immutable": true,
            "value": "test"
        }
    }

----

You can request particular metadata items for an artifact.

    GET /artifact/hello-world/_meta/md5Hash HTTP/1.1
    Authorization: supersecuretoken=

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 84
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:18:21 GMT

    {
        "name": "md5Hash",
        "value": "cd62151eefb59da744549d26a79e2717",
        "immutable": true
    }

----

The following is an example of a PUT/POST request for a particular metadata item. The only difference between a POST and a PUT is that the latter will update existing mutable items.

    POST /artifact/hello-world/_meta/tag2 HTTP/1.1
    Authorization: supersecuretoken=

    {"immutable": false, "value": "edit this stuff"}

And the response..

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 49
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:23:00 GMT

    {"immutable": false, "value": "edit this stuff"}

Since this is mutable, you are able to update this item with a PUT request.

    PUT /artifact/hello-world/_meta/md5Hash HTTP/1.1
    Authorization: supersecuretoken=

    HTTP/1.0 201 CREATED
    Content-Type: application/json
    Content-Length: 49
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:23:00 GMT

    {"immutable": false, "value": "edit this stuff"}

----

####Error Responses

If you attempt to update an immutable item or an existing one via POST this is the error you will receive.

    HTTP/1.0 403 FORBIDDEN
    Content-Type: application/json
    Content-Length: 72
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:21:23 GMT

    {"message": "The metadata item tag is immutable.", "code": "forbidden"}

When requesting metadata or an artifact that does not exist you will receive the following response.

    HTTP/1.0 404 NOT FOUND
    Content-Type: application/json
    Content-Length: 64
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:31:33 GMT

    {"message": "Resource not found", "code": "resource_not_found"}

If you make a request on an artifact or an artifact's metadata that you do not have access to, you will receive the following response.

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 18
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 22:37:49 GMT

    Permission Denied
