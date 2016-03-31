import pyproctor
import pyshelf.configure as configure
import os
import yaml
import errno
import copy


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

    def run_app(self):
        configure.app(self.app, self.path)

    def test_app(self):
        config = {
            "buckets": {
                "myBucket": {
                    "accessKey": "whateveriwanthere",
                    # can't stop seeing WhichCanalSobe
                    "secretKey": "supersecretkeywhichcanalsobewhateveriwant"
                }
            },
            "elasticSearchConnectionString": "http://localhost:9200/metadata"
        }
        self.write_config(config)
        # To make sure it doens't overwrite it
        self.app.config["hello"] = "hi"
        expected = copy.deepcopy(config)
        expected["hello"] = "hi"
        self.run_app()
        self.assertEqual(expected, self.app.config)

    def test_config_value_error(self):
        config = {
            "buckets": {
                "myBucket": {
                    "secretKey": "ffffffffffffffffffuuuuuuuuuuuuuu"
                },
                "myOtherBucket": {
                    "accessKey": "imGaGaGonnaMakeYouSomeSoup",
                    "secretKey": "freeTibet"
                }
            },
            "elasticSearchConnectionString": "http://localhost:9200/metadata"
        }
        self.write_config(config)
        self.assert_value_error()

    def test_config_empty(self):
        config = {}
        self.write_config(config)
        self.assert_value_error()

    def test_config_no_buckets(self):
        config = {"buckets": {}, "elasticSearchConnectionString": "test"}
        self.write_config(config)
        self.assert_value_error()

    def assert_value_error(self):
        thrown = False
        try:
            self.run_app()
        except ValueError:
            thrown = True
        self.assertTrue(thrown)
