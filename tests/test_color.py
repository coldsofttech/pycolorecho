import unittest

from pycolorecho import Color, Layer


class TestColor(unittest.TestCase):
    """Unit test cases for Color class."""

    def test_validate_layer_valid(self):
        Color._validate_layer(Layer.Foreground)

    def test_validate_layer_invalid(self):
        with self.assertRaises(TypeError):
            Color._validate_layer(100)

    def test_hex_to_rgb(self):
        expected_value = (255, 255, 255)
        self.assertEqual(expected_value, Color.hex_to_rgb('#FFFFFF'))

    def test_rgb_to_hex(self):
        expected_value = '#FFFFFF'
        self.assertEqual(expected_value, Color.rgb_to_hex(255, 255, 255))

    def test_cmyk_to_rgb(self):
        expected_value = (255, 255, 255)
        self.assertEqual(expected_value, Color.cmyk_to_rgb(0.0, 0.0, 0.0, 0.0))

    def test_rgb_to_cmyk(self):
        expected_value = (0.0, 0.0, 0.0, 0.0)
        self.assertEqual(expected_value, Color.rgb_to_cmyk(255, 255, 255))

    def test_hex_to_ansi_valid_true_color_background(self):
        expected_value = '\033[48;2;255;255;255m'
        self.assertEqual(expected_value, Color.hex_to_ansi('#FFFFFF', Layer.Background))

    def test_hex_to_ansi_valid_true_color_foreground(self):
        expected_value = '\033[38;2;255;255;255m'
        self.assertEqual(expected_value, Color.hex_to_ansi('#FFFFFF', Layer.Foreground))

    def test_hex_to_ansi_valid_standard_color_background(self):
        expected_value = '\033[107m'
        self.assertEqual(expected_value, Color.hex_to_ansi('#FFFFFF', Layer.Background, true_color=False))

    def test_hex_to_ansi_valid_standard_color_foreground(self):
        expected_value = '\033[97m'
        self.assertEqual(expected_value, Color.hex_to_ansi('#FFFFFF', Layer.Foreground, true_color=False))

    def test_ansi_to_hex_valid_true_color_background(self):
        expected_value = '#FFFFFF'
        self.assertEqual(expected_value, Color.ansi_to_hex('\033[48;2;255;255;255m'))

    def test_ansi_to_hex_valid_true_color_foreground(self):
        expected_value = '#FFFFFF'
        self.assertEqual(expected_value, Color.ansi_to_hex('\033[38;2;255;255;255m'))

    def test_ansi_to_hex_warning_standard_color(self):
        with self.assertRaises(Warning):
            Color.ansi_to_hex('\033[107m')

    def test_rgb_to_ansi_valid_true_color_background(self):
        expected_value = '\033[48;2;255;255;255m'
        self.assertEqual(expected_value, Color.rgb_to_ansi(255, 255, 255, Layer.Background))

    def test_rgb_to_ansi_valid_true_color_foreground(self):
        expected_value = '\033[38;2;255;255;255m'
        self.assertEqual(expected_value, Color.rgb_to_ansi(255, 255, 255, Layer.Foreground))

    def test_rgb_to_ansi_valid_standard_color_background(self):
        expected_value = '\033[107m'
        self.assertEqual(expected_value, Color.rgb_to_ansi(255, 255, 255, Layer.Background, true_color=False))

    def test_rgb_to_ansi_valid_standard_color_foreground(self):
        expected_value = '\033[97m'
        self.assertEqual(expected_value, Color.rgb_to_ansi(255, 255, 255, Layer.Foreground, true_color=False))

    def test_ansi_to_rgb_valid_true_color_background(self):
        expected_value = (255, 255, 255)
        self.assertEqual(expected_value, Color.ansi_to_rgb('\033[48;2;255;255;255m'))

    def test_ansi_to_rgb_valid_true_color_foreground(self):
        expected_value = (255, 255, 255)
        self.assertEqual(expected_value, Color.ansi_to_rgb('\033[38;2;255;255;255m'))

    def test_ansi_to_rgb_warning_standard_color(self):
        with self.assertRaises(Warning):
            Color.ansi_to_rgb('\033[107m')

    def test_cmyk_to_ansi_valid_true_color_background(self):
        expected_value = '\033[48;2;255;255;255m'
        self.assertEqual(expected_value, Color.cmyk_to_ansi(0.0, 0.0, 0.0, 0.0, Layer.Background))

    def test_cmyk_to_ansi_valid_true_color_foreground(self):
        expected_value = '\033[38;2;255;255;255m'
        self.assertEqual(expected_value, Color.cmyk_to_ansi(0.0, 0.0, 0.0, 0.0, Layer.Foreground))

    def test_cmyk_to_ansi_valid_standard_color_background(self):
        expected_value = '\033[107m'
        self.assertEqual(expected_value, Color.cmyk_to_ansi(0.0, 0.0, 0.0, 0.0, Layer.Background, true_color=False))

    def test_cmyk_to_ansi_valid_standard_color_foreground(self):
        expected_value = '\033[97m'
        self.assertEqual(expected_value, Color.cmyk_to_ansi(0.0, 0.0, 0.0, 0.0, Layer.Foreground, true_color=False))

    def test_ansi_to_cmyk_valid_true_color_background(self):
        expected_value = (0.0, 0.0, 0.0, 0.0)
        self.assertEqual(expected_value, Color.ansi_to_cmyk('\033[48;2;255;255;255m'))

    def test_ansi_to_cmyk_valid_true_color_foreground(self):
        expected_value = (0.0, 0.0, 0.0, 0.0)
        self.assertEqual(expected_value, Color.ansi_to_cmyk('\033[38;2;255;255;255m'))

    def test_ansi_to_cmyk_warning_standard_color(self):
        with self.assertRaises(Warning):
            Color.ansi_to_rgb('\033[107m')


if __name__ == "__main__":
    unittest.main()
