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
#  1. print('-'*25) <-- This line appears constantly in my code. It's purpose
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

import sys
import os
import random
import math
import time
import json
import copy
import configparser
import ctypes
import re
import logging
import msvcrt
import traceback
import stat
import pygame

sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Content")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Scripts")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Classes")

# noinspection PyPep8
import tiles
import inv_system
import battle
import magic
import bosses
import items
import sounds
import towns
import units
import ascii_art

# Log everything and send it to stderr.
logging.basicConfig(filename='../error_log.out', level=logging.DEBUG)
logging.debug("Game run")

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# Save File information
save_dir = 'Content/Save Files'
adventure_name = ''

# General Save Files
sav_acquired_gems = 'Content/Save Files/{CHARACTER_NAME}/acquired_gems.json'    # Acquired Gems
sav_def_bosses = 'Content/Save Files/{CHARACTER_NAME}/def_bosses.json'          # Defeated Bosses
sav_equip_items = 'Content/Save Files/{CHARACTER_NAME}/equip_items.json'        # Equipped Items
sav_inventory = 'Content/Save Files/{CHARACTER_NAME}/inventory.json'            # Inventory
sav_misc_boss_info = 'Content/Save Files/{CHARACTER_NAME}/misc_boss_info.json'  # Misc Boss Info
sav_party_info = 'Content/Save Files/{CHARACTER_NAME}/party_info.json'          # Party Info
sav_quests_dia = 'Content/Save Files/{CHARACTER_NAME}/quests_dia.json'          # Quests & Dialogue
sav_spellbook = 'Content/Save Files/{CHARACTER_NAME}/spellbook.json'            # Spellbook

# PCU Save Files
sav_play = 'Content/Save Files/{CHARACTER_NAME}/play_stats.json'        # Player Stats
sav_solou = 'Content/Save Files/{CHARACTER_NAME}/solou_stats.json'      # Solou's Stats
sav_xoann = 'Content/Save Files/{CHARACTER_NAME}/xoann_stats.json'      # Xoann's Stats
sav_chyme = 'Content/Save Files/{CHARACTER_NAME}/chyme_stats.json'      # Chyme's Stats
sav_ran_af = 'Content/Save Files/{CHARACTER_NAME}/ran_af_stats.json'    # Ran'af's Stats
sav_parsto = 'Content/Save Files/{CHARACTER_NAME}/parsto_stats.json'    # Parsto's Stats
sav_adorine = 'Content/Save Files/{CHARACTER_NAME}/adorine_stats.json'  # Adorine's Stats

# The volume of the game, on a scale from 0 (muted) to 1.0 (loudest). Can be changed in the settings.cfg file.
music_vol = 1.0
sound_vol = 1.0

# If enabled, text will appear on screen character-by-character instead of all at once.
do_text_scroll = False

# A dictionary containing generic information about the player's party
party_info = {'reg': 'Central Forest', 'reg_music': 'Content/Music/Through the Forest.ogg',
              'prev_town': tiles.in_for_c, 'p_town_xyz': ['', '', ''], 'is_aethus': False, 'gp': 20,
              'visited_towns': [], 'current_tile': tiles.in_for_c, 'x': 0, 'y': 0, 'z': 0}

# The version number the game is currently updated to
game_version = 'v1.0.0 Beta'

# This text is displayed when you start the game
title_logo = f"""
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
------------------------------------------------------------------------------"""


def set_adventure_name():
    # This function asks the player for an "adventure name". This is the
    # name of the directory in which his/her save files will be stored.
    global adventure_name

    while True:
        # Certain OSes don't allow certain characters, so this removes those characters
        # and replaces them with whitespace. The player is then asked if this is okay.
        choice = input("Finally, what do you want to name this adventure? | Input name: ")

        # Files/Folders cannot be have only whitespace as their filename.
        if not ''.join(choice.split()):
            continue

        temp_name = re.sub('[^\w\-_! ]', '', choice)

        for x, y in enumerate(temp_name):
            try:
                if not(y == ' ' and temp_name[x + 1] == ' '):
                    adventure_name = ''.join([adventure_name, y])

            except IndexError:
                pass

        if adventure_name[0] == ' ':
            adventure_name = adventure_name[1:]

        if not ''.join(adventure_name.split()) and ''.join(choice.split()):
            print("\nPlease choose a different name, that one definitely won't do!")
            continue

        # Make sure that the folder doesn't already exist, because
        # certain OSes don't allow duplicate folder names.
        elif os.path.isdir('/'.join([save_dir, adventure_name])) and adventure_name:
            print("\nI've already read about adventures with that name; be original!\n")
            adventure_name = ''

            continue

        # Check if the modified adventure name is identical to the original one the player proposed
        elif adventure_name != choice:
            while True:
                y_n = input(f'\nI had to change some of that. Does "{adventure_name}" sound okay? | Yes or No: ')
                y_n = y_n.lower()

                if y_n.startswith("y"):
                    format_save_names()

                    if units.player.name.lower() == "give me the gold":
                        print("Gold cheat enabled, you now have 99999 gold!")
                        party_info['gp'] = 99999

                    return

                elif y_n.startswith("n"):
                    adventure_name = ''
                    print()

                    break

        elif len(choice) > 35 and len(adventure_name) > 35:
            print("\That adventure name is far too long, it would never catch on!")
            continue

        else:
            while True:
                y_n = input(f'You wish for your adventure to be known as "{choice}"? | Yes or No: ')

                if y_n.startswith("y"):
                    format_save_names()

                    if units.player.name.lower() == "give me the gold":
                        print("Gold cheat enabled, you now have 99999 gold!")
                        party_info['gp'] = 99999

                    return

                elif y_n.startswith("n"):
                    adventure_name = ''
                    print()

                    break


def format_save_names():
    # Replace "{CHARACTER_NAME}" in the save-file paths to the player's adventure name.
    # e.g. "Save Files/{CHARACTER_NAME}/sav_acquired_gems" --> "Save Files/ADV/sav_acquired_gems

    for x in sorted(['sav_acquired_gems', 'sav_def_bosses', 'sav_equip_items', 'sav_inventory', 'sav_misc_boss_info',
                     'sav_party_info', 'sav_spellbook', 'sav_quests_dia', 'sav_play', 'sav_solou', 'sav_xoann',
                     'sav_chyme', 'sav_adorine', 'sav_ran_af', 'sav_parsto'], key=str.lower):

        globals()[x] = globals()[x].format(CHARACTER_NAME=adventure_name)


def change_settings():
    config = configparser.ConfigParser()

    if os.path.isfile("../settings.cfg"):
        config.read("../settings.cfg")

        for x in config['volume_levels']:
            globals()[x] = float(config['volume_levels'][x])/100

        for x in config['do_text_scroll']:
            if config['do_text_scroll'][x] in ['False', 'True']:
                globals()[x] = eval(config['do_text_scroll'][x])
            else:
                globals()[x] = True

        sounds.change_volume()


