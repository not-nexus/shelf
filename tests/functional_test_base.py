from moto import mock_s3
from pyshelf.app import app
import pyshelf.configure as configure
import boto
from boto.s3.key import Key
import yaml
import tests.metadata_utils as meta_utils
import tests.permission_utils as utils
from tests.route_tester.tester import Tester
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from pyshelf.search.container import Container as SearchContainer
from tests.metadata.comparator import Comparator as MetadataComparator
from pyshelf.resource_identity import ResourceIdentity
from tests.metadata_builder import MetadataBuilder
from tests.test_base import TestBase


class FunctionalTestBase(TestBase):
    RESPONSE_404 = {
        "message": "Resource not found",
        "code": "resource_not_found"
    }

    RESPONSE_403 = {
        "code": "forbidden",
        "message": "Forbidden"
    }

    RESPONSE_INVALID_NAME = {
        "message": "The artifact name provided is not allowable. Please remove leading underscores.",
        "code": "invalid_artifact_name"
    }

    RESPONSE_DUPLICATE = {
        "code": "duplicate_artifact",
        "message": "Artifact by name test already exists in current directory"
    }

    CONFIG = {
        "buckets": {
            "test": {
                "accessKey": "test",
                "secretKey": "test"
            },
            "bucket2": {
                "accessKey": "test",
                "secretKey": "test"
            },
            "thisBucketDoesntExistLol": {
                "accessKey": "fail",
                "secretKey": "fail"
            }
        },
        "elasticsearch": {
            "connectionString": "http://localhost:9200/metadata",
        }
    }

    def setUp(self):
        self.app = app
        self.setup_elastic()
        self.setup_moto()
        self.setup_metadata()
        self.test_client = app.test_client()
        self._route_tester = None
        self._metadata_comparator = None

    @property
    def metadata_comparator(self):
        if not self._metadata_comparator:
            self._metadata_comparator = MetadataComparator(
                self,
                FunctionalTestBase.CONFIG["elasticsearch"]["connectionString"],
                app.logger)

        return self._metadata_comparator

    def assert_metadata_matches(self, resource_url):
        """
            Makes the assumption that mock_s3 has been
            enabled (done in configure_moto).

            Makes sure that the metadata for a particular
            artifact is the same in the search layer and
            the cloud layer.

            Args:
                resource_url(basestring): The full path to the resource from the APIs
                    perspective

            Raises:
                AssertionError
        """
        self.metadata_comparator.compare(resource_url)

    @classmethod
    def setUpClass(cls):
        super(FunctionalTestBase, cls).setUpClass()
        configure.logger(app.logger, "DEBUG")
        app.config.update(cls.CONFIG)

    def setup_elastic(self):
        search_container = SearchContainer(self.app.logger, FunctionalTestBase.CONFIG["elasticsearch"])
        self.search_wrapper = SearchTestWrapper(search_container)

    def setup_moto(self):
        self.moto_s3 = mock_s3()
        self.moto_s3.start()
        import httpretty
        # EXTREMELY IMPORTANT!  If the port is not
        # appended httpretty does not identify it as http
        # but httplib does so the file pointer that
        # is supposed to be filled up by httpetty.fakesocket.socket
        # is not.
        httpretty.core.POTENTIAL_HTTP_PORTS.add(9200)
        self.boto_connection = boto.connect_s3()
        self.boto_connection.create_bucket("test")
        self.boto_connection.create_bucket("bucket2")
        self.test_bucket = self.boto_connection.get_bucket("test")
        self.setup_artifacts()
        self.create_auth_key()

    def setup_artifacts(self):
        key = Key(self.test_bucket, "test")
        key.set_contents_from_string("hello world")
        nested_key = Key(self.test_bucket, "/dir/dir2/dir3/nest-test")
        nested_key.set_contents_from_string("hello world")
        artifact_list = Key(self.test_bucket, "/dir/dir2/dir3/dir4/test5")
        artifact_list.set_contents_from_string("")
        thing_key = Key(self.test_bucket, "empty")
        thing_key.set_contents_from_string("hello world")
        empty_meta = Key(self.test_bucket, "/_metadata_empty.yaml")
        empty_meta.set_contents_from_string("")

    def setup_metadata(self):
        self.add_metadata("/test/artifact/test")
        self.add_metadata("/test/artifact/dir/dir2/dir3/nest-test")
        self.add_metadata("/test/artifact/this/that/other", "1.2")
        self.add_metadata("/test/artifact/thing", "1.2"),
        self.add_metadata("/test/artifact/blah", "1.19"),
        self.add_metadata("/test/artifact/a", "1.19"),
        self.add_metadata("/test/artifact/zzzz", "1.19"),
        self.add_metadata("/test/artifact/dir/dir2/Test", "2")
        self.search_wrapper.refresh_index()

    def add_metadata(self, resource_path, version="1", metadata=None):
        """
            Adds metadata to moto and elastic.
        """
        resource_id = ResourceIdentity(resource_path)
        data = meta_utils.get_meta(resource_id.artifact_name, resource_id.resource_path, version)

        if metadata:
            data.update(metadata)

        key = Key(self.boto_connection.get_bucket(resource_id.bucket_name), resource_id.cloud_metadata)
        key.set_contents_from_string(yaml.dump(data))
        self.search_wrapper.add_metadata(resource_id.search, data)

    def create_auth_key(self):
        self.auth = utils.auth_header()
        key_name = "_keys/{}".format(self.auth["Authorization"])
        auth_key = Key(self.test_bucket, key_name)
        auth_key.set_contents_from_string(utils.get_permissions_func_test())
        auth_bucket2 = Key(self.boto_connection.get_bucket("bucket2"), key_name)
        auth_bucket2.set_contents_from_string(utils.get_permissions_func_test())

    def create_metadata_builder(self):
        return MetadataBuilder()

    @property
    def route_tester(self):
        if not self._route_tester:
            self._route_tester = Tester(self, self.test_client)

        return self._route_tester

    def tearDown(self):
        self.moto_s3.stop()
        self.search_wrapper.teardown_metadata()

    def response_500(self, message=None):
        if not message:
            message = "Internal server error"

        return {
            "message": message,
            "code": "internal_server_error"
        }
