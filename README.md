# `pycolorecho`

Welcome to **pycolorecho** - your go-to Python package for effortlessly colorizing text within terminals, enhancing the
visual appeal and readability of your console applications.

## Features

The **pycolorecho** package offers a plethora of features to style your text:

- **Text Colorization**: Easily change the foreground color of your text to catch attention or categorize information.
- **Background Colorization**: Make your text pop by adding vibrant background colors, ensuring it stands out against
  the terminal background.
- **Text Styles**: From bold to underline, add emphasis and structure to your text with various styling options.
- **Text Cases**: Optimize readability by converting text to different cases like sentence case, title case, or all
  caps.

## Standard and True Color ANSI Formats

With **pycolorecho**, you have the flexibility to choose between standard and true color ANSI formats:

### Standard Colors

Enjoy a classic color palette including black, green, red, yellow, blue, magenta, cyan, and white. These colors are
universally supported across terminals, ensuring consistency across different operating systems.

### True Colors (24-bit)

Step into the vibrant world of true colors, boasting millions of distinct shades for unparalleled visual richness. True
colors, also known as 24-bit color, offer a more accurate representation of images and graphics. However, please note
that support for true colors may vary depending on your terminal and operating system capabilities.

## Getting Started

- Install **pycolorecho** via pip:

```bash
pip install pycolorecho
```

- Import the package in your Python script:

```python
import pycolorecho
```

## Usage

```python
from pycolorecho import echo, TextColor, TextBackgroundColor, TextEffect, ColorMapper

# Colorizing entire message
echo('This is a test message', text_color=TextColor.RED)  # Standard color
echo('This is a test message', text_color=TextColor.ACID_GREEN)  # True color

# Colorizing by regex pattern
echo('This is a test message', regex_pattern=r'test', text_color=TextColor.RED,
     text_background_color=TextBackgroundColor.ACID_GREEN)

# Colorizing by mappings
color_mappings = ColorMapper()
color_mappings.add_mapping('error', [r'error'], text_color=TextColor.RED, text_effect=TextEffect.UNDERLINE)
echo('This is a test error message', mappings=color_mappings)
```

# Documentation

## pycolorecho

#### Constants

- `RESET`: This is a constant ANSI code variable to reset the text styles.

#### Methods

- `echo(message: str, regex_pattern: Optional[str] = None, mappings: Optional[ColorMapper] = None, text_color: Optional[str] = None, text_background_color: Optional[str] = None, text_effect: Optional[str] = None, text_case: Optional[int] = TextCase.NONE, color_match: Optional[bool] = False, ignore_case: Optional[bool] = False)` -
  Printstext colorized within the terminal based on the provided inputs. Supports the following scenarios:
    1) Colorizing a message by specifying text foreground color, text background color, text effect, and text case.
    2) Colorizing a message by matching it with a regex pattern and specifying text foreground color, text background
       color, text effect, text case, ignore case, and color match.
    3) Colorizing a message by matching it with mappings (utilizing a ColorMapper) and specifying text foreground.
- `get_colorized_message(message: str, text_color: Optional[str] = None, text_background_color: Optional[str] = None, text_effect: Optional[str] = None, text_case: Optional[int] = TextCase.NONE) -> str` -
  Generates a colorized message based on the provided inputs.
- `get_colorized_message_by_regex_pattern(message: str, regex_pattern: str, text_color: Optional[str] = None, text_background_color: Optional[str] = None, text_effect: Optional[str] = None, text_case: Optional[int] = TextCase.NONE, color_match: Optional[bool] = False, ignore_case: Optional[bool] = False) -> str` -
  Generates a colorized message based on the provided regex pattern and inputs.
- `get_colorized_message_by_mappings(message: str, mappings: Optional[ColorMapper] = None) -> str` - Generates a
  colorized message based on the provided mappings.
- `is_colorization_supported() -> bool` - Checks if the current operating system supports colorization. Returns True if
  colorization is supported, False otherwise.
- `is_true_color_supported() -> bool` - Verifies whether the true color format is supported by the current operating
  system and terminal. Returns True if true color format is supported, False otherwise.

#### Usage

