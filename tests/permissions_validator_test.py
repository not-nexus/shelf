import pyproctor
from moto import mock_s3
from pyshelf.permissions_validator import PermissionsValidator
from mock import Mock
import yaml
import boto
from pyshelf.container import Container
from tests.stdout_catcher import StdoutCatcher
import logging
import sys


class PermissionsValidatorTest(pyproctor.TestBase):
    def setUp(self):
        super(PermissionsValidatorTest, self).setUp()
        self.permissions_no_name = {
            "token": "TOKEN",
            "write": ["/*"],
            "read": ["/*"]
        }

        self.moto_s3 = mock_s3()
        self.moto_s3.start()

    def tearDown(self):
        super(PermissionsValidatorTest, self).tearDown()
        self.moto_s3.stop()

    def test_permissions_artifact_name(self):
        container_mock = Mock()
        storage_mock = Mock()
        storage_mock.__enter__ = Mock(return_value=storage_mock)
        storage_mock.__exit__ = Mock(return_value=False)
        storage_mock.get_artifact_as_string = Mock(return_value=yaml.dump(self.permissions_no_name))
        request_mock = Mock()
        request_mock.headers = {"Authorization": "TOKEN"}
        container_mock = type(
            "FakeContainer",
            (),
            {"request": request_mock, "create_silent_bucket_storage": Mock(return_value=storage_mock), "logger": Mock()}
        )
        validator = PermissionsValidator(container_mock())
        self.asserts.json_equals(self.permissions_no_name, validator.permissions)
        storage_mock.get_artifact_as_string.assert_called_with("_keys/TOKEN")
        container_mock.logger.warning.assert_called_with("Name was not set in authorization token.")

    def test_no_artifact_not_logged(self):
        """
            A pretty functional test. What I really wanted out of this
            test was to make sure that the PermissionsValidator would use
            the "silent_logger" for the storage that it would use.  We
            don't want it to log a message with the authorization token
            that was used. This potentially could be sensitive information.
            For instance in the case where a user sends a valid token but
            accidentally misspells the bucket name.
        """
        # Create a bucket but don't add anything to it. I only need it to
        # NOT find the token I am requesting.
        boto_connection = boto.connect_s3()
        boto_connection.create_bucket("test")

        # Use StdoutCatcher to gather the stdout for use later.
        with StdoutCatcher() as catcher:
            # Important that this logger is creating inside of this
            # with context because I need sys.stdout to be monkeypatched
            # to be the StringIO object created with StdoutCatcher.
            main_logger = logging.getLogger("MainLogger")
            main_logger.addHandler(logging.StreamHandler(sys.stdout))
            main_logger.setLevel(logging.DEBUG)
            app = type("FakeApp", (), {
                "config": {
                    "buckets": [
                        {
                            "name": "test",
                            "referenceName": "test",
                            "accessKey": "test",
                            "secretKey": "test"
                        },
                    ]
                },
                "logger": main_logger
            })

            request = type("FakeRequest", (), {
                "headers": {
                    "Authorization": "abc123"
                }
            })

            container = Container(app, request)
            container.bucket_name = "test"
            validator = container.permissions_validator
            # This is the meat of the test. When accessing the permissions
            # property it will attempt to get the token from the cloud storage.
            # It should NOT find this token but still should not log anything.
            permissions = validator.permissions

        # Make sure it hadn't found anything.
        self.assertEqual(None, permissions)
        # Make sure it didn't log the token.  The fact that it doesn't log
        # anything else is incidental.
        self.assertEqual("", catcher.output)
