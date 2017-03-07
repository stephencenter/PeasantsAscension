#   This file is part of PythoniusRPG.
#
#    PythoniusRPG is free software: you can redistribute it and/or modify
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
import msvcrt

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input


def text_scroll(string, spacing=0.025):
    """
    This function causes individual characters of a string to
    only be printed one at a time with "spacing" seconds in between.
    If using text_scroll(), then it prints all characters. If
    using input_ts(), then it will print all but the last
    character, which will then be run through the input
    function instead.

    For "spacing", any positive number (including zero) is valid. Anything
    else will cause the "time.sleep()" function to raise a ValueError or
    a TypeError depending on what value is used.

    Examples:

    spam = input_ts('Please type anything you want and then press enter: ')
    text_scroll('You entered "{0}". That\'s sort of interesting, I suppose...'.format(spam))

    """

    if string == '-'*save_load.divider_size:
        print(string)
        return

    string = ''.join([string, "\n"])  # Make sure to print a newline afterwards all other characters have been printed.
    for char in string:
        print(char, end='')  # end='' prevents print() from printing a newline after each character

        sys.stdout.flush()  # Prevent "print" from waiting until the loop is completed to print() "char"

        if char != ' ':
            time.sleep(spacing)

        while msvcrt.kbhit():
            msvcrt.getwch()


def input_ts(string, spacing=0.025):
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

            if char != ' ':
                time.sleep(spacing)

            while msvcrt.kbhit():
                msvcrt.getwch()

        return input(string[-1])
