Permissions
===========

The API uses basic access authentication which requires an `Authorization` header with a token.

The API will look in the requested bucket for a directory at the root of the bucket named `_keys`.
It will then search for a file with the name of the token that was supplied. The permissions are stored in this file in YAML format.

Example

We are attempting to get artifact named test from test-bucket with token 12345

    curl -H "Authorization: 12345" shelf.example.com/test-bucket/artifact/test

The API will look for the following file:

    test-bucket/_keys/12345

The permissions are as follows:

    name: John Doe
    token: 12345
    write:
        - "/**"
    read:
        - "/**"

As you can see this individual is granted access as they have full read and write access.
You can also grant specific access using the following glob syntax.

    -"/test/*"
    -"/test/file"
