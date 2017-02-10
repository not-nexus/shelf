from boto.s3.key import Key
from mock import Mock
from moto import mock_s3
from pyproctor import MonkeyPatcher
from shelf.app import app
from shelf.error_code import ErrorCode
from shelf.metadata.initializer import Initializer
from shelf.resource_identity import ResourceIdentity
from shelf.search.container import Container as SearchContainer
from tests.metadata.comparator import Comparator as MetadataComparator
from tests.metadata_builder import MetadataBuilder
from tests.route_tester.tester import Tester
from tests.search.test_wrapper import TestWrapper as SearchTestWrapper
from tests.test_base import TestBase
import boto
import shelf.configure as configure
import tests.metadata_utils as meta_utils
import tests.permission_utils as utils
import yaml


class FunctionalTestBase(TestBase):
    RESPONSE_404 = {
        "message": "Resource not found",
        "code": ErrorCode.RESOURCE_NOT_FOUND
    }

    RESPONSE_403 = {
        "code": ErrorCode.FORBIDDEN,
        "message": "Forbidden"
    }

    RESPONSE_401 = {
        "code": ErrorCode.PERMISSION_DENIED,
        "message": "Permission denied"
    }

    RESPONSE_INVALID_NAME = {
        "message": "Artifact and directories names that BEGIN with an underscore are reserved as private "
                   "and cannot be accessed or created. This of course exludes _search and _meta which are "
                   "not part of the artifact path itself.",
        "code": ErrorCode.INVALID_ARTIFACT_NAME
    }

    RESPONSE_DUPLICATE = {
        "code": ErrorCode.DUPLICATE_ARTIFACT,
        "message": "Artifact by name test already exists in current directory"
    }

    RESPONSE_INVALID_FORMAT = {
        "code": ErrorCode.INVALID_REQUEST_DATA_FORMAT,
        "message": "Data sent with request must be in JSON format and also be either an array or an object.",
    }

    CONFIG = {
        "buckets": [
            {
                "name": "test",
                "referenceName": "test",
                "accessKey": "test",
                "secretKey": "test"
            },
            {
                "name": "bucket2",
                "referenceName": "b2",
                "accessKey": "test",
                "secretKey": "test"
            },
            {
                "name": "this-bucket-doesnt-exist-lol",
                "referenceName": "thisBucketDoesntExistLol",
                "accessKey": "fail",
                "secretKey": "fail"
            }
        ],
        "elasticsearch": {
            "connectionString": "http://localhost:9200/metadata",
            "upperSearchResultLimit": 100
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
        self.setup_storage()

    def setup_storage(self):
        """
            This is important for comparing metadata later
            on because we "assertEqual" but the date would
            be different every time the test was run.  The
            solution was to patch _to_utc to always return
            the same date.
        """
        get_created_date = Mock(return_value=meta_utils.CREATED_DATE)
        MonkeyPatcher.patch(Initializer, "_get_created_date", get_created_date)

    @property
    def metadata_comparator(self):
        if not self._metadata_comparator:
            self._metadata_comparator = MetadataComparator(
                self,
                FunctionalTestBase.CONFIG["elasticsearch"]["connectionString"],
                app.logger)

        return self._metadata_comparator

    def assert_metadata_matches(self, resource_url, bucket_name=None):
        """
            Makes the assumption that mock_s3 has been
            enabled (done in configure_moto).

            Makes sure that the metadata for a particular
            artifact is the same in the search layer and
            the cloud layer.

            Args:
                resource_url(basestring): The full path to the resource from the APIs
                    perspective
                bucket_name(basestring): Optional.  The name of the bucket the artifact
                    will be stored in.

            Raises:
                AssertionError
        """
        if not bucket_name:
            identity = ResourceIdentity(resource_url)
            for bucket_config in FunctionalTestBase.CONFIG["buckets"]:
                # identity.bucket_name is actually reference name.
                # TODO: Rename this.
                if identity.bucket_name == bucket_config["referenceName"]:
                    bucket_name = bucket_config["name"]

        if not bucket_name:
            self.fail("bucket_name was not provided and we failed to look it up via FunctionalTestBase.CONFIG")

        self.metadata_comparator.compare(resource_url, bucket_name)

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
        self.create_key(self.test_bucket, "test", contents="hello world")
        self.create_key(self.test_bucket, "/dir/dir2/dir3/dir4/test5")
        self.create_key(self.test_bucket, "/dir/dir2/dir3/nest-test", contents="hello world")
        # "empty" has an empty metadata file.  This is used when testing initialization
        # of metadata
        self.create_key(self.test_bucket, "empty", contents="hello world")
        self.create_key(self.test_bucket, "/_metadata_empty.yaml")
        self.create_key(self.test_bucket, "/dir/dir2/_secret", "No one should see this")
        self.create_key(self.test_bucket, "/dir/dir2/not_secret", "You can see this though")

    def create_key(self, bucket, artifact_name, contents=None):
        """
            Creates an artifact in moto.

            Args:
                bucket(boto.s3.bucket.Bucket)
                artifact_name(string)
                contents(string | None)
        """
        if contents is None:
            contents = ""
        key = Key(bucket, artifact_name)
        key.set_contents_from_string(contents)

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
        # TODO: Revamp the permissions utils stuff. I am not
        # a fan of how it works.
        self.auth = self.setup_auth_token(utils.VALID_TOKEN)
        self.read_only_auth = self.setup_auth_token(utils.READ_ONLY_TOKEN)

    def setup_auth_token(self, token):
        """
            Sets up authorization key file in both functional test buckets.

            Args:
                token: string

            Returns:
                dict: Authorization header.
        """
        self.add_auth_token(token, "test")
        self.add_auth_token(token, "bucket2")
        return utils.auth_header(token)

    def add_auth_token(self, token, bucket_name):
        """
            Adds an auth token to the bucket represented by the
            bucket_name provided.  Note: This token must be defined
            in tests.permission_utils.get_permissions

            Args:
                token(string)
                bucket_name(string)
        """
        key_name = "_keys/{0}".format(token)
        permissions = utils.get_permissions(token)
        bucket = self.boto_connection.get_bucket(bucket_name)
        auth_key = Key(bucket, key_name)
        auth_key.set_contents_from_string(permissions)

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
        super(TestBase, self).tearDown()

    def response_500(self, message=None):
        if not message:
            message = "Internal server error"

        return {
            "message": message,
            "code": "internal_server_error"
        }
