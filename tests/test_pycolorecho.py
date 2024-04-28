import unittest

from pycolorecho import RESET, TextColor, TextBackgroundColor, TextEffect, TextCase, ColorMapper
from pycolorecho.__main__ import _get_colorize_sequence, _get_colorized_message, \
    _get_colorized_message_by_regex_pattern, _get_colorized_message_by_mappings


class TestPyColorEcho(unittest.TestCase):
    """
    Unit test cases for pycolorecho package.
    Note: Although test cases regarding echo are not applicable or necessary, it was observed that
    assertions fail due to complexities involving multiple layers, the output buffer of echo, and
    actual printing. Nevertheless, all essential test cases for underlying methods have been ensured,
    including obtaining colorized messages, obtaining colorized messages using regex patterns, and
    obtaining colorized messages using mappings.
    """

    def test_reset_property(self):
        """Test if reset value is as expected."""
        expected_value = '\033[0m'
        self.assertEqual(RESET, expected_value)

    def test_get_colorize_sequence(self):
        """Test if the get colorize sequence works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
        )
        self.assertEqual(
            expected_value,
            _get_colorize_sequence(
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD
            )
        )

    def test_get_colorize_sequence_text_color(self):
        """Test if the get colorize sequence works as expected."""
        expected_value = f'{TextColor.RED}'
        self.assertEqual(expected_value, _get_colorize_sequence(text_color=TextColor.RED))

    def test_get_colorize_sequence_text_background_color(self):
        """Test if the get colorize sequence works as expected."""
        expected_value = f'{TextBackgroundColor.ACID_GREEN}'
        self.assertEqual(expected_value, _get_colorize_sequence(text_background_color=TextBackgroundColor.ACID_GREEN))

    def test_get_colorize_sequence_text_effect(self):
        """Test if the get colorize sequence works as expected."""
        expected_value = f'{TextEffect.BOLD}'
        self.assertEqual(expected_value, _get_colorize_sequence(text_effect=TextEffect.BOLD))

    def test_get_colorized_message(self):
        """Test if the get colorized message works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'this-is-a-test-message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message(
                message='This is a test message',
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD,
                text_case=TextCase.KEBAB_CASE
            )
        )

    def test_get_colorized_message_none(self):
        """Test if the get colorized message works as expected."""
        expected_value = 'This is a test message'
        self.assertEqual(
            expected_value,
            _get_colorized_message('This is a test message')
        )

    def test_get_colorized_message_text_color(self):
        """Test if the get colorized message works as expected."""
        expected_value = (
            f'{TextColor.RED}This is a test message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message(
                message='This is a test message',
                text_color=TextColor.RED
            )
        )

    def test_get_colorized_message_text_background_color(self):
        """Test if the get colorized message works as expected."""
        expected_value = (
            f'{TextBackgroundColor.ACID_GREEN}This is a test message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message(
                message='This is a test message',
                text_background_color=TextBackgroundColor.ACID_GREEN
            )
        )

    def test_get_colorized_message_text_effect(self):
        """Test if the get colorized message works as expected."""
        expected_value = (
            f'{TextEffect.BOLD}This is a test message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message(
                message='This is a test message',
                text_effect=TextEffect.BOLD
            )
        )

    def test_get_colorized_message_text_case(self):
        """Test if the get colorized message works as expected."""
        expected_value = 'this-is-a-test-message'
        self.assertEqual(
            expected_value,
            _get_colorized_message(
                message='This is a test message',
                text_case=TextCase.KEBAB_CASE
            )
        )

    def test_get_colorized_message_by_regex_pattern_1(self):
        """Test if the get colorized message by regex pattern works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'this-is-a-test-message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_regex_pattern(
                message='This is a test message',
                regex_pattern=r'test',
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD,
                text_case=TextCase.KEBAB_CASE
            )
        )

    def test_get_colorized_message_by_regex_pattern_2(self):
        """Test if the get colorized message by regex pattern works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'this-is-a-test-message{RESET}'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_regex_pattern(
                message='This is a test message',
                regex_pattern=r'TEST',
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD,
                text_case=TextCase.KEBAB_CASE,
                ignore_case=True
            )
        )

    def test_get_colorized_message_by_regex_pattern_3(self):
        """Test if the get colorized message by regex pattern works as expected."""
        expected_value = (
            f'This is a {TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'test{RESET} message'
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_regex_pattern(
                message='This is a test message',
                regex_pattern=r'test',
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD,
                text_case=TextCase.KEBAB_CASE,
                color_match=True
            )
        )

    def test_get_colorized_message_by_regex_pattern_4(self):
        """Test if the get colorized message by regex pattern works as expected."""
        expected_value = 'This is a test message'
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_regex_pattern(
                message='This is a test message',
                regex_pattern=r'nottest',
                text_color=TextColor.RED,
                text_background_color=TextBackgroundColor.ACID_GREEN,
                text_effect=TextEffect.BOLD,
                text_case=TextCase.KEBAB_CASE,
                color_match=True
            )
        )

    def test_get_colorized_message_by_mappings_1(self):
        """Test if the get colorized message by mappings works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'this-is-a-test-message{RESET}'
        )
        colorization = ColorMapper()
        colorization.add_mapping(
            name='test',
            keywords='test',
            text_color=TextColor.RED,
            text_background_color=TextBackgroundColor.ACID_GREEN,
            text_effect=TextEffect.BOLD,
            text_case=TextCase.KEBAB_CASE
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_mappings(
                message='This is a test message',
                mappings=colorization
            )
        )

    def test_get_colorized_message_by_mappings_2(self):
        """Test if the get colorized message by mappings works as expected."""
        expected_value = (
            f'{TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'this-is-a-test-message{RESET}'
        )
        colorization = ColorMapper()
        colorization.add_mapping(
            name='test',
            keywords=r'TEST',
            text_color=TextColor.RED,
            text_background_color=TextBackgroundColor.ACID_GREEN,
            text_effect=TextEffect.BOLD,
            text_case=TextCase.KEBAB_CASE,
            ignore_case=True
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_mappings(
                message='This is a test message',
                mappings=colorization
            )
        )

    def test_get_colorized_message_by_mappings_3(self):
        """Test if the get colorized message by mappings works as expected."""
        expected_value = (
            f'This is a {TextColor.RED}{TextBackgroundColor.ACID_GREEN}{TextEffect.BOLD}'
            f'test{RESET} message'
        )
        colorization = ColorMapper()
        colorization.add_mapping(
            name='test',
            keywords=r'test',
            text_color=TextColor.RED,
            text_background_color=TextBackgroundColor.ACID_GREEN,
            text_effect=TextEffect.BOLD,
            text_case=TextCase.KEBAB_CASE,
            color_match=True
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_mappings(
                message='This is a test message',
                mappings=colorization
            )
        )

    def test_get_colorized_message_by_mappings_4(self):
        """Test if the get colorized message by mappings works as expected."""
        expected_value = 'This is a test message'
        colorization = ColorMapper()
        colorization.add_mapping(
            name='test',
            keywords=r'nottest',
            text_color=TextColor.RED,
            text_background_color=TextBackgroundColor.ACID_GREEN,
            text_effect=TextEffect.BOLD,
            text_case=TextCase.KEBAB_CASE,
            color_match=True
        )
        self.assertEqual(
            expected_value,
            _get_colorized_message_by_mappings(
                message='This is a test message',
                mappings=colorization
            )
        )


if __name__ == "__main__":
    unittest.main()
