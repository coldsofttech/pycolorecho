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
        """Test if names of all the constants are in upper case."""
        color_variables = [
            name for name, value in vars(TextBackgroundColor).items()
            if isinstance(value, str) and not name.startswith('__')
        ]
        for name in color_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')

    def test_add_color_true_valid(self):
        """Test if the add color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
            self.assertEqual(self._true_new_color_code, actual_value)
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_add_color_standard_valid(self):
        """Test if the add color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)

    def test_add_color_true_invalid(self):
        """Test if the add color raises Warning or ValueError as expected."""
        with self.assertRaises(Exception) as context:
            TextBackgroundColor.add_color('CUSTOM_3', '\033[38;2;255m')

        self.assertTrue(isinstance(context.exception, (ValueError, Warning)))

    def test_add_color_standard_invalid(self):
        """Test if the add color raises ValueError as expected."""
        with self.assertRaises(ValueError):
            TextBackgroundColor.add_color('CUSTOM_4', '\033[38;2m', true_color=False)

    def test_get_colors_true(self):
        """Test if the get colors works as expected."""
        self.assertEqual(5, len(TextBackgroundColor.get_colors()))

    def test_get_colors_standard(self):
        """Test if the get colors works as expected."""
        self.assertEqual(8, len(TextBackgroundColor.get_colors(False)))

    def test_get_color_true_valid(self):
        """Test if the get color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
            self.assertEqual(self._true_new_color_code, actual_value)
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_get_color_standard_valid(self):
        """Test if the get color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)

    def test_get_color_true_unavailable(self):
        """Test if the get color works as expected."""
        with self.assertRaises(ValueError):
            TextBackgroundColor.get_color('JUNK')

    def test_get_color_standard_unavailable(self):
        """Test if the get color works as expected."""
        with self.assertRaises(ValueError):
            TextBackgroundColor.get_color('JUNK', true_color=False)

    def test_is_true_color_valid(self):
        """Test if is true color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            self.assertTrue(TextBackgroundColor.is_true_color(self._true_new_color_name))
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_is_true_color_invalid(self):
        """Test if is true color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertFalse(TextBackgroundColor.is_true_color(self._standard_new_color_name))

    def test_is_standard_color_valid(self):
        """Test if is standard color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertTrue(TextBackgroundColor.is_standard_color(self._standard_new_color_name))

    def test_is_standard_color_invalid(self):
        """Test if is standard color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            self.assertFalse(TextBackgroundColor.is_standard_color(self._true_new_color_name))
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_is_valid_color_true_valid(self):
        """Test if is valid color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            self.assertTrue(TextBackgroundColor.is_valid_color(self._true_new_color_name))
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_is_valid_color_standard_valid(self):
        """Test if is valid color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        self.assertTrue(TextBackgroundColor.is_valid_color(self._standard_new_color_name, true_color=False))

    def test_is_valid_color_true_unavailable(self):
        """Test if is valid color works as expected."""
        self.assertFalse(TextBackgroundColor.is_valid_color('JUNK'))

    def test_is_valid_color_standard_unavailable(self):
        """Test if is valid color works as expected."""
        self.assertFalse(TextBackgroundColor.is_valid_color('JUNK', true_color=False))

    def test_remove_color_true_valid(self):
        """Test if the remove color works as expected."""
        try:
            TextBackgroundColor.add_color(self._true_new_color_name, self._true_new_color_code)
            actual_value = TextBackgroundColor.get_color(self._true_new_color_name)
            self.assertEqual(self._true_new_color_code, actual_value)
            TextBackgroundColor.remove_color(self._true_new_color_name)
            self.assertFalse(TextBackgroundColor.is_valid_color(self._true_new_color_name))
        except Warning as e:
            self.skipTest(f'Skipping due to "{e}"')

    def test_remove_color_standard_valid(self):
        """Test if the remove color works as expected."""
        TextBackgroundColor.add_color(self._standard_new_color_name, self._standard_new_color_code, true_color=False)
        actual_value = TextBackgroundColor.get_color(self._standard_new_color_name, true_color=False)
        self.assertEqual(self._standard_new_color_code, actual_value)
        TextBackgroundColor.remove_color(self._standard_new_color_name, true_color=False)
        self.assertFalse(TextBackgroundColor.is_valid_color(self._standard_new_color_name, true_color=False))

    def test_text_background_color_true(self):
        """Test if text background colors as works as expected."""
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
        """Test if text background colors as works as expected."""
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
