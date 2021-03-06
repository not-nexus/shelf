from shelf.error_code import ErrorCode


class CloudStorageException(Exception):
    def __init__(self, message, error_code):
        super(CloudStorageException, self).__init__(message)
        self.error_code = error_code


class ArtifactNotFoundError(CloudStorageException):
    def __init__(self, artifact_name):
        message = "Artifact {0} not found".format(artifact_name)
        super(ArtifactNotFoundError, self).__init__(message, ErrorCode.RESOURCE_NOT_FOUND)


class BucketNotFoundError(CloudStorageException):
    def __init__(self, bucket_name):
        message = "Bucket {0} not found".format(bucket_name)
        super(BucketNotFoundError, self).__init__(message, ErrorCode.RESOURCE_NOT_FOUND)


class DuplicateArtifactError(CloudStorageException):
    def __init__(self, artifact_name):
        message = "Artifact by name {0} already exists in current directory".format(artifact_name)
        super(DuplicateArtifactError, self).__init__(message, ErrorCode.DUPLICATE_ARTIFACT)


class BucketConfigurationNotFound(CloudStorageException):
    def __init__(self, bucket_name):
        message = "Could not find configuration for bucket {0}".format(bucket_name)
        super(BucketConfigurationNotFound, self).__init__(message, ErrorCode.RESOURCE_NOT_FOUND)
