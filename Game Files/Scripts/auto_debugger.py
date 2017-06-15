"""
THIS MODULE IS DESIGNED TO REPLACE THE DEFAULT main.s_input() FUNCTION WITH AN AUTOMATIC INPUTTER,
ALLOWING THE GAME TO BASICALLY CHECK ITSELF FOR BUGS.
"""
import copy
import random

do_debug = False  # Set to True if you want the game to run the auto_debugger


def debug_input(x):
    print(x, end='')
    char = random.choice('0123456789ynxpsewrt')
    print(char)

    return char


def debugger():
    if do_debug:
        return debug_input

    else:
        return copy.copy(main.s_input)
