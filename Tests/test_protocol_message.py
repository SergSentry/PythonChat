import unittest

from Protocol.Messages import *


class MessageProtocolTest(unittest.TestCase):
    def test_presence_message(self):
        self.assertDictEqual(
            presence_message("Serg"),
            {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: 'Serg'
                }
            }
        )


if __name__ == '__main__':
    unittest.main()
