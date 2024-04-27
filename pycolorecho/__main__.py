import os
import re
import sys
from enum import Enum
from typing import Optional, Union

RESET: str = "\033[0m"


def _is_colorization_supported() -> bool:
    """
    Checks if the current operating system supports colorization.
    :return: True if colorization is supported, False otherwise.
    :rtype: bool
    """
    file_name = 'lm_color.temp'
    # Check for Windows operating systems
    if sys.platform == 'win32':
        major, minor = sys.getwindowsversion().major, sys.getwindowsversion().minor
        return major > 10 or (major == 10 and minor >= 0)

    # Check for Linux-based operating systems
    term = os.environ.get('TERM')
    if term is None:
        return False

    if 'color' in os.popen('tput colors').read():
        return True

    try:
        with open(file_name, 'w') as f:
            os.system('tput setaf 1')
            os.system('tput setab 0')
            os.system('echo -n "\033[1;31m"')
            os.system('echo -n "\033[0m')

        with open(file_name, 'r') as f:
            content = f.read()
            return '\033[1;31m' in content
    finally:
        os.remove(file_name)


def _is_true_color_supported() -> bool:
    """
    Verifies whether the true color format is supported by the current operating system and terminal.
    :return: True if true color format is supported, False otherwise.
    :rtype: bool
    """
    if os.name == 'nt':
        true_color_support = True
    else:
        true_color_support = os.getenv('COLORTERM') in ['truecolor', '24bit']

    return true_color_support


class Validate:
    """
    Internal utility class designed to facilitate validation across various scenarios.
    """

    @classmethod
    def validate_range(cls, values, expected_range, message) -> None:
        """
        Performs validation to ensure that the provided list of values falls within the expected range.
        If any value is outside the specified range, a ValueError is raised.
        :param values: The list of values to be validated.
        :param expected_range: The expected range (from and to) within which the values should fall.
        :param message: The message to be displayed when a ValueError is raised.
        """
        if not all(expected_range[0] <= x <= expected_range[1] for x in values):
            raise ValueError(message)

    @classmethod
    def validate_type(cls, value, expected_type, message) -> None:
        """
        Conducts validation to confirm that the provided value matches the expected type.
        If the value does not match the expected type, a ValueError is raised.
        :param value: The value to be validated.
        :param expected_type: The anticipated type for verification.
        :param message: The message to be displayed when a ValueError is raised.
        """
        if not isinstance(value, expected_type):
            raise TypeError(message)

    @classmethod
    def validate_hex(cls, hex_code: str) -> None:
        """
        Conducts validation to ensure that the provided value is in the correct HEX color format, namely #RRGGBB.
        :param hex_code: The value to be validated as a HEX color code.
        :type hex_code: str
        """
        cls.validate_type(hex_code, str, 'hex_code should be a string.')
        if not re.match(r'#[0-9a-fA-F]{6}$', hex_code.upper()):
            raise ValueError('Invalid HEX code format. Example: #RRGGBB.')

    @classmethod
    def validate_rgb(cls, *args) -> None:
        """
        Performs validation to ensure that the provided values for red (r), green (g), and blue (b)
        are in the correct format, specifically within the range of 0 to 255.
        :param args: The arguments representing red (r), green (g), and blue (b) values.
        """
        if len(args) != 3:
            raise ValueError('Exactly 3 arguments are required.')

        cls.validate_range(
            args,
            (0, 255),
            'Invalid RGB code format. RGB values should be in the range 0-255. Example: 127, 128, 255.'
        )

    @classmethod
    def validate_cmyk(cls, *args) -> None:
        """
        Performs validation to ensure that the provided values for cyan (c), magenta (m), yellow (y), and
        key (k) are in the correct format, specifically within the range of 0.0 to 1.0
        :param args: The arguments representing cyan (c), magenta (m), yellow (y), and key (k).
        """
        if len(args) != 4:
            raise ValueError('Exactly 4 arguments are required.')

        cls.validate_range(
            args,
            (0.0, 1.0),
            'Invalid CMYK code format. CMYK values should be in the range 0.0-1.0. Example: 0.7, 0.1, 1.0, 1.0.'
        )

    @classmethod
    def validate_ansi(cls, ansi: str) -> None:
        """
        Conducts validation to ensure that the provided ANSI code adheres to the expected format,
        supporting both true and standard color formats.
        :param ansi: The ANSI code to be validated.
        :type ansi: str
        """
        cls.validate_type(ansi, str, 'ansi should be a string.')

        if not re.match(r'^\033\[[0-9;]+m$', ansi) and not re.match(r'^\x1b\[[0-9;]+m$', ansi):
            raise ValueError('Invalid ANSI code format.')

        code = ansi[2:].rstrip('m')
        if not code.startswith('38;2;') and not code.startswith('48;2;') and not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')


class HEXCodes:
    """
    This supporting class encapsulates constants representing HEX code formats for various colors
    sourced from Wikipedia. For licensing information, please refer to the appropriate sources.
    """
    ABSOLUTE_ZERO: str = "#0048BA"
    ACID_GREEN: str = "#B0BF1A"
    AERO: str = "#7CB9E8"
    AFRICAN_VIOLET: str = "#B284BE"
    AIR_SUPERIORITY_BLUE: str = "#72A0C1"


