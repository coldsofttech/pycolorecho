import unittest

from pycolorecho import TextCase


class TestTextCase(unittest.TestCase):
    """Unit test cases for TextCase class."""

    def setUp(self) -> None:
        self.test_message1 = 'This is a test message@12345!'
        self.test_message2 = 'this is a TEST message_-24#@'

    def test_variable_names(self):
        """Test if names of all the constants are in upper case."""
        color_variables = [
            name for name, value in vars(TextCase).items()
            if isinstance(value, str) and not name.startswith('__')
        ]
        for name in color_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')

    def test_get_cases(self):
        """Test if the get cases works as expected."""
        self.assertEqual(10, len(TextCase.get_cases()))

    def test_all_caps(self):
        """Test if all caps works as expected."""
        self.assertEqual(
            'THIS IS A TEST MESSAGE@12345!',
            TextCase.convert_text(self.test_message1, TextCase.ALL_CAPS)
        )

    def test_camel_case(self):
        """Test if camel case works as expected."""
        self.assertEqual(
            'thisIsATestMessage_24',
            TextCase.convert_text(self.test_message2, TextCase.CAMEL_CASE)
        )

    def test_kebab_case(self):
        """Test if kebab case works as expected."""
        self.assertEqual(
            'this-is-a-test-message-24',
            TextCase.convert_text(self.test_message2, TextCase.KEBAB_CASE)
        )

    def test_no_caps(self):
        """Test if no caps works as expected."""
        self.assertEqual(
            'this is a test message@12345!',
            TextCase.convert_text(self.test_message1, TextCase.NO_CAPS)
        )

    def test_pascal_case(self):
        """Test if pascal case works as expected."""
        self.assertEqual(
            'ThisIsATestMessage24',
            TextCase.convert_text(self.test_message2, TextCase.PASCAL_CASE)
        )

    def test_sentence_case(self):
        """Test if sentence case works as expected."""
        self.assertEqual(
            'This is a test message_-24#@',
            TextCase.convert_text(self.test_message2, TextCase.SENTENCE_CASE)
        )

    def test_snake_case(self):
        """Test if snake case works as expected."""
        self.assertEqual(
            'this_is_a_test_message_24',
            TextCase.convert_text(self.test_message2, TextCase.SNAKE_CASE)
        )

    def test_title_case(self):
        """Test if title case works as expected."""
        self.assertEqual(
            'This Is A Test Message_-24#@',
            TextCase.convert_text(self.test_message2, TextCase.TITLE_CASE)
        )

    def test_none(self):
        """Test if none works as expected."""
        self.assertEqual(
            self.test_message1,
            TextCase.convert_text(self.test_message1, TextCase.NONE)
        )


if __name__ == "__main__":
    unittest.main()
