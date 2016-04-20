import pyproctor
import pyshelf.configure as configure
import os
import yaml
import errno
import copy
from jsonschema import ValidationError


class ConfigureTest(pyproctor.TestBase):
    def setUp(self):
        super(ConfigureTest, self).setUp()
        self.path = os.path.dirname(os.path.realpath(__file__)) + "/data/config.yaml"
        self.app = type("TestApp", (), {})()
        self.app.config = {}

    def tearDown(self):
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

    def test_app(self):
        config = {
            "buckets": [
                {
                    "accessKey": "whateveriwanthere",
                    # can't stop seeing WhichCanalSobe
                    "secretKey": "supersecretkeywhichcanalsobewhateveriwant",
                    "name": "myBucket",
                    "alias": "test"
                }
            ],
            "elasticsearch": {
                "connectionString": "http://localhost:9200/metadata",
                "region": "us-east-1",
                "accessKey": "blahdiddyblah",
                "secretKey": "sneakyAlphaNumericKey"
            }
        }
        self.write_config(config)
        # To make sure it doens't overwrite it
        self.app.config["hello"] = "hi"
        expected = copy.deepcopy(config)
        expected["hello"] = "hi"
        expected["bulkUpdateLogDirectory"] = "/var/log/bucket-update"
        self.run_app_config()
        self.assertEqual(expected, self.app.config)

    def test_config_value_error(self):
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
        with self.assertRaises(ValidationError):
            self.run_app_config()

    def test_config_empty(self):
        config = {}
        self.write_config(config)
        with self.assertRaises(ValidationError):
            self.run_app_config()

    def test_config_no_buckets(self):
        config = {"buckets": {}, "elasticsearch": {}}
        self.write_config(config)
        with self.assertRaises(ValidationError):
            self.run_app_config()