class Layer(Enum):
    """
    Supplies enum-based options for different color layers within a terminal, such as Foreground and Background.
    """
    Foreground: int = 38
    Background: int = 48


class Color:
    """
    Utility class handling various color format conversions, including ANSI to RGB, RGB to CMYK, and others.

    Note: Some methods converting to ANSI currently do not support the standard color format.
    """

    @classmethod
    def _validate_layer(cls, layer: Layer) -> None:
        """
        Conducts validation to ensure that the provided layer value conforms to the expected format,
        i.e., it should be of the Layer enum type.
        :param layer: The layer value to be validated, expected to be of the Layer enum type.
        :type layer: Layer
        """
        Validate.validate_type(layer, Layer, 'layer should be of Layer type.')

    @classmethod
    def _hex_distance(cls, hex1: str, hex2: str) -> int:
        """
        Produces the closest RGB color value based on the provided inputs.
        The inputs consist of the HEX code of the standard color and the HEX code to identify the nearest value.
        Note: Exclude the '#' symbol before the HEX codes.
        :param hex1: The HEX code of the standard color.
        :type hex1: str
        :param hex2: The HEX code of the color to find the closest to.
        :type hex2: str
        :return: The integer-based closest RGB value for the provided inputs.
        :rtype: int
        """
        if len(hex1) != 6 or len(hex2) != 6:
            raise ValueError('Hex color values must be of length 6 (excluding # symbol)')

        r1, g1, b1 = tuple(int(hex1[i:i + 2], 16) for i in (0, 2, 4))
        r2, g2, b2 = tuple(int(hex2[i:i + 2], 16) for i in (0, 2, 4))
        return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

    @classmethod
    def _closest_standard_color(cls, hex_code: str) -> int:
        """
        Generates the nearest RGB color value based on the provided input. The input is a HEX code used
        to identify the closest color. This method utilizes standard colors and the provided HEX code to
        determine the nearest color value.
        :param hex_code: The HEX code of the color to find the closest match to.
        :type hex_code: str
        :return: The integer-based closest RGB value for the provided input.
        :rtype: int
        """
        standard_colors = [
            '000000', '800000', '008000', '808000',
            '000080', '800080', '008080', 'C0C0C0',
            '808080', 'FF0000', '00FF00', 'FFFF00',
            '0000FF', 'FF00FF', '00FFFF', 'FFFFFF'
        ]
        closest_color = min(standard_colors, key=lambda color: cls._hex_distance(hex_code, color))
        return standard_colors.index(closest_color) + 44

    @classmethod
    def hex_to_rgb(cls, hex_code: str) -> tuple[int, int, int]:
        """
        Converts the given color HEX code to RGB format.
        :param hex_code: The HEX code of the color to be converted.
        :type hex_code: str
        :return: The equivalent RGB (red, green, blue) value for the provided input.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_hex(hex_code)

        hex_code = hex_code.lstrip('#')
        return (
            int(hex_code[0:2], 16),
            int(hex_code[2:4], 16),
            int(hex_code[4:6], 16)
        )

    @classmethod
    def rgb_to_hex(cls, r: int, g: int, b: int) -> str:
        """
        Converts the provided RGB (red, green, blue) color values to HEX code format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :return: The equivalent HEX code value for the provided RGB color input.
        :rtype: str
        """
        Validate.validate_rgb(r, g, b)

        return f'#{r:02x}{g:02x}{b:02x}'.upper()

    @classmethod
    def cmyk_to_rgb(cls, c: float, m: float, y: float, k: float) -> tuple[int, int, int]:
        """
        Converts the given CMYK (cyan, magenta, yellow, key) color values to RGB (red, green, blue) format.
        :param c: The cyan value of the color to be converted.
        :type c: float
        :param m: The magenta value of the color to be converted.
        :type m: float
        :param y: The yellow value of the color to be converted.
        :type y: float
        :param k: The key value of the color to be converted.
        :type k: float
        :return: The equivalent RGB color value for the provided CMYK color input.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_cmyk(c, m, y, k)

        return (
            int(255 * (1 - c) * (1 - k)),
            int(255 * (1 - m) * (1 - k)),
            int(255 * (1 - y) * (1 - k))
        )

    @classmethod
    def rgb_to_cmyk(cls, r: int, g: int, b: int) -> tuple[float, float, float, float]:
        """
        Converts the given RGB (red, green, blue) color values to CMYK (cyan, magenta, yellow, key) format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :return: The equivalent CMYK color value for the provided RGB color input.
        :rtype: tuple(float, float, float, float)
        """
        Validate.validate_rgb(r, g, b)

        if (r, g, b) == (0, 0, 0):
            return 0.0, 0.0, 0.0, 1.0

        c = 1 - r / 255
        m = 1 - g / 255
        y = 1 - b / 255
        k = min(c, m, y)
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)

        return c, m, y, k

    @classmethod
    def hex_to_ansi(cls, hex_code: str, layer: Layer, true_color: Optional[bool] = True) -> str:
        """
        Converts a given HEX code color value to ANSI code format.
        Note: If standard color is chosen instead of true color, the closest color value will be returned.
        :param hex_code: The HEX code color value to be converted.
        :type hex_code: str
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent ANSI code color value for the provided HEX code color input value.
        :rtype: str
        """
        Validate.validate_hex(hex_code)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            r, g, b = cls.hex_to_rgb(hex_code)
            return f'\033[{layer.value};2;{r};{g};{b}m'
        else:
            closest_color_code = cls._closest_standard_color(hex_code.lstrip('#'))
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_hex(cls, ansi: str) -> str:
        """
        Converts the provided ANSI code color value to the HEX code color format.
        Note: Conversion from ANSI to HEX for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent HEX code color value for the provided ANSI code color input value.
        :rtype: str
        """
        Validate.validate_ansi(ansi)

        if ansi.startswith('\033[38;2;') or ansi.startswith('\033[48;2;'):
            code = ansi[7:].rstrip('m')
            r, g, b = map(int, code.split(';'))
            return cls.rgb_to_hex(r, g, b)
        else:
            raise Warning('Converting ANSI to HEX for standard colors is not currently supported.')

    @classmethod
    def rgb_to_ansi(cls, r: int, g: int, b: int, layer: Layer, true_color: Optional[bool] = True) -> str:
        """
        Converts the given RGB (red, green, blue) color values to the corresponding HEX code color format.
        :param r: The red value of the color to be converted.
        :type r: int
        :param g: The green value of the color to be converted.
        :type g: int
        :param b: The blue value of the color to be converted.
        :type b: int
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent HEX code color value for the provided RGB color input value.
        :rtype: str
        """
        Validate.validate_rgb(r, g, b)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return f'\033[{layer.value};2;{r};{g};{b}m'
        else:
            hex_code = cls.rgb_to_hex(r, g, b).lstrip('#')
            closest_color_code = cls._closest_standard_color(hex_code)
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_rgb(cls, ansi: str) -> tuple[int, int, int]:
        """
        Converts the provided ANSI code color value to the RGB (red, green, blue) color format.
        Note: Conversion from ANSI to RGB for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent RGB code color value for the provided ANSI code color input value.
        :rtype: tuple(int, int, int)
        """
        Validate.validate_ansi(ansi)

        if ansi.startswith('\033[38;2;') or ansi.startswith('\033[48;2;'):
            code = ansi[7:].rstrip('m')
            r, g, b = map(int, code.split(';'))
            return r, g, b
        else:
            raise Warning('Converting ANSI to RGB for standard colors is not currently supported.')

    @classmethod
    def cmyk_to_ansi(
            cls, c: float, m: float, y: float, k: float, layer: Layer, true_color: Optional[bool] = True
    ) -> str:
        """
        Converts the given CMYK (cyan, magenta, yellow, key) color values to the corresponding ANSI code color format.
        :param c: The cyan value of the color to be converted.
        :type c: float
        :param m: The magenta value of the color to be converted.
        :type m: float
        :param y: The yellow value of the color to be converted.
        :type y: float
        :param k: The key value of the color to be converted.
        :type k: float
        :param layer: The layer to which the color should be applied, either Foreground or Background.
        :type layer: Layer
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The equivalent ANSI code color value for the provided CMYK color input value.
        :rtype: str
        """
        Validate.validate_cmyk(c, m, y, k)
        cls._validate_layer(layer)
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            r, g, b = cls.cmyk_to_rgb(c, m, y, k)
            return cls.rgb_to_ansi(r, g, b, layer, true_color)
        else:
            r, g, b = cls.cmyk_to_rgb(c, m, y, k)
            hex_code = cls.rgb_to_hex(r, g, b).lstrip('#')
            closest_color_code = cls._closest_standard_color(hex_code)
            return f'\033[{closest_color_code + layer.value}m'

    @classmethod
    def ansi_to_cmyk(cls, ansi: str) -> tuple[float, float, float, float]:
        """
        Converts the provided ANSI code color value to the CMYK (cyan, magenta, yellow, key) color format.
        Note: Conversion from ANSI to CMYK for standard colors is not currently supported.
        :param ansi: The ANSI code color to be converted.
        :type ansi: str
        :return: The equivalent CMYK code color value for the provided ANSI code color input value.
        :rtype: tuple(float, float, float, float)
        """
        try:
            r, g, b = cls.ansi_to_rgb(ansi)
            return cls.rgb_to_cmyk(r, g, b)
        except Warning:
            raise Warning('Converting ANSI to CMYK for standard colors is not currently supported.')


