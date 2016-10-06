Artifact
========

You can upload an artifact provided you are authorized for that particular location. The `ref-name` is an alias for the backend storage (at the moent this is S3 only). See more about [reference name on the main README](../../README.md). A reference name is not required. If one is not specified the reference name will be the name of the storage (currently the S3 bucket's name).

     POST /ref-name/artifact/hello-world HTTP/1.1
     Authorization: supersecuretoken
     Expect: 100-continue
     Content-Type: multipart/form-data; boundary=------------------------b1ba732d480278ab

If successful, you will get back a 201 CREATED.

     HTTP/1.1 201 CREATED
     Content-Type: application/json
     Location: http://localhost:8080/ref-name/artifact/upload_tests

If the artifact already exists, you will not be allowed to upload over it.  Instead you will be returned a
403 FORBIDDEN.

     HTTP/1.1 403 FORBIDDEN
     Content-Type: application/json

     {
        "code": "duplicate_artifact",
        "message": "This artifact already exists and you are not allowed to overwrite it."
     }

If an artifact has an invalid name or begins with an underscore (reserved).

     HTTP/1.1 403 FORBIDDEN
     Content-Type: application/json

     {
        "code": "invalid_artifact_name",
        "message": "The name of the artifact was invalid."
     }



Here is an example using curl (examples directory has some great curl examples)

     curl -v -i -L -H "Authorization: supersecuretoken" -F "file=@./upload-test.txt" localhost:8080/ref-name/artifact/upload-test.txt

---

To get the same artifact back you can use get on the same path.

     GET /ref-name/artifact/hello-world HTTP/1.1
     Authorization: supersecuretoken

     HTTP/1.0 200 OK
     Content-Type: application/octet-stream
     Link: </ref-name/artifact/hello-world>; rel="self"; title="hello-world"
     Link: </ref-name/artifact/hello-world/_meta>; rel="metadata"; title="metadata"
     Content-Length: 74
     Server: Werkzeug/0.11.2 Python/2.7.9
     Date: Sun, 20 Dec 2015 23:12:21 GMT

If the artifact can not be found you will receive a 404 NOT FOUND

     HTTP/1.1 404 NOT FOUND
     Content-Type: application/json

     {
        "message": "Resource not found",
        "code": "resource_not_found"
     }

In curl:

     curl -i -L -H "Authorization: supersecuretoken" localhost:8080/ref-name/artifact/hello-world > hello-world.txt
