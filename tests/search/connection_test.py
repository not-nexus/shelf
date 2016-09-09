import pyproctor
from pyshelf.search.connection import Connection


class ConnectionTest(pyproctor.TestBase):
    def test_https(self):
        # Ensuring use_ssl is set properly if https schema is passed in.
        con = Connection("https://localhost:9200/index")
        self.assertEqual("https://localhost:9200", con.transport.connection_pool.connection.base_url)
