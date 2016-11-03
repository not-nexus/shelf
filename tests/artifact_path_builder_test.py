from tests.unit_test_base import UnitTestBase
from shelf.artifact_path_builder import ArtifactPathBuilder


class ArtifactPathBuilderTest(UnitTestBase):
    def test_build(self):
        builder = ArtifactPathBuilder("my-bucket")
        url = builder.build("/path/to/artifact")
        self.assertEqual("/my-bucket/artifact/path/to/artifact", url)