```python
from pycolorecho import is_colorization_supported, is_true_color_supported, get_colorized_message, get_colorized_message_by_regex_pattern, get_colorized_message_by_mappings, TextColor, TextBackgroundColor, TextEffect, ColorMapper

print(is_colorization_supported())  # Prints True if colorization is supported, False otherwise
print(is_true_color_supported())  # Prints True if true color format is supported, False otherwise

# Retrieving colorized message
print(get_colorized_message('This is a test message', text_color=TextColor.RED))

# Retrieving colorized message by regex pattern
print(get_colorized_message_by_regex_pattern('This is a test message', regex_pattern=r'test', text_color=TextColor.RED,
                                             text_background_color=TextBackgroundColor.ACID_GREEN))

# Retrieving colorized message by mappings
color_mappings = ColorMapper()
color_mappings.add_mapping('error', [r'error'], text_color=TextColor.RED, text_effect=TextEffect.UNDERLINE)
print(get_colorized_message_by_mappings('This is a test error message', mappings=color_mappings))
```

### Layer

Supplies enum-based options for different color layers within a terminal, such as Foreground and Background.

#### Options

- `Foreground` - To colorize the text foreground color.
- `Background` - To colorize the text background color.

### TextBackgroundColor

Enhance your text styling further with the TextBackgroundColor class, which offers a wide range of background color
options for console text within the terminal. This class encompasses both standard and true colors, providing
versatility and customization options to suit your preferences.

#### Constants

Maintained within this class are constants representing both standard and true color codes.

#### Methods

Explore the functionality provided by the TextBackgroundColor class:

- `add_color(name: str, ansi_code: str, true_color: Optional[bool] = True)`: Add a custom background color, supporting
  both standard and true color formats. Note that true colors can only be added if the terminal supports them.
- `get_colors(true_color: Optional[bool] = True) -> dict`: Generate a dictionary containing a list of all colors based
  on the provided input.
- `get_color(name: str, true_color: Optional[bool] = True) -> str`: Obtain the color code corresponding to the provided
  input.
- `is_standard_color(name: str) -> bool`: Check whether the provided color name corresponds to a standard color.
- `is_true_color(name: str) -> bool`: Check whether the provided color name corresponds to a true color.
- `is_valid_color(name: str, true_color: Optional[bool] = True) -> bool`: Check whether the provided color name
  corresponds to either a standard or true color.
- `remove_color(name: str, true_color: Optional[bool] = True)`: Delete the custom background color specified by name
  from the dictionary.

#### Usage

Here's how you can utilize the TextBackgroundColor class:

```python
from pycolorecho import TextBackgroundColor

# Accessing standard color
print(TextBackgroundColor.RED)

# Accessing true color
print(TextBackgroundColor.ACID_GREEN)

# Adding new custom true color
TextBackgroundColor.add_color(name='CUSTOM_1', ansi_code='\033[48;2;255;255;255m', true_color=True)

# Adding new custom standard color
TextBackgroundColor.add_color(name='CUSTOM_2', ansi_code='\033[107m', true_color=False)

# Printing all true colors
print(TextBackgroundColor.get_colors(true_color=True))

# Printing all standard colors
print(TextBackgroundColor.get_colors(true_color=False))

# Retrieving true color code
print(TextBackgroundColor.get_color(name='CUSTOM_1', true_color=True))

# Retrieving standard color code
print(TextBackgroundColor.get_color(name='CUSTOM_2', true_color=False))

# Checking standard color
print(TextBackgroundColor.is_standard_color('CUSTOM_2'))

# Checking true color
print(TextBackgroundColor.is_true_color('CUSTOM_1'))

# Checking color
print(TextBackgroundColor.is_valid_color(name='CUSTOM_1', true_color=True))

# Removing custom true color
print(TextBackgroundColor.remove_color(name='CUSTOM_1', true_color=True))

# Removing custom standard color
print(TextBackgroundColor.remove_color(name='CUSTOM_2', true_color=False))
```

### TextColor

Elevate your text styling with the TextColor class, providing an extensive range of foreground color options for console
text within the terminal. This class encompasses both standard and true colors, offering flexibility and customization
to suit your visual preferences.

#### Constants

Within this class, constants representing both standard and true color codes are maintained.

#### Methods

Explore the capabilities of the TextColor class:

- `add_color(name: str, ansi_code: str, true_color: Optional[bool] = True)`: Add a custom foreground color, supporting
  both standard and true color formats. Please note that true colors can only be added if the terminal supports them.
- `get_colors(true_color: Optional[bool] = True) -> dict`: Generate a dictionary containing a list of all colors based
  on the provided input.
- `get_color(name: str, true_color: Optional[bool] = True) -> str`: Obtain the color code corresponding to the provided
  input.
- `is_standard_color(name: str) -> bool`: Check whether the provided color name corresponds to a standard color.
- `is_true_color(name: str) -> bool`: Check whether the provided color name corresponds to a true color.
- `is_valid_color(name: str, true_color: Optional[bool] = True) -> bool`: Check whether the provided color name
  corresponds to either a standard or true color.