class TextBackgroundColor:
    """
    This class defines text background colors for styling console text within the terminal.
    It includes both standard and true colors. The true colors are sourced from Wikipedia;
    please refer to the licensing information for more details. Additionally, the class offers
    methods to handle custom colors.
    """

    # Standard terminal colors supported by various operating systems
    _standard_colors = {
        'BLACK': "\033[40m",
        'RED': "\033[41m",
        'GREEN': "\033[42m",
        'YELLOW': "\033[43m",
        'BLUE': "\033[44m",
        'MAGENTA': "\033[45m",
        'CYAN': "\033[46m",
        'WHITE': "\033[47m"
    }

    # True colors, also known as 24-bit color, allow for a much broader range of colors than the
    # traditional 8-bit color systems. They enable millions of distinct colors to be displayed,
    # providing more accurate and vibrant representations of images and graphics. However, support
    # for true colors may vary depending on the capabilities of the terminal and the underlying operating system.
    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Background),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Background),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Background),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Background),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Background)
    }

    # Constants defining standard color values
    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    # Constants defining true color values
    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
        """
        Enables the addition of a custom background color to the dictionary, supporting both standard
        and true color formats. However, it's essential to note that true colors can only be added if
        the terminal supports them.
        :param name: The name for the custom background color.
        :type name: str
        :param ansi_code: The ANSI code color value for the custom background.
        :type ansi_code: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')
        Validate.validate_ansi(ansi_code)

        if true_color and not _is_true_color_supported():
            raise Warning('True colors are not supported by this terminal.')

        code = ansi_code[2:].rstrip('m')
        if true_color:
            pattern = (
                rf'^{Layer.Background.value};2;'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5])$'
            )
            if not re.match(pattern, code):
                raise ValueError('Unsupported ANSI code format.')

            cls._true_colors[name.upper()] = ansi_code
        else:
            if not code.isdigit():
                raise ValueError('Unsupported ANSI code format.')

            cls._standard_colors[name.upper()] = ansi_code

    @classmethod
    def get_colors(cls, true_color: Optional[bool] = True) -> dict:
        """
        Generates a dictionary containing a list of all colors based on the provided input.
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The dictionary containing the list of colors based on the provided input.
        :rtype: dict
        """
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
        """
        Obtains the color code corresponding to the provided input.
        :param name: The name of the color to retrieve.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            result = cls._true_colors.get(name.upper())
        else:
            result = cls._standard_colors.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid {"true" if true_color else "standard"} '
                f'color value for TextBackgroundColor'
            )

        return result

    @classmethod
    def is_standard_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a standard color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a standard color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a true color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a true color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        """
        Checks whether the provided color name corresponds to either a standard or true color.
        :param name: The name of the color to be validated.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :return: True if the provided color is either a standard or true color, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        """
        Deletes the custom background color specified by name from the dictionary.
        :param name: The name of the color to be removed.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextColor:
    """
    This class defines text foreground colors for styling console text within the terminal.
    It includes both standard and true colors. The true colors are sourced from Wikipedia;
    please refer to the licensing information for more details. Additionally, the class offers
    methods to handle custom colors.
    """

    # Standard terminal colors supported by various operating systems
    _standard_colors = {
        'BLACK': "\033[30m",
        'RED': "\033[31m",
        'GREEN': "\033[32m",
        'YELLOW': "\033[33m",
        'BLUE': "\033[34m",
        'MAGENTA': "\033[35m",
        'CYAN': "\033[36m",
        'WHITE': "\033[37m"
    }

    # True colors, also known as 24-bit color, allow for a much broader range of colors than the
    # traditional 8-bit color systems. They enable millions of distinct colors to be displayed,
    # providing more accurate and vibrant representations of images and graphics. However, support
    # for true colors may vary depending on the capabilities of the terminal and the underlying operating system.
    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Foreground),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Foreground),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Foreground),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Foreground),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Foreground)
    }

    # Constants defining standard color values
    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    # Constants defining true color values
    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
        """
        Enables the addition of a custom foreground color to the dictionary, supporting both standard
        and true color formats. However, it's essential to note that true colors can only be added if
        the terminal supports them.
        :param name: The name for the custom foreground color.
        :type name: str
        :param ansi_code: The ANSI code color value for the custom foreground.
        :type ansi_code: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')
        Validate.validate_ansi(ansi_code)

        if true_color and not _is_true_color_supported():
            raise Warning('True colors are not supported by this terminal.')

        code = ansi_code[2:].rstrip('m')
        if true_color:
            pattern = (
                rf'^{Layer.Foreground.value};2;'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5]);'
                r'(?:0|1?\d{1,2}|2[0-4]\d|25[0-5])$'
            )
            if not re.match(pattern, code):
                raise ValueError('Unsupported ANSI code format.')

            cls._true_colors[name.upper()] = ansi_code
        else:
            if not code.isdigit():
                raise ValueError('Unsupported ANSI code format.')

            cls._standard_colors[name.upper()] = ansi_code

    @classmethod
    def get_colors(cls, true_color: Optional[bool] = True) -> dict:
        """
        Generates a dictionary containing a list of all colors based on the provided input.
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The dictionary containing the list of colors based on the provided input.
        :rtype: dict
        """
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
        """
        Obtains the color code corresponding to the provided input.
        :param name: The name of the color to retrieve.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            result = cls._true_colors.get(name.upper())
        else:
            result = cls._standard_colors.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid {"true" if true_color else "standard"} '
                f'color value for TextColor'
            )

        return result

    @classmethod
    def is_standard_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a standard color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a standard color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        """
        Checks whether the provided color name corresponds to a true color.
        :param name: The name of the color to be validated.
        :type name: str
        :return: True if the provided color is a true color, False otherwise.
        :rtype: bool
        """
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        """
        Checks whether the provided color name corresponds to either a standard or true color.
        :param name: The name of the color to be validated.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :return: True if the provided color is either a standard or true color, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        """
        Deletes the custom background color specified by name from the dictionary.
        :param name: The name of the color to be removed.
        :type name: str
        :param true_color: Indicates whether true color format is chosen (True) or
        standard color format is chosen (False).
        :type true_color: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextEffect:
    """
    This class defines text effects for styling console text within the terminal. Additionally, the class offers
    methods to handle custom effects.
    """

    # Standard terminal effects supported by various operating systems
    _effects = {
        'BOLD': "\033[1m",
        'ITALIC': "\033[3m",
        'MONOSPACE': "\033[7m",
        'STRIKETHROUGH': "\033[9m",
        'UNDERLINE': "\033[4m"
    }

    # Constants defining effect values
    BOLD: str = _effects['BOLD']
    ITALIC: str = _effects['ITALIC']
    MONOSPACE: str = _effects['MONOSPACE']
    STRIKETHROUGH: str = _effects['STRIKETHROUGH']
    UNDERLINE: str = _effects['UNDERLINE']

    @classmethod
    def add_effect(cls, name: str, ansi_code: str) -> None:
        """
        Enables the addition of a custom effect to the dictionary.
        :param name: The name for the custom effect.
        :type name: str
        :param ansi_code: The ANSI code value for the custom effect.
        :type ansi_code: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_ansi(ansi_code)

        code = ansi_code[2:].rstrip('m')
        if not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')

        cls._effects[name.upper()] = ansi_code

    @classmethod
    def get_effects(cls) -> dict:
        """
        Generates a dictionary containing a list of all effects.
        :return: The dictionary containing the list of effects.
        :rtype: dict
        """
        return dict(sorted(cls._effects.items()))

    @classmethod
    def get_effect(cls, name: str) -> str:
        """
        Obtains the effect code corresponding to the provided input.
        :param name: The name of the effect to retrieve.
        :type name: str
        :return: The color code value of the provided color name.
        :rtype: str
        """
        Validate.validate_type(name, str, 'name should be a string.')
        result = cls._effects.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid effect value for TextEffect'
            )

        return result

    @classmethod
    def is_valid_effect(cls, name: str) -> bool:
        """
        Checks whether the provided effect name exists within the dictionary.
        :param name: The name of the effect to be validated.
        :type name: str
        :return: True if the provided effect exists, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return cls.get_effect(name) is not None
        except ValueError:
            return False

    @classmethod
    def remove_effect(cls, name: str) -> None:
        """
        Deletes the custom effect specified by name from the dictionary.
        :param name: The name of the effect to be removed.
        :type name: str
        """
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in cls._effects:
            del cls._effects[name.upper()]


