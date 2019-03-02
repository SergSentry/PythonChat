import unittest
from Protocol.Response import *


class ResponseProtocolTest(unittest.TestCase):
    def test_good_response_message(self):
        self.assertDictEqual(
            good_response(),
            {RESPONSE: GOOD_RESPONSE_COD}
        )


if __name__ == '__main__':
    unittest.main()
