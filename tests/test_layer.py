import unittest

from pycolorecho import Layer


class TestLayer(unittest.TestCase):
    """Unit test cases for Layer class."""

    def test_foreground(self):
        """Test if the foreground value is as expected."""
        self.assertEqual(38, Layer.Foreground.value)

    def test_background(self):
        """Test if the background value is as expected."""
        self.assertEqual(48, Layer.Background.value)


if __name__ == "__main__":
    unittest.main()
