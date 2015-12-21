from pyshelf.error_code import ErrorCode

class ArtifactNotFoundError(Exception):
    def __init__(self, artifact_name):
        message = "Artifact {} not found".format(artifact_name)
        super(ArtifactNotFoundError, self).__init__(message)
        self.error_code = ErrorCode.RESOURCE_NOT_FOUND


class BucketNotFoundError(Exception):
    def __init__(self, bucket_name):
        message = "Bucket {} not found".format(bucket_name)
        super(BucketNotFoundError, self).__init__(message)
        self.error_code = ErrorCode.INTERNAL_SERVER_ERROR       


class DuplicateArtifactError(Exception):
    def __init__(self, artifact_name):
        message = "Artifact by name {} already exists in current directory".format(artifact_name)
        super(DuplicateArtifactError, self).__init__(message)
        self.error_code = ErrorCode.DUPLICATE_ARTIFACT


class InvalidNameError(Exception):
    def __init__(self, name):
        message = "The artifact name provided is not an allowable name. Please remove leading underscores."
        super(InvalidNameError, self).__init__(message)
        self.error_code = ErrorCode.INVALID_ARTIFACT_NAME
