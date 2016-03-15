Artifact Links
==============

Note: this feature is a newly added feature with very basic linking and will be improved during development.

When you request an artifact links are included. For artifacts that represent a file you will receive a self and metadata link back.

    GET /bucket-name/artifact/hello-world HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 200 OK
    Content-Type: application/octet-stream
    Link: /bucket-name/artifact/hello-world; rel=self; title=hello-world, /bucket-name/artifact/hello-world/_meta; rel=metadata; title=metadata
    Content-Length: 74
    Server: Werkzeug/0.11.2 Python/2.7.9
    Date: Sun, 20 Dec 2015 23:12:21 GMT


For an artifact that represents a directory you will receive back header links for artifacts in that directory. Note the trailing forward slash.

    GET /bucket-name/artifact/hello-world-dir/ HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: /bucket-name/artifact/hello-world; rel=child; title=hello-world, /bucket-name/artifact/hello-world-dir/; rel=self; title=hello-world-dir/
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT
