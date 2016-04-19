Artifact Links
==============

Note: this feature is a newly added feature with very basic linking and will be improved during development.

When you request an artifact links are included. For artifacts that represent a file you will receive a self and metadata link back.

    GET /bucket-name/artifact/hello-world HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 200 OK
    Content-Type: application/octet-stream
    Link: /bucket-name/artifact/hello-world; rel=self; title=hello-world
    Link: /bucket-name/artifact/hello-world/_meta; rel=related; title=metadata
    Content-Length: 74
    Server: Werkzeug/0.11.2 Python/2.7.9
    Date: Sun, 20 Dec 2015 23:12:21 GMT

If you want links without the artifact you can use the HEAD verb instead, which only returns headers.

For an artifact that represents a directory you will receive back header links for artifacts in that directory.

    GET /bucket-name/artifact/dir HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: /bucket-name/artifact/dir/hello-world; rel=item; title=artifact
    Link: /bucket-name/artifact/dir/; rel=self; title=a collection of metadata
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT
