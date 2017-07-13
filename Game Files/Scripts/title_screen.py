# This file is part of Peasants' Ascension.
#
# Peasants' Ascension is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Peasants' Ascension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
import time
import os

import pygame
import save_load

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# The version number the game is currently updated to
game_version = 'v1.0.0 Beta'


def show_title():
    title_logo = f"""\
  ____                            _       _
 |  _ \ ___  __ _ ___  __ _ _ __ | |_ ___( )
 | |_) / _ \/ _` / __|/ _` | '_ \| __/ __|/
 |  __/  __/ (_| \__ \ (_| | | | | |_\__ \\
 |_|   \___|\__,_|___/\__,_|_| |_|\__|___/
         _                           _
        / \   ___  ___ ___ _ __  ___(_) ___  _ __
       / _ \ / __|/ __/ _ \ '_ \/ __| |/ _ \| '_ \\
      / ___ \\\__ \ (_|  __/ | | \__ \ | (_) | | | |
     /_/   \_\___/\___\___|_| |_|___/_|\___/|_| |_|
Peasants' Ascension {game_version} -- Programmed by TheFrozenMawile using Python
Licensed under the GNU GPLv3: [https://www.gnu.org/copyleft/gpl.html]
Check here often for updates: [http://www.reddit.com/r/PeasantsAscension/]
{'-'*save_load.divider_size}"""

    pygame.mixer.music.load('Content/Music/Prologue.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(save_load.music_vol)

    print(title_logo)

    while True:
        # Give the user a choice of keys to press to do specific actions
        choice = main.s_input('[P]lay Game | [S]ettings | [C]redits | [L]ore | [E]xit | Input Letter: ').lower()

        if choice.startswith('p'):
            return

        if choice.startswith("s"):
            os.system("notepad.exe ../settings.cfg")

        if choice.startswith('c'):
            show_credits()
            print(title_logo)

        if choice.startswith('l'):
            while True:
                c_2 = main.s_input('View [H]istory or [S]tory? | Input letter (or type "back"): ').lower()

                if c_2.startswith("h"):
                    show_history()

                elif c_2.startswith("s"):
                    show_story()

                elif c_2 in ['e', 'x', 'exit', 'b', 'back']:
                    break

            print(title_logo)

        if choice.startswith('e'):
            # Exit the game
            pygame.quit()
            sys.exit()


def show_credits():
    print('-'*save_load.divider_size)

    try:
        pygame.mixer.music.load('Content/Music/Credits Music for an 8-bit RPG.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

        # Display the credits one line at a time with specific lengths
        # of time in between each line. Syncs up with the music!
        with open('Content/Credits.txt') as f:
            for number, line in enumerate(f):
                print(''.join(line.split("\n")))
                main.smart_sleep([0.75, 1.25, 0.75, 1.25, 1, 1, 0.5, 0.5, 1, 1,
                                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                  1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                  1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5,
                                  0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                  0.5, 0.5, 0.5, 0.5][number])

            main.smart_sleep(3)

            pygame.mixer.music.load('Content/Music/Prologue.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

    except FileNotFoundError:
        # Display this is the Credits.txt file couldn't be found
        logging.exception(f'Error finding credits.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('The "credits.txt" file could not be found.')
        main.s_input("\nPress enter/return ")

    except OSError:
        # If there is a problem opening the Credits.txt file, but it does exist,
        # display this message and log the error
        logging.exception(f'Error loading credits.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was a problem opening "credits.txt".')
        main.s_input("\nPress enter/return ")


def show_story():
    # Display the storyline of the game
    print('-'*save_load.divider_size)
    main.s_input('Press enter/return after each line to advance the text ')
    print('-'*save_load.divider_size)

    try:
        pygame.mixer.music.load('Content/Music/CopperNickel.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

        # Display each line one at a time, and require the pressing of enter
        # on lines that aren't solely whitespace
        with open('Content/peasant_plot.txt', encoding='utf-8') as f:
            for line in f:
                if ''.join(char for char in line.split(" ") if char.isalnum()):
                    main.s_input(''.join(line.split("\n")))

                else:
                    print(''.join(line.split("\n")))

        pygame.mixer.music.load('Content/Music/Prologue.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

    except FileNotFoundError:
        # Display this is the peasant_plot.txt file couldn't be found
        logging.exception(f'Error finding peasant_plot.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('The "peasant_plot.txt" file could not be found.')
        main.s_input("\nPress enter/return ")

    except OSError:
        # If there is a problem opening the peasant_plot.txt file, but it does exist,
        # display this message and log the error
        logging.exception(f'Error loading peasant_plot.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an problem opening "peasant_plot.txt".')
        main.s_input("\nPress enter/return ")

    print('-'*save_load.divider_size)


def show_history():
    # Display side-story lore and the history of Pythonia
    print('-'*save_load.divider_size)
    main.s_input('Press enter/return after each line to advance the text ')
    print('-'*save_load.divider_size)

    try:
        pygame.mixer.music.load('Content/Music/CopperNickel.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

        # Display each line one at a time, and require the pressing of enter
        # on lines that aren't solely whitespace
        with open('Content/peasant_lore.txt', encoding='utf-8') as f:
            for line in f:
                if ''.join(char for char in line.split(" ") if char.isalnum()):
                    main.s_input(''.join(line.split("\n")))
                else:
                    print(''.join(line.split("\n")))

        pygame.mixer.music.load('Content/Music/Prologue.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

    except FileNotFoundError:
        logging.exception(f'Error finding peasant_lore.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('The "peasant_lore.txt" file could not be found.')

    except OSError:
        logging.exception(f'Error loading peasant_lore.txt on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an problem opening "peasant_lore.txt".')

    print('-'*save_load.divider_size)
