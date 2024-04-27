import unittest

from pycolorecho.__main__ import Validate


class TestValidate(unittest.TestCase):
    """Unit test cases for Validate class."""

    def testValidate_range_valid(self):
        Validate.validate_range([150], [100, 200], "Valid")

    def testValidate_range_invalid(self):
        with self.assertRaises(ValueError):
            Validate.validate_range([50], [100, 200], "Invalid")

    def testValidate_type_valid(self):
        Validate.validate_type('test', str, "Valid")

    def testValidate_type_invalid(self):
        with self.assertRaises(TypeError):
            Validate.validate_type(100, str, "Invalid")

    def testValidate_hex_valid(self):
        Validate.validate_hex('#FFFFFF')

    def testValidate_hex_invalid_1(self):
        with self.assertRaises(ValueError):
            Validate.validate_hex('FG3452')

    def testValidate_hex_invalid_2(self):
        with self.assertRaises(TypeError):
            Validate.validate_hex(100)

    def testValidate_rgb_valid(self):
        Validate.validate_rgb(255, 255, 255)

    def testValidate_rgb_invalid_1(self):
        with self.assertRaises(ValueError):
            Validate.validate_rgb(300, 255, 255)

    def testValidate_rgb_invalid_2(self):
        with self.assertRaises(TypeError):
            Validate.validate_rgb('255', 255, 255)

    def testValidate_rgb_invalid_3(self):
        with self.assertRaises(ValueError):
            Validate.validate_rgb(255, 255, 255, 255)

    def testValidate_rgb_invalid_4(self):
        with self.assertRaises(ValueError):
            Validate.validate_rgb(255)

    def testValidate_cmyk_valid(self):
        Validate.validate_cmyk(1.0, 1.0, 1.0, 1.0)

    def testValidate_cmyk_invalid_1(self):
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(2.0, 1.0, 1.0, 1.0)

    def testValidate_cmyk_invalid_2(self):
        with self.assertRaises(TypeError):
            Validate.validate_cmyk('1.0', 1.0, 1.0, 1.0)

    def testValidate_cmyk_invalid_3(self):
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(1.0, 1.0, 1.0, 1.0, 1.0)

    def testValidate_cmyk_invalid_4(self):
        with self.assertRaises(ValueError):
            Validate.validate_cmyk(1.0)

    def testValidate_ansi_valid_true_color_background(self):
        Validate.validate_ansi('\033[48;2;255;255;255m')

    def testValidate_ansi_valid_true_color_foreground(self):
        Validate.validate_ansi('\033[38;2;255;255;255m')

    def testValidate_ansi_valid_standard_color(self):
        Validate.validate_ansi('\033[107m')

    def testValidate_ansi_valid_x1b_format(self):
        Validate.validate_ansi('\x1b[107m')

    def testValidate_ansi_invalid_1(self):
        with self.assertRaises(TypeError):
            Validate.validate_ansi(100)

    def testValidate_ansi_invalid_2(self):
        with self.assertRaises(ValueError):
            Validate.validate_ansi('100')


if __name__ == "__main__":
    unittest.main()
