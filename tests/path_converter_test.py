from tests.unit_test_base import UnitTestBase
from shelf.artifact_path_builder import ArtifactPathBuilder
from shelf.path_converter import PathConverter


class PathConverterTest(UnitTestBase):
    def setUp(self):
        super(PathConverterTest, self).setUp()
        builder = ArtifactPathBuilder("test")
        self.converter = PathConverter(builder)

    def test_from_cloud_metadata(self):
        path = "andy_gertjejansen/_metadata_test.txt.yaml"
        expected = "/test/artifact/andy_gertjejansen/test.txt"
        self.assertEqual(expected, self.converter.from_cloud_metadata(path))
