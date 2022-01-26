import unittest
import main


class MyTestCase(unittest.TestCase):  # unittest.TestCase is a base class used to run tests
    def test_start_up(self):  # Python tests need to start with the prefix "test...". Self is the instance of the class(kind of like "this" in java)
        self.assertEqual(0, main.test())  # add assertions here


if __name__ == '__main__':
    unittest.main()
