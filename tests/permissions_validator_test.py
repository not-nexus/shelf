import yaml
from shelf.permissions_validator import PermissionsValidator
from mock import Mock
import boto
from shelf.container import Container
from tests.stdout_catcher import StdoutCatcher
import logging
import sys
from tests.functional_test_base import FunctionalTestBase


class PermissionsValidatorTest(FunctionalTestBase):
    def setUp(self):
        super(PermissionsValidatorTest, self).setUp()
        self.token = "PERMISSIONS_VALIDATOR.abc123"
        self.request = type("FakeRequest", (), {
            "headers": {
                "Authorization": self.token
            },
            "method": "POST",
            "path": "/test/artifact/test/file"
        })
        self.app.logger.warning = Mock()
        self.app.logger.info = Mock()
        self.container = Container(self.app, self.request)
        self.container.bucket_name = self.test_bucket.name
        self.permissions_no_name = {
            "token": "TOKEN",
            "write": ["/*"],
            "read": ["/*"]
        }

    def write_permissions(self, permissions):
        self.write_raw_permissions(yaml.dump(permissions))

    def write_raw_permissions(self, permissions):
        self.create_key(self.test_bucket, "_keys/{0}".format(self.token), permissions)

    def test_permissions_artifact_name(self):
        self.write_permissions(self.permissions_no_name)
        validator = PermissionsValidator(self.container)
        self.asserts.json_equals(self.permissions_no_name, validator.permissions)
        self.container.logger.warning.assert_called_with("Name was not set in authorization token.")

    def test_invalid_yaml(self):
        self.write_raw_permissions("{")
        validator = PermissionsValidator(self.container)
        permissions = validator.permissions
        self.assertEqual(None, permissions)

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
        self.assertEqual("Failed to find token provided.\n", catcher.output)

    def test_no_write(self):
        permissions_no_write = {
            "name": "wick",
            "token": "TOKEN",
            "read": ["/*"]
        }
        self.write_permissions(permissions_no_write)
        validator = PermissionsValidator(self.container)
        self.assertFalse(validator.allowed())
