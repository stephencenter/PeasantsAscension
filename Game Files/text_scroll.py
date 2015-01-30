#   This file is part of PythoniusRPG.
#
#	 PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.

import time
import sys


class TSModeError(Exception):
    """
    Stands for "Text Scroll Mode Error"

    Raised if an invalid value for "mode" is chosen in "text_scroll()"

    """
    def __init__(self, expression):
        self.expression = expression


def text_scroll(string, mode="print", spacing=0.045):
    """
    This function causes individual characters of a string to
    only be printed one at a time with "spacing" seconds in between.
    If "mode == "print", then it prints all characters. If
    mode == "input", then it will print all but the last
    character, which will then be run through the input
    function instead.

    "mode" has two valid values: "print" and "input". Any other mode
    will raise a ModeError.

    For "spacing", any positive number (including zero) is valid. Anything
    else will cause the "time.time()" function to raise a ValueError or
    a TypeError depending on what value is used.

    Examples:

    spam = text_scroll('Please type anything you want and then press enter: ', mode="input")
    text_scroll('You entered "{0}". That\'s sort of interesting, I suppose...'.format(spam))

    """

    if mode == "print":
        string = ''.join([string, "\n"])  # Make sure to print a newline afterwards all other
                                          # characters have been printed.
        for char in string:
            print(char, end='')  # end='' prevents print() from printing a newline
                                 # after each character

            sys.stdout.flush()  # Prevent "print" from waiting until the loop is
                                # completed to print() "char"

            time.sleep(spacing)

    elif mode == "input":
        # Input mode prints all but the last character. The last character
        # is instead passed as the argument for the "input()" function,
        # the result of which is returned.

        if not string.endswith(' '):
            # If there isn't a space, then user input will be
            # meshed together with the printed characters.

            string = ''.join([string, ' '])

        for char in string[:-1]:  # Select all but the last character
            print(char, end='')
            sys.stdout.flush()
            time.sleep(spacing)

        return input(string[-1])

    else:
        raise TSModeError('Invalid value for mode: "{0}"'.format(mode))