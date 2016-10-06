Artifact Links
==============

Artifact links come in a variety of `rel`s.
* **artifact** - This type of link specifies an artifact (a file) that can be downloaded. You cannot upload to that resource link due to it being immuatable(you cannot change it).
* **collection** - This specifies a "directory" which may contain other `collection` or `artifact` links.
* **metadata** - This is a link that tells you where [metadata](metadata.md) is stored for a particular `artifact`.  You will not get this link unless you perform a `HEAD` or `GET` request on an `artifact` resource.
* **self** - This points to the `artifact` or `metadata` resource you have requested.

When you request an `artifact`, links are included in the HTTP headers. If you request an artifact directly you will get a `self` and `metadata` link back along with the [artifact](artifact.md) as the body. 

    GET /ref-name/artifact/hello-world HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 200 OK
    Content-Type: application/octet-stream
    Link: </ref-name/artifact/hello-world>; rel="self"; title="hello-world"
    Link: </ref-name/artifact/hello-world/_meta>; rel="related"; title="metadata"
    Content-Length: 74
    Server: Werkzeug/0.11.2 Python/2.7.9
    Date: Sun, 20 Dec 2015 23:12:21 GMT

If you want links without the artifact you can use the `HEAD` verb instead, which only returns headers (which includes `Link` headers).

If you perform a `GET` on a directory instead of an `artifact` you will receive header links for `artifact`s or `collection`s in that directory. Pay close attention to the `rel` type. This will tell you which type that resource is.

    GET /ref-name/artifact/dir HTTP/1.1
    Authorization: supersecuretoken

    HTTP/1.0 204 NO CONTENT
    Content-Type: text/html; charset=utf-8
    Link: </ref-name/artifact/dir/hello-world>; rel="item"; title="artifact"
    Link: </ref-name/artifact/dir/; rel="self">; title="a collection of metadata"
    Content-Length: 0
    Server: Werkzeug/0.11.3 Python/2.7.10
    Date: Wed, 09 Mar 2016 21:51:40 GMT
