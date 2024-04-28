import io
import sys
import unittest

from pycolorecho import TextEffect, RESET


class TestTextEffect(unittest.TestCase):
    """Unit test cases for TextEffect class."""

    def setUp(self) -> None:
        self._new_effect_name = 'CUSTOM_1'
        self._new_effect_code = '\033[5m'

    def tearDown(self) -> None:
        TextEffect.remove_effect(self._new_effect_name)

    def test_variable_names(self):
        """Test if names of all the constants are in upper case."""
        color_variables = [
            name for name, value in vars(TextEffect).items()
            if isinstance(value, str) and not name.startswith('__')
        ]
        for name in color_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')

    def test_add_effect_valid(self):
        """Test if the add effect works as expected."""
        TextEffect.add_effect(self._new_effect_name, self._new_effect_code)
        actual_value = TextEffect.get_effect(self._new_effect_name)
        self.assertEqual(self._new_effect_code, actual_value)

    def test_add_effect_invalid(self):
        """Test if the add effect raises ValueError as expected."""
        with self.assertRaises(ValueError):
            TextEffect.add_effect('CUSTOM_2', '\033[48;2;255m')

    def test_get_effects(self):
        """Test if the get effects works as expected."""
        self.assertEqual(5, len(TextEffect.get_effects()))

    def test_get_effect_valid(self):
        """Test if the get effect works as expected."""
        TextEffect.add_effect(self._new_effect_name, self._new_effect_code)
        actual_value = TextEffect.get_effect(self._new_effect_name)
        self.assertEqual(self._new_effect_code, actual_value)

    def test_get_effect_unavailable(self):
        """Test if the get effect works as expected."""
        with self.assertRaises(ValueError):
            TextEffect.get_effect('JUNK')

    def test_is_valid_effect_valid(self):
        """Test if is valid effect works as expected."""
        TextEffect.add_effect(self._new_effect_name, self._new_effect_code)
        self.assertTrue(TextEffect.is_valid_effect(self._new_effect_name))

    def test_is_valid_effect_unavailable(self):
        """Test if is valid effect works as expected."""
        self.assertFalse(TextEffect.is_valid_effect('JUNK'))

    def test_remove_effect_valid(self):
        """Test if the remove effect works as expected."""
        TextEffect.add_effect(self._new_effect_name, self._new_effect_code)
        actual_value = TextEffect.get_effect(self._new_effect_name)
        self.assertEqual(self._new_effect_code, actual_value)
        TextEffect.remove_effect(self._new_effect_name)
        self.assertFalse(TextEffect.is_valid_effect(self._new_effect_name))

    def test_text_effect(self):
        """Test if text effects as works as expected."""
        value = (
            f'{TextEffect.BOLD}'
            f'This is a test BOLD message'
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
