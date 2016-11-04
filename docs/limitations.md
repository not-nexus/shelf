Limitations
===========

Below are a list of limitations that the API has.  Most of these should have issues opened for them unless it is an excepted limitation.

* A search could become accurate if it matches more than the artifacts configured in `upperSearchResultLimit`.  This by default is 10000 but can be configured higher. [Issue here](https://github.com/not-nexus/shelf/issues/72).
* **Currently there is a limit of 5GB for an upload.**  [AWS requires multipart upload for anything larger than 5GB](http://docs.aws.amazon.com/AmazonS3/latest/dev/UploadingObjects.html).  We do not support this as of now.  If we did support multipart upload we would need handle our own hashes as well.  [Hashes are not as simple as "md5 the content" when it is uploaded in parts.](https://forums.aws.amazon.com/thread.jspa?messageID=203436&#203436).  Some thought is required for a good solution to this.
