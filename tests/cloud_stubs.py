from pyshelf.cloud.cloud_exceptions import ArtifactNotFoundError


class CloudStreamIteratorStub(object):
    def __init__(self, content):
        self.content = content
        self.index = 0
        self.chunk_size = 10

    def __iter__(self):
        return self

    def next(self):
        position = self.index * self.chunk_size
        end = position + self.chunk_size
        chunk = None

        if position < len(self.content):
            if (end + 1) > len(self.content):
                chunk = self.content[position:]
            else:
                chunk = self.content[position:end]

            self.index += 1
        else:
            raise StopIteration

        return chunk

    @property
    def headers(self):
        return {"content-type": "text/plain"}

default_artifacts = {
    "test": "hello world"
}


class CloudFactoryStub(object):

    storage_list = []
    artifacts = default_artifacts

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    @staticmethod
    def register_artifact(self, name, content):
        CloudFactoryStub.artifacts[name] = content

    @staticmethod
    def reset():
        CloudFactoryStub.artifacts = default_artifacts
        CloudFactoryStub.storage_list = []

    def create_storage(self, bucket_name):
        c = self.config
        storage = CloudStorageStub(c["accessKey"], c["secretKey"], bucket_name, self.logger)
        storage.artifacts = CloudFactoryStub.artifacts
        CloudFactoryStub.storage_list.append(storage)
        return storage


class CloudStorageStub(object):
    def __init__(self, access_key, secret_key, bucket_name, logger):
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.logger = logger
        self.artifacts = {}

    def connect(self):
        self.logger.debug("Stubbed connection")

    def close(self):
        self.logger.debug("Closing subbed connection")

    def get_artifact(self, artifact_name):
        artifact = self.artifacts.get(artifact_name)
        if artifact:
            stream = CloudStreamIteratorStub(artifact)
        else:
            raise ArtifactNotFoundError(artifact_name)
        return stream

    def upload_artifact(self, artifact_name, fp):
        return True
    
    def get_permissions_key(self, token):
        yaml = """
        name: 'Andy Gertjejansen'
        token: '190a64931e6e49ccb9917c7f32a29d19'
        write:
          - 'andy_gertjejansen/**'
          - 'kyle_long/andy_upload_access/*'
        read:
          - '/**'"""
               
        return yaml
                
    def delete_artifact(self, artifact_name):
        return True

    def __enter__(self):
        """ For use in "with" syntax"""
        self.connect()
        return self

    def __exit__(self, exception_type, exception, traceback):
        """ For use in "with" syntax"""
        self.close()
        return False
