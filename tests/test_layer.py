import unittest

from pycolorecho import Layer


class TestLayer(unittest.TestCase):
    """Unit test cases for Layer class."""

    def test_foreground(self):
        self.assertEqual(38, Layer.Foreground.value)

    def test_background(self):
        self.assertEqual(48, Layer.Background.value)


if __name__ == "__main__":
    unittest.main()