def check_save():  # Check for save files and load the game if they're found
    global party_info
    global adventure_name

    print('-'*25)

    # Check each part of the save file
    print('Searching for valid save files...')
    if not os.path.isdir(save_dir):
        smart_sleep(0.1)

        print('No save files found. Starting new game...')
        smart_sleep(0.1)

        print('-'*25)
        units.create_player()
        return

    dirs = [d for d in os.listdir(save_dir) if os.path.isdir(os.path.join(save_dir, d))]

    save_files = {}
    menu_info = {}

    save_file_list = [
        sav_acquired_gems, sav_def_bosses, sav_equip_items, sav_inventory, sav_misc_boss_info, sav_party_info,
        sav_quests_dia, sav_spellbook, sav_play, sav_solou, sav_xoann, sav_ran_af, sav_adorine, sav_parsto, sav_chyme
    ]

    for directory in dirs:

        # If all save-file components exist...
        if all(map(os.path.isfile, [x.format(CHARACTER_NAME=directory) for x in save_file_list])):

            # ...then set the dictionary key equal to the newly-formatted save file names
            save_files[directory] = [x.format(CHARACTER_NAME=directory) for x in save_file_list]

            try:
                with open('/'.join([save_dir, directory, "menu_info.txt"]),
                          encoding='utf-8') as f:
                    menu_info[directory] = f.read()

            except FileNotFoundError:
                menu_info[directory] = "Unable to load preview info"

    smart_sleep(0.1)

    if not save_files:
        # If there are no found save files, then have the player make a new character
        print('No save files found. Starting new game...')

        smart_sleep(0.1)

        print('-'*25)
        units.create_player()

        return

    print('-'*25)
    print(f'Found {len(save_files)} valid save file(s): ')

    # padding is a number that the game uses to determine how much whitespace is needed
    # to make certain visual elements line up on the screen.
    padding = len(max([index for index in save_files], key=len))

    spam = True
    while spam:
        # Print information about each save file and allow the player to choose which
        # file to open
        print('     ', '\n      '.join([f"[{num + 1}] {fol}{' '*(padding - len(fol))} | {menu_info[fol]}"
                                       for num, fol in enumerate([key for key in sorted(save_files)])]))

        while True:
            chosen = input('Input [#] (or type "create new"): ')
            try:
                # Account for the fact that list indices start at 0
                chosen = int(chosen) - 1
                if chosen < 0:
                    continue

            except ValueError:
                chosen = chosen.lower()

                # Let the player create a new save file
                if chosen.startswith("c"):
                    print('-'*25)
                    units.create_player()
                    return

                else:
                    continue

            try:
                # Sort the save file names in alphanumerical order
                adventure_name = sorted(save_files)[chosen]
            except IndexError:
                continue

            format_save_names()

            print('-'*25)
            print(f'Loading Save File: "{sorted(save_files)[chosen]}"...')
            smart_sleep(0.1)

            # Attempt to open the save files and translate
            # them into objects/dictionaries
            try:
                with open(sav_def_bosses, encoding='utf-8') as f:
                    bosses.defeated_bosses = list(json.load(f))

                with open(sav_party_info, encoding='utf-8') as f:
                    party_info = json.load(f)

                for key in party_info:
                    if key in ['current_tile', 'prev_town'] and party_info[key]:
                        for tile in tiles.all_tiles:
                            if party_info[key] == tile.tile_id:
                                party_info[key] = tile

                # Call functions to serialize more advanced things
                items.deserialize_gems(sav_acquired_gems)
                inv_system.deserialize_equip(sav_equip_items)
                inv_system.deserialize_inv(sav_inventory)
                bosses.deserialize_bosses(sav_misc_boss_info)
                npcs.deserialize_dialogue(sav_quests_dia)
                magic.deserialize_sb(sav_spellbook)
                units.deserialize_player(sav_play, sav_solou, sav_xoann, sav_adorine, sav_chyme, sav_ran_af, sav_parsto)

                print('Load successful.')

                if not towns.search_towns(enter=False):
                    print('-'*25)

                return

            except (OSError, ValueError):
                logging.exception('Error loading game:')
                print('There was an error loading your game.')
                input("\nPress enter/return ")
                print('-'*25)
                break


def save_game():
    while True:
        y_n = input('Do you wish to save your progress? | Yes or No: ')

        y_n = y_n.lower()

        if y_n.startswith('y'):
            print('Saving...')
            smart_sleep(0.1)

            # Check if the save directory already exists, and create it if it doesn't
            try:
                os.makedirs('/'.join([save_dir, adventure_name]))
            except FileExistsError:
                pass

            format_save_names()

            try:
                with open(sav_def_bosses, mode='w', encoding='utf-8') as f:
                    json.dump(bosses.defeated_bosses, f, indent=4, separators=(', ', ': '))

                json_party_info = {}
                for key in party_info:
                    if key in ['current_tile', 'prev_town']:
                        if isinstance(party_info[key], tiles.Tile):
                            json_party_info[key] = party_info[key].tile_id

                        else:
                            json_party_info[key] = party_info[key]

                    else:
                        json_party_info[key] = party_info[key]

                with open(sav_party_info, mode='w', encoding='utf-8') as f:
                    json.dump(json_party_info, f, indent=4, separators=(', ', ': '))

                items.serialize_gems(sav_acquired_gems)
                inv_system.serialize_equip(sav_equip_items)
                inv_system.serialize_inv(sav_inventory)
                bosses.serialize_bosses(sav_misc_boss_info)
                npcs.serialize_dialogue(sav_quests_dia)
                magic.serialize_sb(sav_spellbook)
                units.serialize_player(sav_play, sav_solou, sav_xoann, sav_adorine, sav_chyme, sav_ran_af, sav_parsto)

                with open('/'.join([save_dir, adventure_name, 'menu_info.txt']), mode='w', encoding='utf-8') as f:
                    f.write("NAME: {0} | LEVEL: {1} | CLASS: {2}".format(units.player.name,
                                                                         units.player.lvl,
                                                                         units.player.class_.title()))

                print('Save successful.')

                return

            except (OSError, ValueError):
                logging.exception('Error saving game:')
                print('There was an error saving your game.')
                input("\nPress enter/return ")

        elif y_n.startswith('n'):
            return