- `remove_color(name: str, true_color: Optional[bool] = True)`: Delete the custom foreground color specified by name
  from the dictionary.

#### Usage

Here's how you can utilize the TextColor class:

```python
from pycolorecho import TextColor

# Accessing standard color
print(TextColor.RED)

# Accessing true color
print(TextColor.ACID_GREEN)

# Adding new custom true color
TextColor.add_color(name='CUSTOM_1', ansi_code='\033[38;2;255;255;255m', true_color=True)

# Adding new custom standard color
TextColor.add_color(name='CUSTOM_2', ansi_code='\033[97m', true_color=False)

# Printing all true colors
print(TextColor.get_colors(true_color=True))

# Printing all standard colors
print(TextColor.get_colors(true_color=False))

# Retrieving true color code
print(TextColor.get_color(name='CUSTOM_1', true_color=True))

# Retrieving standard color code
print(TextColor.get_color(name='CUSTOM_2', true_color=False))

# Checking standard color
print(TextColor.is_standard_color('CUSTOM_2'))

# Checking true color
print(TextColor.is_true_color('CUSTOM_1'))

# Checking color
print(TextColor.is_valid_color(name='CUSTOM_1', true_color=True))

# Removing custom true color
print(TextColor.remove_color(name='CUSTOM_1', true_color=True))

# Removing custom standard color
print(TextColor.remove_color(name='CUSTOM_2', true_color=False))
```

### TextEffect

Enhance your text styling with the TextEffect class, providing a variety of effects for console text within the
terminal. This class allows you to add custom effects, offering further versatility in text presentation.

#### Constants

Supported effects are maintained as constants within this class.

#### Methods

Discover the functionality offered by the TextEffect class:

- `add_effect(name: str, ansi_code: str)`: Add a custom effect to the dictionary.
- `get_effects() -> dict`: Generate a dictionary containing a list of all effects.
- `get_effect(name: str) -> str`: Obtain the effect code corresponding to the provided input.
- `is_valid_effect(name: str) -> bool`: Check whether the provided effect name exists within the dictionary.
- `remove_effect(name: str)`: Delete the custom effect specified by name from the dictionary.

#### Usage

Here's how you can utilize the TextEffect class:

```python
from pycolorecho import TextEffect

# Accessing effect
print(TextEffect.BOLD)

# Adding new custom effect
TextEffect.add_effect(name='CUSTOM_1', ansi_code='\033[5m')

# Printing all effects
print(TextEffect.get_effects())

# Retrieving effect code
print(TextEffect.get_effect('CUSTOM_1'))

# Checking effect
print(TextEffect.is_valid_effect('CUSTOM_1'))

# Removing custom effect
print(TextEffect.remove_effect('CUSTOM_1'))
```

### TextCase

Refine your text styling with the TextCase class, offering options for transforming text cases within the terminal.

#### Constants

Supported text cases are maintained as constants within this class.

#### Methods

Explore the functionalities provided by the TextCase class:

- `convert_text(message: str, text_case: int) -> str`: Convert the provided message to the specified text case.
- `get_cases() -> dict`: Generate a dictionary containing a list of all supported text cases.

#### Usage

Here's how you can utilize the TextCase class:

```python
from pycolorecho import TextCase

# Accessing case
print(TextCase.ALL_CAPS)

# Printing all cases
print(TextCase.get_cases())

# Converts the message
print(TextCase.convert_text(message='This is a test message', text_case=TextCase.ALL_CAPS))
```

### ColorMapper

Empower your text styling with the ColorMapper class, offering functionality to create and manage mappings for text
styles within the terminal. These mappings enable dynamic styling based on keywords, including text color, background
color, effects, and case transformations.

#### Methods

Discover the capabilities provided by the ColorMapper class:

- `add_mapping(name: str, keywords: str | list[str], text_color: Optional[str] = None, text_background_color: Optional[str] = None, text_effect: Optional[str] = None, text_case: Optional[int] = TextCase.NONE, color_match: Optional[bool] = False, ignore_case: Optional[bool] = False)`:
  Add a mapping to the dictionary for styling text based on specified keywords.
- `get_mapping(name: str) -> dict`: Retrieve the mapping associated with the provided input name.
- `get_mappings() -> dict`: Generate a dictionary containing a list of all mappings.
- `is_valid_mapping(name: str) -> bool`: Check whether the provided mapping name exists within the dictionary.
- `remove_mapping(name: str)`: Delete the mapping specified by name from the dictionary.

