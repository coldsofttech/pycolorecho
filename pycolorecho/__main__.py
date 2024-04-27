import os
import re
import sys
from enum import Enum
from typing import Optional, Union

import colorama

RESET: str = "\033[0m"


def _is_colorization_supported() -> bool:
    colorama.init()

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
            print(colorama.Fore.RED + 'Test', file=f, end='')
            print(colorama.Style.RESET_ALL, file=f, end='')

        with open(file_name, 'r') as f:
            content = f.read()
            return 'Test' in content
    finally:
        os.remove(file_name)
        colorama.deinit()


def _is_true_color_supported() -> bool:
    colorama.init()

    if os.name == 'nt':
        true_color_support = True
    else:
        true_color_support = os.getenv('COLORTERM') in ['truecolor', '24bit']

    colorama.deinit()
    return true_color_support


class Validate:
    @classmethod
    def validate_range(cls, values, expected_range, message) -> None:
        if not all(expected_range[0] <= x <= expected_range[1] for x in values):
            raise ValueError(message)

    @classmethod
    def validate_type(cls, value, expected_type, message) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(message)

    @classmethod
    def validate_hex(cls, hex_code: str) -> None:
        cls.validate_type(hex_code, str, 'hex_code should be a string.')
        if not re.match(r'#[0-9a-fA-F]{6}$', hex_code.upper()):
            raise ValueError('Invalid HEX code format. Example: #RRGGBB.')

    @classmethod
    def validate_rgb(cls, *args) -> None:
        if len(args) != 3:
            raise ValueError('Exactly 3 arguments are required.')

        cls.validate_range(
            args,
            (0, 255),
            'Invalid RGB code format. RGB values should be in the range 0-255. Example: 127, 128, 255.'
        )

    @classmethod
    def validate_cmyk(cls, *args) -> None:
        if len(args) != 4:
            raise ValueError('Exactly 4 arguments are required.')

        cls.validate_range(
            args,
            (0.0, 1.0),
            'Invalid CMYK code format. CMYK values should be in the range 0.0-1.0. Example: 0.7, 0.1, 1.0, 1.0.'
        )

    @classmethod
    def validate_ansi(cls, ansi: str) -> None:
        cls.validate_type(ansi, str, 'ansi should be a string.')

        if not re.match(r'^\033\[[0-9;]+m$', ansi) and not re.match(r'^\x1b\[[0-9;]+m$', ansi):
            raise ValueError('Invalid ANSI code format.')

        code = ansi[2:].rstrip('m')
        if not code.startswith('38;2;') and not code.startswith('48;2;') and not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')


class HEXCodes:
    ABSOLUTE_ZERO: str = "#0048BA"
    ACID_GREEN: str = "#B0BF1A"
    AERO: str = "#7CB9E8"
    AFRICAN_VIOLET: str = "#B284BE"
    AIR_SUPERIORITY_BLUE: str = "#72A0C1"


class Layer(Enum):
    Foreground: int = 38
    Background: int = 48


