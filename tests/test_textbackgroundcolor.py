import io
import sys
import unittest

from pycolorecho import TextBackgroundColor, RESET


class TestTextBackgroundColor(unittest.TestCase):
    """Unit test cases for TextBackgroundColor class."""

    def setUp(self) -> None:
        self._true_new_color_name = 'CUSTOM_1'
        self._true_new_color_code = '\033[48;2;176;191;26m'

        self._standard_new_color_name = 'CUSTOM_2'
        self._standard_new_color_code = '\033[108m'

    def tearDown(self) -> None:
        TextBackgroundColor.remove_color(self._true_new_color_name)
        TextBackgroundColor.remove_color(self._standard_new_color_name, true_color=False)

    def test_variable_names(self):
        color_variables = [
            name for name, value in vars(TextBackgroundColor).items()
            if isinstance(value, str) and name != '__module__'
        ]
        for name in color_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')

    def test_add_color_true_valid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
        self.assertEqual(self._true_new_color_code, actual_value)

    def test_add_color_standard_valid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)

    def test_add_color_true_invalid(self):
        with self.assertRaises(ValueError):
            TextBackgroundColor.add_color('CUSTOM_3', '\033[38;2;255m')

    def test_add_color_standard_invalid(self):
        with self.assertRaises(ValueError):
            TextBackgroundColor.add_color('CUSTOM_4', '\033[38;2m', true_color=False)

    def test_get_colors_true(self):
        self.assertEqual(5, len(TextBackgroundColor.get_colors()))

    def test_get_colors_standard(self):
        self.assertEqual(8, len(TextBackgroundColor.get_colors(False)))

    def test_get_color_true_valid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
        self.assertEqual(self._true_new_color_code, actual_value)

    def test_get_color_standard_valid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)

    def test_get_color_true_unavailable(self):
        with self.assertRaises(ValueError):
            TextBackgroundColor.get_color('JUNK')

    def test_get_color_standard_unavailable(self):
        with self.assertRaises(ValueError):
            TextBackgroundColor.get_color('JUNK', true_color=False)

    def test_is_true_color_valid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        self.assertTrue(TextBackgroundColor.is_true_color(self._true_new_color_name))

    def test_is_true_color_invalid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertFalse(TextBackgroundColor.is_true_color(self._standard_new_color_name))

    def test_is_standard_color_valid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertTrue(TextBackgroundColor.is_standard_color(self._standard_new_color_name))

    def test_is_standard_color_invalid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        self.assertFalse(TextBackgroundColor.is_standard_color(self._true_new_color_name))

    def test_is_valid_color_true_valid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        self.assertTrue(TextBackgroundColor.is_valid_color(self._true_new_color_name))

    def test_is_valid_color_standard_valid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertTrue(TextBackgroundColor.is_valid_color(self._standard_new_color_name, true_color=False))

    def test_is_valid_color_true_unavailable(self):
        self.assertFalse(TextBackgroundColor.is_valid_color('JUNK'))

    def test_is_valid_color_standard_unavailable(self):
        self.assertFalse(TextBackgroundColor.is_valid_color('JUNK', true_color=False))

    def test_remove_color_true_valid(self):
        TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
        actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
        self.assertEqual(self._true_new_color_code, actual_value)
        TextBackgroundColor.remove_color(self._true_new_color_name)
        self.assertFalse(TextBackgroundColor.is_valid_color(self._true_new_color_name))

    def test_remove_color_standard_valid(self):
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)
        TextBackgroundColor.remove_color(self._standard_new_color_name, true_color=False)
        self.assertFalse(TextBackgroundColor.is_valid_color(self._standard_new_color_name, true_color=False))

    def test_text_background_color_true(self):
        value = (
            f'{TextBackgroundColor.ACID_GREEN}'
            f'This is a test ACID GREEN background colored message'
            f'{RESET}'
        )
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        print(value)
        expected_value = f'{value}\n'
        sys.stdout = sys.__stdout__
        self.assertEqual(expected_value, output_buffer.getvalue())

    def test_text_background_color_standard(self):
        value = (
            f'{TextBackgroundColor.RED}'
            f'This is a test RED background colored message'
            f'{RESET}'
        )
        output_buffer = io.StringIO()
        sys.stdout = output_buffer
        print(value)
        expected_value = f'{value}\n'
        sys.stdout = sys.__stdout__
        self.assertEqual(expected_value, output_buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
