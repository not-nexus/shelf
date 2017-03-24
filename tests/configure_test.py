import pyproctor
import shelf.configure as configure
import os
import yaml
import errno
import copy
from mock import Mock
import logging


class ConfigureTest(pyproctor.TestBase):
    def setUp(self):
        super(ConfigureTest, self).setUp()
        self.path = os.path.dirname(os.path.realpath(__file__)) + "/data/config.yaml"
        self.app = type("TestApp", (), {})()
        self.app.config = {}

    def tearDown(self):
        super(ConfigureTest, self).tearDown()
        # This appears to be the most pythonic way to do it
        # instead of calling the os.path.exists.  Discussion
        # about it here:
        # http://stackoverflow.com/questions/10840533/most-pythonic-way-to-delete-a-file-which-may-not-exist
        try:
            os.remove(self.path)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def write_config(self, data):
        contents = yaml.safe_dump(
            data,
            encoding="utf-8",
            indent=4,
            default_flow_style=False
        )

        with open(self.path, "w") as f:
            f.write(contents)

    def run_app_config(self):
        configure.app_config(self.app.config, self.path)

    def create_config(self, hook_command=None):
        config = {
            "buckets": [
                {
                    "accessKey": "whateveriwanthere",
                    # can't stop seeing WhichCanalSobe
                    "secretKey": "supersecretkeywhichcanalsobewhateveriwant",
                    "name": "myBucket",
                    "referenceName": "test"
                }
            ],
            "elasticsearch": {
                "connectionString": "http://localhost:9200/metadata",
                "region": "us-east-1",
                "accessKey": "blahdiddyblah",
                "secretKey": "sneakyAlphaNumericKey"
            }
        }

        if hook_command:
            config["hookCommand"] = hook_command

        return config

    def test_app(self):
        config = self.create_config()
        self.write_config(config)
        # To make sure it doens't overwrite it
        self.app.config["hello"] = "hi"
        expected = copy.deepcopy(config)
        expected["hello"] = "hi"
        expected["bulkUpdateLogDirectory"] = "/var/log/bucket-update"
        self.run_app_config()
        self.assertEqual(expected, self.app.config)

    def test_app_with_hook_command(self):
        # Config is in tests/data/config.yaml
        config = self.create_config("../bin/hook-test")
        self.write_config(config)
        base = os.path.dirname(__file__)
        hook_command = os.path.realpath(os.path.join(base, "bin/hook-test"))
        self.run_app_config()
        self.assertEqual(hook_command, self.app.config["hookCommand"])

    def test_app_config_invalid_yaml(self):
        contents = """
        elasticsearch:
        connectionString: http://localhost:9200/metadata
        bulkUpdateLogDirectory: /var/log/bucket-update
        buckets:
        -
            name: 1
            referenceName: 1
            accessKey: fake
            {{ # this is invalid
            secretKey: fake

        """
        with open(self.path, "w") as f:
            f.write(contents)

        with self.assertRaises(ValueError) as context:
            self.run_app_config()

        self.assertEqual("{0} contained invalid yaml".format(self.path), context.exception.message)

    def test_app_config_config_does_not_exist(self):
        with self.assertRaises(ValueError) as context:
            self.run_app_config()

        self.assertEqual("Could not find or open file {0}".format(self.path), context.exception.message)

    def test_config_validation_error(self):
        config = {
            "buckets": [
                {
                    "secretKey": "ffffffffffffffffffungal",
                    "name": "myBucket"
                },
                {
                    "accessKey": "imGaGaGonnaMakeYouSoup",
                    "secretKey": "freeTibet",
                    "name": "myOtherBucket"
                }
            ],
            "elasticsearch": {
                "connectionString": "http://localhost:9200/metadata"
            }
        }
        self.write_config(config)
        with self.assertRaises(ValueError):
            self.run_app_config()

    def test_config_value_error(self):
        config = {
            "buckets": [
                {
                    "secretKey": "ft",
                    "accessKey": "ft",
                    "name": "myBucket"
                },
                {
                    "accessKey": "ft",
                    "secretKey": "ft",
                    "name": "myOtherBucket",
                    "referenceName": "myBucket"
                }
            ],
            "elasticsearch": {
                "connectionString": "http://localhost:9200/metadata"
            }
        }
        self.write_config(config)
        with self.assertRaises(ValueError):
            self.run_app_config()

    def test_configure_app(self):
        dirname_mock = Mock(return_value="dir")
        pyproctor.MonkeyPatcher.patch(os.path, "dirname", dirname_mock)
        app_config_mock = Mock()
        pyproctor.MonkeyPatcher.patch(configure, "app_config", app_config_mock)
        self.app.logger = Mock()
        configure.app(self.app)
        log_level = logging.getLevelName("INFO")
        calls = self.app.logger.addHandler.mock_calls
        self.assertEqual(1, len(calls))
        self.app.logger.setLevel.assert_called_with(log_level)
        configure.app_config.assert_called_with({}, "dir/../config.yaml")

    def test_hook_command_file_doesnt_exist(self):
        with self.assertRaises(ValueError):
            configure.hook_command(self.path, "totally-doesnt-exist")

    def test_hook_command_file_not_executable(self):
        with self.assertRaises(ValueError):
            configure.hook_command(self.path, "../bin/hook-test-not-executable")

    def test_hook_command_works_with_args(self):
        cmd = configure.hook_command(self.path, "../bin/hook-test a b c")
        self.assertIsInstance(cmd, basestring)