def title_screen():
    pygame.mixer.music.load('Content/Music/Prologue.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_vol)

    print(title_logo)

    while True:
        # Give the user a choice of keys to press to do specific actions
        choice = input('[P]lay Game | [C]redits | [S]tory | [L]ore | [E]xit  |  Input Letter: ')

        choice = choice.lower()

        if choice.startswith('p'):
            return

        elif choice.startswith('c'):
            print('-'*25)

            try:
                pygame.mixer.music.load('Content/Music/Credits Music for an 8-bit RPG.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display the credits one line at a time with specific lengths
                # of time in between each line. Syncs up with the music!
                with open('Content/Credits.txt') as f:
                    for number, f.readline in enumerate(f):
                        print(''.join(f.readline.rstrip("\n").split(";")))
                        smart_sleep([0.75, 1.25, 0.75, 1.25, 1, 1, 0.5, 0.5, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5,
                                    0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5][number])

                    smart_sleep(3)

                    pygame.mixer.music.load('Content/Music/Prologue.ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(music_vol)

            except FileNotFoundError:
                # Display this is the Credits.txt file couldn't be found
                print('The "Credits.txt" file could not be found.')

            except OSError:
                # If there is a problem opening the Credits.txt file, but it does exist,
                # display this message and log the error
                logging.exception('Error loading Credits.txt:')
                print('There was a problem opening "Credits.txt".')

            print(title_logo)

        elif choice.startswith('s'):
            # Display the storyline of the game
            print('-'*25)
            input('Press enter/return after each line to advance the text ')
            print('-'*25)

            try:
                pygame.mixer.music.load('Content/Music/CopperNickel.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display each line one at a time, and require the pressing of enter
                # on lines that aren't solely whitespace
                with open('Content/peasant_plot.txt', encoding='utf-8') as f:
                    for f.readline in f:
                        if ''.join(char for char in f.readline.split(" ") if char.isalnum()):
                            input(''.join(f.readline.rstrip("\n").split(";")))
                        else:
                            print(''.join(f.readline.rstrip("\n").split(";")))

                pygame.mixer.music.load('Content/Music/Prologue.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

            except FileNotFoundError:
                # Display this is the peasant_plot.txt file couldn't be found
                print('The "peasant_plot.txt" file could not be found.')

            except OSError:
                # If there is a problem opening the peasant_plot.txt file, but it does exist,
                # display this message and log the error
                logging.exception('Error loading peasant_plot.txt:')
                print('There was an problem opening "peasant_plot.txt".')

            print('-'*25)

        elif choice.startswith('l'):
            # Display side-story lore and the history of Pythonia
            print('-'*25)
            input('Press enter/return after each line to advance the text ')
            print('-'*25)

            try:
                pygame.mixer.music.load('Content/Music/CopperNickel.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display each line one at a time, and require the pressing of enter
                # on lines that aren't solely whitespace
                with open('Content/peasant_lore.txt', encoding='utf-8') as f:
                    for f.readline in f:
                        if ''.join(char for char in f.readline.split(" ") if char.isalnum()):
                            input(''.join(f.readline.rstrip("\n").split(";")))
                        else:
                            print(''.join(f.readline.rstrip("\n").split(";")))

                pygame.mixer.music.load('Content/Music/Prologue.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

            except FileNotFoundError:
                print('The "peasant_lore.txt" file could not be found.')

            except OSError:
                logging.exception('Error loading peasant_lore.txt:')
                print('There was an problem opening "peasant_lore.txt".')

            print('-'*25)

        elif choice.startswith('e'):
            # Exit the game
            pygame.quit()
            sys.exit()


def set_prompt_properties():
    # Configure the properties of the command prompt so that everything fits/looks right

    # Find the size of the screen
    screen = ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1)

    class Coord(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class ConsoleFontInfo(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong), ("nFont", ctypes.c_ulong), ("dwFontSize", Coord),
                    ("FontFamily", ctypes.c_uint), ("FontWeight", ctypes.c_uint), ("FaceName", ctypes.c_wchar*32)]

    font = ConsoleFontInfo()
    font.cbSize = ctypes.sizeof(ConsoleFontInfo)
    font.nFont = 12

    # Adjust for screen sizes
    font.dwFontSize.X = 8 if screen[0] < 1024 else 10 if screen[0] < 1280 else 12 if screen[0] < 1920 else 15
    font.dwFontSize.Y = 14 if screen[0] < 1024 else 18 if screen[0] < 1280 else 22 if screen[0] < 1920 else 28

    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Lucida Console"

    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, ctypes.c_long(False), ctypes.pointer(font))

    # Calculate the proper width for the buffer size and then set the height to be 150
    # A height of 150 should allow the player to scroll back up to read previous events if needs be.
    os.system("@echo off")
    os.system("conSize.bat {0} {1} {2} {3}".format(math.ceil(screen[0]/font.dwFontSize.X),
                                                   math.ceil(screen[1]/font.dwFontSize.Y),
                                                   math.ceil(screen[0]/font.dwFontSize.X), 150))

    # Set the console title
    ctypes.windll.kernel32.SetConsoleTitleA(f"Peasants' Ascension {game_version}".encode())


def copy_error(text):
    # This is a modified verstion of Albert Sweigart's "Pyperclip" module.
    # It is licensed under the BSD (link: http://opensource.org/licenses/BSD-2-Clause)
    # I removed a large portion of it due to it being unnessesary, and changed the variable names
    # to match my naming conventions.

    d = ctypes.windll
    d.user32.OpenClipboard(None)
    d.user32.EmptyClipboard()
    hcd = d.kernel32.GlobalAlloc(0x2000, len(text.encode('utf-16-le')) + 2)
    pch_data = d.kernel32.GlobalLock(hcd)
    ctypes.cdll.msvcrt.wcscpy(ctypes.c_wchar_p(pch_data), text)
    d.kernel32.GlobalUnlock(hcd)
    d.user32.SetClipboardData(13, hcd)
    d.user32.CloseClipboard()


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
    change_settings()  # ...set the volume and save file settings...
    title_screen()  # ...display the titlescreen...
    check_save()  # ...check for save files...
    tiles.movement_system()  # ...and then start the game.


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    import npcs

    # Yes, this is a try...except statement that includes functions that spans thousands of lines,
    # but it's necessary for error logging.
    try:
        # Run the game.
        main()

    except Exception as e:
        # If an exception is raised and not caught, log the error message.
        # raise # Uncomment this if you're using the auto-input debugger
        logging.exception('Got exception of main handler:')
        pygame.mixer.music.stop()
        print(traceback.format_exc())

        print('''Peasants' Ascension encountered an error and crashed! The error message above should
be sent as soon as possible to TheFrozenMawile (ninjafurret@gmail.com) to make sure the bug gets fixed.
The error message can be immediately copied to your clipboard if you wish.''')
        print('-'*25)

        # The player is given the option to copy it instead of just being forced, because
        # I personally hate programs that overwrite your clipboard without permission.
        while True:
            c = input('Type in "copy" to copy to your clipboard, or simply press enter to exit: ')
            if c.lower() == "copy":
                copy_error(traceback.format_exc())
                print('-'*25)
                print('The error message has been copied to your clipboard.')
                input('Press enter/return to exit ')

                raise

            elif c.lower() == '':
                raise
