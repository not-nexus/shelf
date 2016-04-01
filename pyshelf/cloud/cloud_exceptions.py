from pyshelf.error_code import ErrorCode


class CloudStorageException(Exception):
    def __init__(self, message, error_code):
        super(CloudStorageException, self).__init__(message)
        self.error_code = error_code


class ArtifactNotFoundError(CloudStorageException):
    def __init__(self, artifact_name):
        message = "Artifact {} not found".format(artifact_name)
        super(ArtifactNotFoundError, self).__init__(message, ErrorCode.RESOURCE_NOT_FOUND)


class BucketNotFoundError(CloudStorageException):
    def __init__(self, bucket_name):
        message = "Bucket {} not found".format(bucket_name)
        super(BucketNotFoundError, self).__init__(message, ErrorCode.INTERNAL_SERVER_ERROR)


class DuplicateArtifactError(CloudStorageException):
    def __init__(self, artifact_name):
        message = "Artifact by name {} already exists in current directory".format(artifact_name)
        super(DuplicateArtifactError, self).__init__(message, ErrorCode.DUPLICATE_ARTIFACT)


class InvalidNameError(CloudStorageException):
    def __init__(self, name):
        message = "The artifact name provided is not allowable. Please remove leading underscores."
        super(InvalidNameError, self).__init__(message, ErrorCode.INVALID_ARTIFACT_NAME)
