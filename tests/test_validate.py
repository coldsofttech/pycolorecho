import unittest

from pycolorecho.__main__ import Validate


class TestValidate(unittest.TestCase):
    """Unit test cases for Validate class."""

    def test_validate_range_valid(self):
        """Test if the validate range works as expected."""
        Validate.validate_range([150], [100, 200], "Valid")

    def test_validate_range_invalid(self):
        """Test if the validate range raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_range([50], [100, 200], "Invalid")

    def test_validate_type_valid(self):
        """Test if the validate type works as expected."""
        Validate.validate_type('test', str, "Valid")

    def test_validate_type_invalid(self):
        """Test if the validate type raises TypeError as expected."""
        with self.assertRaises(TypeError):
            Validate.validate_type(100, str, "Invalid")

    def test_validate_hex_valid(self):
        """Test if the validate hex works as expected."""
        Validate.validate_hex('#FFFFFF')

    def test_validate_hex_invalid_1(self):
        """Test if the validate hex raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_hex('FG3452')

    def test_validate_hex_invalid_2(self):
        """Test if the validate hex raises TypeError as expected."""
        with self.assertRaises(TypeError):
            Validate.validate_hex(100)

    def test_validate_rgb_valid(self):
        """Test if the validate rgb works as expected."""
        Validate.validate_rgb(255, 255, 255)

    def test_validate_rgb_invalid_1(self):
        """Test if the validate rgb raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_rgb(300, 255, 255)

    def test_validate_rgb_invalid_2(self):
        """Test if the validate rgb raises TypeError as expected."""
        with self.assertRaises(TypeError):
            Validate.validate_rgb('255', 255, 255)

    def test_validate_rgb_invalid_3(self):
        """Test if the validate rgb raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_rgb(255, 255, 255, 255)

    def test_validate_rgb_invalid_4(self):
        """Test if the validate rgb raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_rgb(255)

    def test_validate_cmyk_valid(self):
        """Test if the validate cmyk works as expected."""
        Validate.validate_cmyk(1.0, 1.0, 1.0, 1.0)

    def test_validate_cmyk_invalid_1(self):
        """Test if the validate cmyk raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(2.0, 1.0, 1.0, 1.0)

    def test_validate_cmyk_invalid_2(self):
        """Test if the validate cmyk raises TypeError as expected."""
        with self.assertRaises(TypeError):
            Validate.validate_cmyk('1.0', 1.0, 1.0, 1.0)

    def test_validate_cmyk_invalid_3(self):
        """Test if the validate cmyk raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(1.0, 1.0, 1.0, 1.0, 1.0)

    def test_validate_cmyk_invalid_4(self):
        """Test if the validate cmyk raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(1.0)

    def test_validate_ansi_valid_true_color_background(self):
        """Test if the validate ansi works as expected."""
        Validate.validate_ansi('\033[48;2;255;255;255m')

    def test_validate_ansi_valid_true_color_foreground(self):
        """Test if the validate ansi works as expected."""
        Validate.validate_ansi('\033[38;2;255;255;255m')

    def test_validate_ansi_valid_standard_color(self):
        """Test if the validate ansi works as expected."""
        Validate.validate_ansi('\033[107m')

    def testValidate_ansi_valid_x1b_format(self):
        """Test if the validate ansi works as expected."""
        Validate.validate_ansi('\x1b[107m')

    def test_validate_ansi_invalid_1(self):
        """Test if the validate ansi raises TypeError as expected."""
        with self.assertRaises(TypeError):
            Validate.validate_ansi(100)

    def test_validate_ansi_invalid_2(self):
        """Test if the validate ansi raises ValueError as expected."""
        with self.assertRaises(ValueError):
            Validate.validate_ansi('100')


if __name__ == "__main__":
    unittest.main()