#### Usage

Here's how you can utilize the ColorMapper class:

```python
from pycolorecho import ColorMapper, TextColor

# Initialize ColorMapper
color_mappings = ColorMapper()

# Adding new custom mapping
color_mappings.add_mapping(name='error', keywords=[r'error'], text_color=TextColor.RED)

# Retrieving custom mapping
print(color_mappings.get_mapping('error'))

# Retrieving all mappings
print(color_mappings.get_mappings())

# Checking mapping
print(color_mappings.is_valid_mapping('error'))

# Removing custom mapping
color_mappings.remove_mapping('error')
```

### Color

The Color class provides versatile methods for handling various color format conversions, empowering you to seamlessly
manage color representations within terminal applications.

#### Methods

Explore the functionalities offered by the Color class:

- `hex_to_rgb(hex_code: str) -> tuple[int, int, int]`: Convert the given color HEX code to RGB format.
- `rgb_to_hex(r: int, g: int, b: int) -> str`: Convert the provided RGB (red, green, blue) color values to HEX code
  format.
- `cmyk_to_rgb(c: float, m: float, y: float, k: float) -> tuple[int, int, int]`: Convert the given CMYK (cyan, magenta,
  yellow, key) color values to RGB (red, green, blue) format.
- `rgb_to_cmyk(r: int, g: int, b: int) -> tuple[float, float, float, float]`: Convert the given RGB (red, green, blue)
  color values to CMYK (cyan, magenta, yellow, key) format.
- `hex_to_ansi(hex_code: str, layer: Layer, true_color: Optional[bool] = True) -> str`: Convert a given HEX code color
  value to ANSI code format.
- `ansi_to_hex(ansi: str) -> str`: Convert the provided ANSI code color value to the HEX code color format.
- `rgb_to_ansi(r: int, g: int, b: int, layer: Layer, true_color: Optional[bool] = True) -> str`: Convert the given RGB (
  red, green, blue) color values to the corresponding ANSI code color format.
- `ansi_to_rgb(ansi: str) -> tuple[int, int, int]`: Convert the provided ANSI code color value to the RGB (red, green,
  blue) color format.
- `cmyk_to_ansi(c: float, m: float, y: float, k: float, layer: Layer, true_color: Optional[bool] = True) -> str`:
  Convert the given CMYK (cyan, magenta, yellow, key) color values to the corresponding ANSI code color format.
- `ansi_to_cmyk(ansi: str) -> tuple[float, float, float, float]`: Convert the provided ANSI code color value to the
  CMYK (cyan, magenta, yellow, key) color format.

#### Usage

Here's how you can utilize the methods provided by the Color class:

```python
from pycolorecho import Color, Layer

# Convert HEX code to RGB format
print(Color.hex_to_rgb('#FFFFFF'))

# Convert RGB color values to HEX code format
print(Color.rgb_to_hex(255, 255, 255))

# Convert CMYK color values to RGB format
print(Color.cmyk_to_rgb(0.0, 0.0, 0.0, 0.0))

# Convert RGB color values to CMYK format
print(Color.rgb_to_cmyk(255, 255, 255))

# Convert HEX code color value to ANSI code format
print(Color.hex_to_ansi('#FFFFFF', Layer.Foreground, true_color=True))

# Convert ANSI code color value to HEX code color format
print(Color.ansi_to_hex('\033[48;2;255;255;255m'))

# Convert RGB color values to corresponding ANSI code color format
print(Color.rgb_to_ansi(255, 255, 255, Layer.Background, true_color=True))

# Convert ANSI code color value to RGB color format
print(Color.ansi_to_rgb('\033[38;2;255;255;255m'))

# Convert CMYK color values to corresponding ANSI code color format
print(Color.cmyk_to_ansi(0.0, 0.0, 0.0, 0.0, Layer.Background, true_color=True))

# Convert ANSI code color value to CMYK color format
print(Color.ansi_to_cmyk('\033[107m'))
```

### HEXCodes

The HEXCodes class serves as a supporting class encapsulating constants representing HEX code formats for various
colors, sourced from Wikipedia. For licensing information regarding the colors, please refer to the appropriate sources.

# License

Please refer to the [MIT license](LICENSE) within the project for more information. Additionally, refer to
the [ADDITIONAL LICENSES](ADDITIONAL%20LICENSES.md) file for licensing information related to components used within
this package.

# Contributing

We welcome contributions from the community! Whether you have ideas for new features, bug fixes, or enhancements, feel
free to open an issue or submit a pull request on [GitHub](https://github.com/coldsofttech/pycolorecho).