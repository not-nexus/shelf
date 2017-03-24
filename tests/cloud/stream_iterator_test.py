import pyproctor
from shelf.cloud.stream_iterator import StreamIterator
from mock import Mock


class StreamIteratorTest(pyproctor.TestBase):
    def test_next(self):
        val = "hello"
        logger = type("FakeLogger", (object, ), {
            "info": Mock()
        })
        key = type("FakeKey", (object, ), {
            "open_read": Mock(),
            "name": "hi"
        })
        key.next = Mock(return_value=val)
        key.bucket = type("FakeBucket", (object, ), {
            "name": "test"
        })
        StreamIterator.BYTE_LOG_INCREMENT = 1
        iterator = StreamIterator(key, logger)
        iterator.request_id = "ABC123"
        result = iterator.next()
        self.assertEqual(val, result)
        logger.info.assert_called_with("ABC123 - Downloading test/artifact/hi: 5 bytes")
