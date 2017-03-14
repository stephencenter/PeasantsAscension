#!/usr/bin/env python
# Peasants' Ascension v1.0.0 Beta
# --------------------------------------------------------------------------- #
#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------- #
# Music by Ben Landis: http://www.benlandis.com/
# And Eric Skiff: http://ericskiff.com/music/
# --------------------------------------------------------------------------- #
# Contact me via Twitter (@TheFrozenMawile) or email (ninjafurret@gmail.com)
# for questions/feedback. My website is http://rbwnjafurret.com/
# --------------------------------------------------------------------------- #
# Notes for people reading this code:
#  1. print('-'*save_load.divider_size) <-- This line appears constantly in my code. It's purpose
#     is to enhance readability and organization for people playing the game.
#
#  2. I am completely open to any and all criticism! I'm still pretty new to
#     programming, so I need all the advice I can get. Bug reports are great
#     too! Contact information is near the top of this module.
#
#  3. If you encounter an error message at any point when playing this, please
#     email the error code to me. If you could provide a description of what
#     you did to cause the bug, that'd be great. Contact information is near
#     the top of the module.
# --------------------------------------------------------------------------- #

import ctypes
import logging
import msvcrt
import sys
import time
import traceback

import pygame

sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Content")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Scripts")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Classes")

import tiles
import title_screen
import save_load

# Log everything and send it to stderr.
logging.basicConfig(filename='../error_log.out', level=logging.DEBUG, format="\n%(message)s")

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# A dictionary containing generic information about the player's party
party_info = {'reg': 'Central Forest', 'reg_music': 'Content/Music/Through the Forest.ogg',
              'prev_town': tiles.in_for_c, 'p_town_xyz': ['', '', ''], 'is_aethus': False, 'gp': 20,
              'visited_towns': [], 'current_tile': tiles.in_for_c, 'x': 0, 'y': 0, 'z': 0,
              'steps_without_battle': 0}


class YouDontSurfException(Exception):
    # Joke exception, used just for testing the error logger
    @staticmethod
    def bullshit_shirt():
        # Used `raise YouDontSurfException(YouDontSurfException.bullshit_shirt())`
        # This is so I don't have to type out the whole meme when I want to use this
        return "that's a stupid fucking shirt you don't surf you've never surfed lying little shit with your bullshit \
shirt fuck you"


def set_prompt_properties():
    # Find the size of the screen
    screen = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    class Coord(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class ConsoleFontInfo(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("nFont", ctypes.c_ulong), ("dwFontSize", Coord),
                    ("FontFamily", ctypes.c_uint), ("FontWeight", ctypes.c_uint), ("FaceName", ctypes.c_wchar*32)]

    # Set font information
    font = ConsoleFontInfo()
    font.cbSize = ctypes.sizeof(ConsoleFontInfo)
    font.nFont = 12
    font.FontFamily = 54
    font.FontWeight = 400

    # Adjust for screen sizes
    font.dwFontSize.X = 8 if screen[0] < 1024 else 10 if screen[0] < 1280 else 12 if screen[0] < 1920 else 15
    font.dwFontSize.Y = 14 if screen[0] < 1024 else 18 if screen[0] < 1280 else 22 if screen[0] < 1920 else 28

    # Lucidia Console is a popular monospaced font, meaning that every single character is the exact same width
    font.FaceName = "Lucida Console"
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

    # Set the console title
    ctypes.windll.kernel32.SetConsoleTitleA(f"Peasants' Ascension {title_screen.game_version}".encode())


def smart_sleep(duration):
    # "Pauses" the game for a specific duration, and then does some magic to make everything work correctly

    # return # Uncomment this when doing automated bug-testing

    time.sleep(duration)

    # I have no idea how this works but I found it on Stack Overflow and it makes the text sync properly
    while msvcrt.kbhit():
        msvcrt.getwch()


def main():
    # main() handles all the setup for the game, and includes the main game loop.
    # Everything happens in this function in one way or another.

    set_prompt_properties()  # Set the CMD size and whatnot...
    save_load.change_settings()  # ...set the volume and save file settings...
    title_screen.show_title()  # ...display the titlescreen...
    save_load.load_game()  # ...check for save files...
    tiles.movement_system()  # ...and then start the game.


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    try:
        # Run the game.
        main()

    except Exception as e:
        # If an exception is raised and not caught, log the error message.
        logging.exception(f'Got exception of main handler on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')

        # raise # Uncomment this if you're using the auto-input debugger

        print(traceback.format_exc())
        print("""\
Peasants' Ascension encountered an error and crashed! Send the error message
shown above to TheFrozenMawile (ninjafurret@gmail.com) to make sure the bug
gets fixed. The error message, along with any errors messages encountered,
can also be found in the error_log.out file.""")
        input("\nPress enter/return")

        pygame.quit()
        sys.exit()