class Color:
    @classmethod
    def _validate_layer(cls, layer: Layer) -> None:
        Validate.validate_type(layer, Layer, 'layer should be of Layer type.')

    @classmethod
    def _hex_distance(cls, hex1: str, hex2: str) -> int:
        if len(hex1) != 6 or len(hex2) != 6:
            raise ValueError('Hex color values must be of length 6 (excluding # symbol)')

        r1, g1, b1 = tuple(int(hex1[i:i + 2], 16) for i in (0, 2, 4))
        r2, g2, b2 = tuple(int(hex2[i:i + 2], 16) for i in (0, 2, 4))
        return abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)

    @classmethod
    def _closest_standard_color(cls, hex_code: str) -> int:
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
        Validate.validate_hex(hex_code)

        hex_code = hex_code.lstrip('#')
        return (
            int(hex_code[0:2], 16),
            int(hex_code[2:4], 16),
            int(hex_code[4:6], 16)
        )

    @classmethod
    def rgb_to_hex(cls, r: int, g: int, b: int) -> str:
        Validate.validate_rgb(r, g, b)

        return f'#{r:02x}{g:02x}{b:02x}'.upper()

    @classmethod
    def cmyk_to_rgb(cls, c: float, m: float, y: float, k: float) -> tuple[int, int, int]:
        Validate.validate_cmyk(c, m, y, k)

        return (
            int(255 * (1 - c) * (1 - k)),
            int(255 * (1 - m) * (1 - k)),
            int(255 * (1 - y) * (1 - k))
        )

    @classmethod
    def rgb_to_cmyk(cls, r: int, g: int, b: int) -> tuple[float, float, float, float]:
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
        Validate.validate_ansi(ansi)

        if ansi.startswith('\033[38;2;') or ansi.startswith('\033[48;2;'):
            code = ansi[7:].rstrip('m')
            r, g, b = map(int, code.split(';'))
            return cls.rgb_to_hex(r, g, b)
        else:
            raise Warning('Converting ANSI to HEX for standard colors is not currently supported.')

    @classmethod
    def rgb_to_ansi(cls, r: int, g: int, b: int, layer: Layer, true_color: Optional[bool] = True) -> str:
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
        try:
            r, g, b = cls.ansi_to_rgb(ansi)
            return cls.rgb_to_cmyk(r, g, b)
        except Warning:
            raise Warning('Converting ANSI to CMYK for standard colors is not currently supported.')


class TextBackgroundColor:
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

    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Background),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Background),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Background),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Background),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Background)
    }

    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
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
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
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
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextColor:
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

    _true_colors = {
        'ABSOLUTE_ZERO': Color.hex_to_ansi(HEXCodes.ABSOLUTE_ZERO, Layer.Foreground),
        'ACID_GREEN': Color.hex_to_ansi(HEXCodes.ACID_GREEN, Layer.Foreground),
        'AERO': Color.hex_to_ansi(HEXCodes.AERO, Layer.Foreground),
        'AFRICAN_VIOLET': Color.hex_to_ansi(HEXCodes.AFRICAN_VIOLET, Layer.Foreground),
        'AIR_SUPERIORITY_BLUE': Color.hex_to_ansi(HEXCodes.AIR_SUPERIORITY_BLUE, Layer.Foreground)
    }

    BLACK: str = _standard_colors['BLACK']
    RED: str = _standard_colors['RED']
    GREEN: str = _standard_colors['GREEN']
    YELLOW: str = _standard_colors['YELLOW']
    BLUE: str = _standard_colors['BLUE']
    MAGENTA: str = _standard_colors['MAGENTA']
    CYAN: str = _standard_colors['CYAN']
    WHITE: str = _standard_colors['WHITE']

    ABSOLUTE_ZERO: str = _true_colors['ABSOLUTE_ZERO']
    ACID_GREEN: str = _true_colors['ACID_GREEN']
    AERO: str = _true_colors['AERO']
    AFRICAN_VIOLET: str = _true_colors['AFRICAN_VIOLET']
    AIR_SUPERIORITY_BLUE: str = _true_colors['AIR_SUPERIORITY_BLUE']

    @classmethod
    def add_color(cls, name: str, ansi_code: str, true_color: Optional[bool] = True) -> None:
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
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            return dict(sorted(cls._true_colors.items()))
        else:
            return dict(sorted(cls._standard_colors.items()))

    @classmethod
    def get_color(cls, name: str, true_color: Optional[bool] = True) -> str:
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
        return cls.is_valid_color(name, true_color=False)

    @classmethod
    def is_true_color(cls, name: str) -> bool:
        return cls.is_valid_color(name, true_color=True)

    @classmethod
    def is_valid_color(cls, name: str, true_color: Optional[bool] = True) -> bool:
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        try:
            return cls.get_color(name, true_color) is not None
        except ValueError:
            return False

    @classmethod
    def remove_color(cls, name: str, true_color: Optional[bool] = True) -> None:
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(true_color, bool, 'true_color should be a boolean.')

        if true_color:
            if name.upper() in cls._true_colors:
                del cls._true_colors[name.upper()]
        else:
            if name.upper() in cls._standard_colors:
                del cls._standard_colors[name.upper()]


