import unittest

from pycolorecho import ColorMapper, TextColor


class TestColorMapper(unittest.TestCase):
    """Unit test cases for ColorMapper class."""

    def test_get_mapping_valid(self):
        """Test if the get mapping works as expected."""
        colorization = ColorMapper()
        colorization.add_mapping('error', ['error'], text_color=TextColor.RED)
        expected_output = {
            'keywords': ['error'],
            'color_mapping': {
                'text_color': TextColor.RED,
                'text_background_color': None,
                'text_effect': None,
                'text_case': 0
            },
            'flags': {
                'ignore_case': False,
                'color_match': False
            }
        }
        self.assertDictEqual(expected_output, colorization.get_mapping('error'))

    def test_get_mapping_do_not_exist(self):
        """Test if the get mapping raises ValueError as expected."""
        colorization = ColorMapper()
        with self.assertRaises(ValueError):
            colorization.get_mapping('error')

    def test_get_mappings_no_input(self):
        """Test if the get mappings works as expected."""
        colorization = ColorMapper()
        self.assertEqual(0, len(colorization.get_mappings()))

    def test_get_mappings_valid(self):
        """Test if the get mappings works as expected."""
        colorization = ColorMapper()
        colorization.add_mapping('error', ['error'], text_color=TextColor.RED)
        self.assertEqual(1, len(colorization.get_mappings()))

    def test_is_valid_mapping_exists(self):
        """Test if is valid mappings works as expected."""
        colorization = ColorMapper()
        colorization.add_mapping('error', ['error'], text_color=TextColor.RED)
        self.assertTrue(colorization.is_valid_mapping('error'))

    def test_is_valid_mapping_do_not_exists(self):
        """Test if is valid mappings works as expected."""
        colorization = ColorMapper()
        self.assertFalse(colorization.is_valid_mapping('error'))

    def test_remove_mapping_valid(self):
        """Test if the remove mapping works as expected."""
        colorization = ColorMapper()
        colorization.add_mapping('error', ['error'], text_color=TextColor.RED)
        colorization.remove_mapping('error')
        self.assertFalse(colorization.is_valid_mapping('error'))

    def test_remove_mapping_do_not_exist(self):
        """Test if the remove mapping works as expected."""
        colorization = ColorMapper()
        colorization.remove_mapping('error')

    def test_add_mapping_valid(self):
        """Test if the add mapping works as expected."""
        colorization = ColorMapper()
        colorization.add_mapping('error', ['error'], text_color=TextColor.RED)
        self.assertTrue(colorization.is_valid_mapping('error'))


if __name__ == "__main__":
    unittest.main()
