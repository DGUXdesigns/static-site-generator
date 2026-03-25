import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        result = extract_title("# Hello")

        self.assertEqual(result, "Hello")


if __name__ == "__main__":
    unittest.main()
