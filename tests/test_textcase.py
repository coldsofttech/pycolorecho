import unittest

from pycolorecho import TextCase


class TestTextCase(unittest.TestCase):
    """Unit test cases for TextCase class."""

    def setUp(self) -> None:
        self.test_message1 = 'This is a test message@12345!'
        self.test_message2 = 'this is a TEST message_-24#@'

    def test_variable_names(self):
        color_variables = [
            name for name, value in vars(TextCase).items()
            if isinstance(value, str) and name != '__module__'
        ]
        for name in color_variables:
            if not name.isupper():
                self.fail(f'{name} variable name is not all uppercase.')

    def test_get_cases(self):
        self.assertEqual(10, len(TextCase.get_cases()))

    def test_all_caps(self):
        self.assertEqual(
            'THIS IS A TEST MESSAGE@12345!',
            TextCase.convert_text(self.test_message1, TextCase.ALL_CAPS)
        )

    def test_camel_case(self):
        self.assertEqual(
            'thisIsATestMessage_24',
            TextCase.convert_text(self.test_message2, TextCase.CAMEL_CASE)
        )

    def test_kebab_case(self):
        self.assertEqual(
            'this-is-a-test-message-24',
            TextCase.convert_text(self.test_message2, TextCase.KEBAB_CASE)
        )

    def test_no_caps(self):
        self.assertEqual(
            'this is a test message@12345!',
            TextCase.convert_text(self.test_message1, TextCase.NO_CAPS)
        )

    def test_pascal_case(self):
        self.assertEqual(
            'ThisIsATestMessage24',
            TextCase.convert_text(self.test_message2, TextCase.PASCAL_CASE)
        )

    def test_sentence_case(self):
        self.assertEqual(
            'This is a test message_-24#@',
            TextCase.convert_text(self.test_message2, TextCase.SENTENCE_CASE)
        )

    def test_snake_case(self):
        self.assertEqual(
            'this_is_a_test_message_24',
            TextCase.convert_text(self.test_message2, TextCase.SNAKE_CASE)
        )

    def test_title_case(self):
        self.assertEqual(
            'This Is A Test Message_-24#@',
            TextCase.convert_text(self.test_message2, TextCase.TITLE_CASE)
        )

    def test_none(self):
        self.assertEqual(
            self.test_message1,
            TextCase.convert_text(self.test_message1, TextCase.NONE)
        )


if __name__ == "__main__":
    unittest.main()
