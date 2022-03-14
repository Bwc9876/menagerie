"""
    A set of functions that are helpful when outputting data
"""
from __future__ import annotations

import sys
from enum import IntEnum
from dataclasses import dataclass


__all__ = (
    'ConsoleColorMode',
    'COLOR_MODE',
    'ConsoleTextStyle',
    'FourBitConsoleColors',
    'color_text',
    'reset_format',
    'progressbar'
)


class ConsoleColorMode(IntEnum):
    FOUR_BIT = 0
    EIGHT_BIT = 1
    RGB = 2


COLOR_MODE = ConsoleColorMode.FOUR_BIT


class FourBitConsoleColors(IntEnum):
    """
        Use this static class to select colors in :class:ConsoleTextStyle
    """

    BLACK = 0
    RED = 1
    GREEN = 2
    YELLOW = 3
    BLUE = 4
    PURPLE = 5
    CYAN = 6
    WHITE = 7


@dataclass
class ConsoleTextStyle:
    """
        A set of options for outputting colored and bolded text to the console

        :ivar color: The color of the text (see :class:ConsoleColors)
        :type color: int
        :ivar bold: Whether the text will be bolded in the console
        :type bold: bool
        :ivar high_intesity: Switch to the high intensity variant of the color selected
        :type high_itensity: bool
    """

    fg_color: int | tuple[int] = None
    bg_color: int | tuple[int] = None
    bold: bool = False
    underline: bool = False
    overline: bool = False
    blink: bool = False
    high_intensity: bool = False

    def get_flags(self):
        return self.bold, self.underline, self.overline, self.blink


flag_codes = (
    (1, None),
    (4, 24),
    (53, 55),
    (5, 25),
)


# \033[color;bg;flagsmMESSAGE\033[0m


def handle_flags(style):
    flags = style.get_flags()
    flag_string = ""
    for flag, possible in enumerate(flag_codes):
        if flags[flag] is True and possible[0] is not None:
            flag_string += f"{possible[0]};"
        elif flags[flag] is False and possible[1] is not None:
            flag_string += f"{possible[1]};"
    return flag_string[:-1]


def handle_color(color_type, style: ConsoleTextStyle, mode):
    color = style.fg_color if color_type == 0 else style.bg_color
    if color is None:
        return ""
    else:
        if mode == ConsoleColorMode.RGB:
            return str(38 if color_type == 0 else 48) + f";2;{color[0]};{color[1]};{color[2]};"
        elif mode == ConsoleColorMode.FOUR_BIT:
            return str((10 if color_type == 1 else 0) + (60 if style.high_intensity else 0) + int(color) + 30) + ";"
        elif mode == ConsoleColorMode.EIGHT_BIT:
            return str(38 if color_type == 0 else 48) + ';5;' + str(color) + ";"


def color_text(in_str: str, style: ConsoleTextStyle, reset: bool = True, override_color_mode: ConsoleColorMode = None):
    """
        Colors the given string according to the provided :py:class:`ConsoleTextStyle`

        :param reset: Whether to reset the formatting after the string
        :type reset: bool
        :param override_color_mode: Overrides the COLOR_MODE global option
        :type override_color_mode: ConsoleColorMode
        :param in_str: The string to color
        :type in_str: str
        :param style: The style to apply
        :type style: ConsoleTextStyle
    """

    if style is None:
        return in_str
    else:
        if override_color_mode is None:
            color_mode = COLOR_MODE
        else:
            color_mode = override_color_mode
        start_sequence = "\033["
        fg_color_sequence = handle_color(0, style, color_mode)
        bg_color_sequence = handle_color(1, style, color_mode)
        flag_sequence = handle_flags(style)
        end_sequence = '\033[0m' if reset else ""
        return start_sequence + fg_color_sequence + bg_color_sequence + flag_sequence + 'm' + in_str + end_sequence


def reset_format():
    print('\033[0m', end='\r')


def progressbar(it, prefix="", size=60):
    """
        Wraps a given iterator or generator (use a cast to list) to print a progress bar to the console

        :param it: The iterator to apply the bar to
        :type it: iterable
        :param prefix: Characters to show before the bar
        :type prefix: str
        :param size: The size of the bar
        :type size: int
    """

    count = len(it)

    def show(j):
        x = int(size * j / count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#" * x, "." * (size - x), j, count))
        sys.stdout.flush()

    show(0)
    for i, item in enumerate(it):
        yield item
        show(i + 1)
    sys.stdout.write("\n")
    sys.stdout.flush()