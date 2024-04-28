import re
import unittest

from pycolorecho import HEXCodes


class TestHEXCodes(unittest.TestCase):
    """Unit test cases for _HEXCodes class."""

    def test_hex_code_format(self):
        """Test if values of all the constants are in HEX format."""
        hex_codes = [
            value for name, value in vars(HEXCodes).items()
            if isinstance(value, str) and not name.startswith('__')
        ]
        if not re.match(r'^#[0-9A-Fa-f]{6}$', hex_codes[0]):
            hex_codes = hex_codes[1:]
        for hex_code in hex_codes:
            self.assertTrue(re.match(r'^#[0-9A-Fa-f]{6}$', hex_code), f'{hex_code} is not in HEX format.')

    def test_variable_names(self):
        """Test if names of all the constants are in upper case."""
        hex_variables = [
            name for name, value in vars(HEXCodes).items()
            if isinstance(value, str) and not name.startswith('__')
        ]
        for name in hex_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')


if __name__ == "__main__":
    unittest.main()