class TextEffect:
    _effects = {
        'BOLD': "\033[1m",
        'ITALIC': "\033[3m",
        'MONOSPACE': "\033[7m",
        'STRIKETHROUGH': "\033[9m",
        'UNDERLINE': "\033[4m"
    }

    BOLD: str = _effects['BOLD']
    ITALIC: str = _effects['ITALIC']
    MONOSPACE: str = _effects['MONOSPACE']
    STRIKETHROUGH: str = _effects['STRIKETHROUGH']
    UNDERLINE: str = _effects['UNDERLINE']

    @classmethod
    def add_effect(cls, name: str, ansi_code: str) -> None:
        Validate.validate_type(name, str, 'name should be a string.')
        Validate.validate_type(ansi_code, str, 'ansi_code should be a string.')
        Validate.validate_ansi(ansi_code)

        code = ansi_code[2:].rstrip('m')
        if not code.isdigit():
            raise ValueError('Unsupported ANSI code format.')

        cls._effects[name.upper()] = ansi_code

    @classmethod
    def get_effects(cls) -> dict:
        return dict(sorted(cls._effects.items()))

    @classmethod
    def get_effect(cls, name: str) -> str:
        Validate.validate_type(name, str, 'name should be a string.')
        result = cls._effects.get(name.upper())

        if result is None:
            raise ValueError(
                f'{name} is not a valid effect value for TextEffect'
            )

        return result

    @classmethod
    def is_valid_effect(cls, name: str) -> bool:
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return cls.get_effect(name) is not None
        except ValueError:
            return False

    @classmethod
    def remove_effect(cls, name: str) -> None:
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in cls._effects:
            del cls._effects[name.upper()]


class TextCase:
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
        return message.upper()

    @classmethod
    def _camel_case(cls, message: str) -> str:
        cleaned_message = re.sub(r'[^a-zA-Z0-9_]+', ' ', message)
        return ''.join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(cleaned_message.split())
        )

    @classmethod
    def _kebab_case(cls, message: str) -> str:
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '-'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _no_caps(cls, message: str) -> str:
        return message.lower()

    @classmethod
    def _pascal_case(cls, message: str) -> str:
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return ''.join(word.capitalize() for word in cleaned_message.split())

    @classmethod
    def _sentence_case(cls, message: str) -> str:
        return message.capitalize()

    @classmethod
    def _small_caps(cls, message: str) -> str:
        return ''.join(chr(ord(c.upper()) + 0xFEE0) if 'a' <= c <= 'z' else c for c in message)

    @classmethod
    def _snake_case(cls, message: str) -> str:
        cleaned_message = re.sub(r'[^a-zA-Z0-9]+', ' ', message)
        return '_'.join(word.lower() for word in cleaned_message.split())

    @classmethod
    def _title_case(cls, message: str) -> str:
        return message.title()

    @classmethod
    def convert_text(cls, message: str, text_case: int) -> str:
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
        return dict(sorted(cls._cases.items()))


class ColorMapper:
    def __init__(self) -> None:
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
        Validate.validate_type(name, str, 'name should be a string.')

        result = self._mappings.get(name.upper())
        if result is None:
            raise ValueError(f'"{name}" mapping not found.')

        return result

    def get_mappings(self) -> dict:
        return dict(sorted(self._mappings.items()))

    def is_valid_mapping(self, name: str) -> bool:
        Validate.validate_type(name, str, 'name should be a string.')

        try:
            return self.get_mapping(name) is not None
        except ValueError:
            return False

    def remove_mapping(self, name: str) -> None:
        Validate.validate_type(name, str, 'name should be a string.')

        if name.upper() in self._mappings:
            del self._mappings[name.upper()]


def _get_colorize_sequence(
        text_color: Optional[str] = None,
        text_background_color: Optional[str] = None,
        text_effect: Optional[str] = None
) -> str:
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