class TextCase:
    """
    This class defines text cases for styling console text within the terminal.
    """

    # Standard terminal cases supported by various operating systems
    _cases = {
        'NONE': 0,
        'NO_CAPS': 10,
        'ALL_CAPS': 20,
        'SMALL_CAPS': 30,
        'TITLE_CASE': 40,
        'SENTENCE_CASE': 50,
        'PASCAL_CASE': 60,
        'CAMEL_CASE': 70,
        'SNAKE_CASE': 80,
        'KEBAB_CASE': 90
    }

    # Constants defining case values
    ALL_CAPS: int = _cases['ALL_CAPS']
    CAMEL_CASE: int = _cases['CAMEL_CASE']
    KEBAB_CASE: int = _cases['KEBAB_CASE']
    NONE: int = _cases['NONE']
    NO_CAPS: int = _cases['NO_CAPS']
    PASCAL_CASE: int = _cases['PASCAL_CASE']
    SENTENCE_CASE: int = _cases['SENTENCE_CASE']
    SMALL_CAPS: int = _cases['SMALL_CAPS']
    SNAKE_CASE: int = _cases['SNAKE_CASE']
    TITLE_CASE: int = _cases['TITLE_CASE']

    @classmethod
    def _all_caps(cls, message: str) -> str:
        """
        Converts the provided message to upper case.
        :param message: The message to be converted to uppercase.
        :type message: str
        :return: The converted message in upper case.
        :rtype: str
        """
        return message.upper()

    @classmethod
    def _camel_case(cls, message: str) -> str:
        """
        Converts the provided message to camel case.
        :param message: The message to be converted to camel case.
        :type message: str
        :return: The converted message in camel case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9_]+', ' ', message)
        return ''.join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(cleaned_message.split())
        )

    @classmethod
    def _kebab_case(cls, message: str) -> str:
        """
        Converts the provided message to kebab case.
        :param message: The message to be converted to kebab case.
        :type message: str
        :return: The converted message in kebab case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '-'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _no_caps(cls, message: str) -> str:
        """
        Converts the provided message to lower case.
        :param message: The message to be converted to lower case.
        :type message: str
        :return: The converted message in lower case.
        :rtype: str
        """
        return message.lower()

    @classmethod
    def _pascal_case(cls, message: str) -> str:
        """
        Converts the provided message to pascal case.
        :param message: The message to be converted to pascal case.
        :type message: str
        :return: The converted message in pascal case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return ''.join(word.capitalize() for word in cleaned_message.split())

    @classmethod
    def _sentence_case(cls, message: str) -> str:
        """
        Converts the provided message to sentence case.
        :param message: The message to be converted to sentence case.
        :type message: str
        :return: The converted message in sentence case.
        :rtype: str
        """
        return message.capitalize()

    @classmethod
    def _small_caps(cls, message: str) -> str:
        """
        Converts the provided message to small caps.
        :param message: The message to be converted to small caps.
        :type message: str
        :return: The converted message in small caps.
        :rtype: str
        """
        return ''.join(chr(ord(c.upper()) + 0xFEE0) if 'a' <= c <= 'z' else c for c in message)

    @classmethod
    def _snake_case(cls, message: str) -> str:
        """
        Converts the provided message to snake case.
        :param message: The message to be converted to snake case.
        :type message: str
        :return: The converted message in snake case.
        :rtype: str
        """
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '_'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _title_case(cls, message: str) -> str:
        """
        Converts the provided message to title case.
        :param message: The message to be converted to title case.
        :type message: str
        :return: The converted message in title case.
        :rtype: str
        """
        return message.title()

    @classmethod
    def convert_text(cls, message: str, text_case: int) -> str:
        """
        Converts the provided message to the specified text case.
        :param message: The message to be converted.
        :type message: str
        :param text_case: The text case to which the message should be converted.
        :type text_case: str
        :return: The converted message.
        :rtype: str
        """
        Validate.validate_type(message, str, 'message should be a string.')
        Validate.validate_type(text_case, int, 'text_case should be an integer.')

        match text_case:
            case cls.ALL_CAPS:
                return cls._all_caps(message)
            case cls.CAMEL_CASE:
                return cls._camel_case(message)
            case cls.KEBAB_CASE:
                return cls._kebab_case(message)
            case cls.NONE:
                return message
            case cls.NO_CAPS:
                return cls._no_caps(message)
            case cls.PASCAL_CASE:
                return cls._pascal_case(message)
            case cls.SENTENCE_CASE:
                return cls._sentence_case(message)
            case cls.SMALL_CAPS:
                return cls._small_caps(message)
            case cls.SNAKE_CASE:
                return cls._snake_case(message)
            case cls.TITLE_CASE:
                return cls._title_case(message)
            case _:
                return message

    @classmethod
    def get_cases(cls) -> dict:
        """
        Generates a dictionary containing a list of all supported text cases.
        :return: The dictionary containing the list of supported text cases.
        :rtype: dict
        """
        return dict(sorted(cls._cases.items()))


class ColorMapper:
    """
    Offers functionality to create and manage mappings for text styles, including text color,
    background color, effects, and case transformations, based on keywords such as strings or
    regex patterns. These mappings are utilized with "echo" to style text within terminals.
    """

    def __init__(self) -> None:
        """
        Initializes the ColorMapper class.
        """
        self._mappings = {}

    def add_mapping(
            self,
            name: str,
            keywords: str | list[str],
            text_color: Optional[str] = None,
            text_background_color: Optional[str] = None,
            text_effect: Optional[str] = None,
            text_case: Optional[int] = TextCase.NONE,
            color_match: Optional[bool] = False,
            ignore_case: Optional[bool] = False
    ) -> None:
        """
        Allows the addition of a mapping to the dictionary for styling text based on specified keywords.
        :param name: The name for the mapping.
        :type name: str
        :param keywords: The list of keywords to match within the text and style if matching.
        This can include either a string or list of strings. Additionally, supports regex patterns.
        :type keywords: str | list[str]
        :param text_color: The ANSI color code to apply for text foreground color.
        :type text_color: str
        :param text_background_color: The ANSI color code to apply for text background color.
        :type text_background_color: str
        :param text_effect: The ANSI effect code to apply for text.
        :type text_effect: str
        :param text_case: The text case to apply to text.
        :type text_case: int
        :param color_match: Flag to colorize only the matching content of keyword.
        If True, colorize just the matching content, else the entire text will be colorized.
        :type color_match: bool
        :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
        (case-insensitive) and matches the content, else case-sensitive match is performed.
        :type ignore_case: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(keywords, Union[str, list], 'keywords should either be a string or list of strings.')
        if isinstance(keywords, list):
            all(
                Validate.validate_type(keyword, str, 'keywords should either be a string or list of strings.')
                for keyword in keywords
            )
        Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
        Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
        Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
        Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')
        Validate.validate_type(color_match, Union[bool, None], 'color_match should be a boolean.')
        Validate.validate_type(ignore_case, Union[bool, None], 'ignore_case should be a boolean.')

        name = name.upper()
        if name in self._mappings:
            self._mappings[name]['keywords'] = [keywords] if isinstance(keywords, str) else keywords
            self._mappings[name]['color_mapping'] = {
                'text_color': text_color,
                'text_background_color': text_background_color,
                'text_effect': text_effect,
                'text_case': text_case
            }
            self._mappings[name]['flags'] = {
                'ignore_case': ignore_case,
                'color_match': color_match
            }
        else:
            self._mappings[name] = {
                'keywords': [keywords] if isinstance(keywords, str) else keywords,
                'color_mapping': {
                    'text_color': text_color,
                    'text_background_color': text_background_color,
                    'text_effect': text_effect,
                    'text_case': text_case
                },
                'flags': {
                    'ignore_case': ignore_case,
                    'color_match': color_match
                }
            }

    def get_mapping(self, name: str) -> dict:
        """
        Retrieves the mapping associated with the provided input name.
        :param name: The name of the mapping to be retrieved.
        :type name: str
        :return: The mapping in dictionary format corresponding to the provided input name.
        :rtype: dict
        """
        Validate.validate_type(name, str, 'name should be a string.')

        result = self._mappings.get(name.upper())
        if result is None:
            raise ValueError(f'"{name}" mapping not found.')

        return result

    def get_mappings(self) -> dict:
        """
        Generates a dictionary containing a list of all mappings.
        :return: The dictionary containing the list of mappings.
        :rtype: dict
        """
        return dict(sorted(self._mappings.items()))

    def is_valid_mapping(self, name: str) -> bool:
        """
        Checks whether the provided mapping name exists within the dictionary.
        :param name: The name of the mapping to be validated.
        :type name: str
        :return: True if the provided mapping exists, False otherwise.
        :rtype: bool
        """
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return self.get_mapping(name) is not None
        except ValueError:
            return False

    def remove_mapping(self, name: str) -> None:
        """
        Deletes the mapping specified by name from the dictionary.
        :param name: The name of the mapping to be removed.
        :type name: str
        """
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in self._mappings:
            del self._mappings[name.upper()]


def _get_colorize_sequence(
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None
) -> str:
    """
    Produces a colorization sequence based on the provided inputs.
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :return: The generated colorized sequence.
    :rtype: str
    """
    colorize_sequence = (
        f'{text_color if text_color is not None else ""}'
        f'{text_background_color if text_background_color is not None else ""}'
        f'{text_effect if text_effect is not None else ""}'
    )
    return colorize_sequence


def _get_colorized_message(
        message: str,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE
) -> str:
    """
    Generates a colorized message based on the provided inputs.
    :param message: The message to be colorized.
    :type message: str
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect:str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :return: The generated colorized message.
    :rtype: str
    """
    if text_color is None and text_background_color is None and text_effect is None:
        return f'{TextCase.convert_text(message, text_case)}'

    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
    return (
        f'{colorize_sequence}'
        f'{TextCase.convert_text(message, text_case)}'
        f'{RESET if colorize_sequence is not None else ""}'
    )


def _get_colorized_message_by_regex_pattern(
        message: str,
        regex_pattern: Optional[str] = None,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE,
        color_match: Optional[bool] = False,
        ignore_case: Optional[bool] = False
) -> str:
    """
    Generates a colorized message based on the provided regex pattern and inputs.
    :param message: The message to be colorized.
    :type message: str
    :param regex_pattern: The regex pattern used to verify and colorize the matching text.
    :type regex_pattern: str
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :param color_match: Flag to colorize only the matching content of keyword. If True,
    colorize just the matching content, else the entire text will be colorized.
    :type color_match: bool
    :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
    (case-insensitive) and matches the content, else case-sensitive match is performed.
    :type ignore_case: bool
    :return: The generated colorized message.
    :rtype: str
    """
    colorized_message = message
    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)

    if ignore_case:
        if color_match:
            colorized_message = re.sub(
                regex_pattern,
                lambda match: (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(match.group(), text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                ),
                colorized_message,
                flags=re.IGNORECASE
            )
        else:
            if re.search(regex_pattern, colorized_message, re.IGNORECASE):
                colorized_message = (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(colorized_message, text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                )
    else:
        if color_match:
            colorized_message = re.sub(
                regex_pattern,
                lambda match: (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(match.group(), text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                ),
                colorized_message
            )
        else:
            if re.search(regex_pattern, colorized_message):
                colorized_message = (
                    f'{colorize_sequence}'
                    f'{TextCase.convert_text(colorized_message, text_case)}'
                    f'{RESET if colorize_sequence is not None else ""}'
                )

    return colorized_message


def _get_colorized_message_by_mappings(
        message: str,
        mappings: Optional[ColorMapper] = None
) -> str:
    """
    Generates a colorized message based on the provided mappings.
    :param message: The message to be colorized.
    :type message: str
    :param mappings: The mappings utilized for verifying and colorizing the matched text.
    :type mappings: ColorMapper
    :return: The generated colorized message.
    :rtype: str
    """
    colorized_message = message
    for key, value in mappings.get_mappings().items():
        keywords = value.get('keywords', [])
        color_mappings = value.get('color_mapping', {})
        flags = value.get('flags', {})

        for keyword_pattern in keywords:
            if flags.get('ignore_case', False):
                if re.search(keyword_pattern, colorized_message, re.IGNORECASE):
                    text_color = color_mappings.get('text_color', '')
                    text_background_color = color_mappings.get('text_background_color', '')
                    text_effect = color_mappings.get('text_effect', '')
                    text_case = color_mappings.get('text_case', '')
                    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
                    if flags.get('color_match', False):
                        colorized_message = re.sub(
                            keyword_pattern,
                            lambda match: (
                                f'{colorize_sequence}'
                                f'{TextCase.convert_text(match.group(), text_case)}'
                                f'{RESET}'
                            ),
                            colorized_message,
                            flags=re.IGNORECASE
                        )
                    else:
                        colorized_message = (
                            f'{colorize_sequence}'
                            f'{TextCase.convert_text(colorized_message, text_case)}'
                            f'{RESET}'
                        )

                    break
            else:
                if re.search(keyword_pattern, colorized_message):
                    text_color = color_mappings.get('text_color', '')
                    text_background_color = color_mappings.get('text_background_color', '')
                    text_effect = color_mappings.get('text_effect', '')
                    text_case = color_mappings.get('text_case', '')
                    colorize_sequence = _get_colorize_sequence(text_color, text_background_color, text_effect)
                    if flags.get('color_match', False):
                        colorized_message = re.sub(
                            keyword_pattern,
                            lambda match: (
                                f'{colorize_sequence}'
                                f'{TextCase.convert_text(match.group(), text_case)}'
                                f'{RESET}'
                            ),
                            colorized_message
                        )
                    else:
                        colorized_message = (
                            f'{colorize_sequence}'
                            f'{TextCase.convert_text(colorized_message, text_case)}'
                            f'{RESET}'
                        )

                    break

    return colorized_message


def echo(
        message: str,
        regex_pattern: Optional[str] = None,
        mappings: Optional[ColorMapper] = None,
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None,
        text_case: Optional[int] = TextCase.NONE,
        color_match: Optional[bool] = False,
        ignore_case: Optional[bool] = False
) -> None:
    """
    Prints text colorized within the terminal based on the provided inputs. Supports the following scenarios:
    1) Colorizing a message by specifying text foreground color, text background color, text effect, and text case.
    2) Colorizing a message by matching it with a regex pattern and specifying text foreground color, text
    background color, text effect, text case, ignore case, and color match.
    3) Colorizing a message by matching it with mappings (utilizing a ColorMapper) and specifying text foreground
    color, text background color, text effect, text case, ignore case, and color match.
    :param message: The message to be colorized.
    :type message: str
    :param regex_pattern: The regex pattern used to verify and colorize the matching text.
    :type regex_pattern: str
    :param mappings: The mappings utilized for verifying and colorizing the matched text.
    :type mappings: ColorMapper
    :param text_color: The ANSI color code for the text foreground color.
    :type text_color: str
    :param text_background_color: The ANSI color code for the text background color.
    :type text_background_color: str
    :param text_effect: The ANSI effect code for the effect.
    :type text_effect: str
    :param text_case: The case to be applied for the text.
    :type text_case: str
    :param color_match: Flag to colorize only the matching content of keyword. If True,
    colorize just the matching content, else the entire text will be colorized.
    :type color_match: bool
    :param ignore_case: Flag to ignore case while performing match. If True, ignores the case
    (case-insensitive) and matches the content, else case-sensitive match is performed.
    :type ignore_case: bool
    """
    if mappings is not None:
        Validate.validate_type(mappings, ColorMapper, 'mappings should be of ColorMapper type.')
    elif regex_pattern is not None:
        Validate.validate_type(regex_pattern, str, 'regex_pattern should be a string.')
        Validate.validate_type(color_match, bool, 'color_match should be a boolean.')
        Validate.validate_type(ignore_case, bool, 'ignore_case should be a boolean.')

    if mappings is None:
        Validate.validate_type(text_color, Union[str, None], 'text_color should be a string.')
        Validate.validate_type(text_background_color, Union[str, None], 'text_background_color should be a string.')
        Validate.validate_type(text_effect, Union[str, None], 'text_effect should be a string.')
        Validate.validate_type(text_case, Union[int, None], 'text_case should be an integer.')

    colorized_message = message

    if _is_colorization_supported():
        if mappings is not None:
            colorized_message = _get_colorized_message_by_mappings(colorized_message, mappings)
        elif regex_pattern is not None:
            colorized_message = _get_colorized_message_by_regex_pattern(
                colorized_message, regex_pattern,
                text_color, text_background_color, text_effect, text_case,
                color_match, ignore_case
            )
        else:
            colorized_message = _get_colorized_message(
                colorized_message, text_color, text_background_color, text_effect, text_case
            )

    print(colorized_message)
