import configparser
import json
import logging
import os
import re
import sys
import time
import shutil

import pygame

import inv_system
import items
import magic
import npcs
import sounds
import tiles
import towns
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# General Save Files
sav_acquired_gems = '{ADVENTURE_NAME}/acquired_gems.json'    # Acquired Gems
sav_def_bosses = '{ADVENTURE_NAME}/def_bosses.json'          # Defeated Bosses
sav_equip_items = '{ADVENTURE_NAME}/equip_items.json'        # Equipped Items
sav_inventory = '{ADVENTURE_NAME}/inventory.json'            # Inventory
sav_misc_boss_info = '{ADVENTURE_NAME}/misc_boss_info.json'  # Misc Boss Info
sav_party_info = '{ADVENTURE_NAME}/party_info.json'          # Party Info
sav_quests_dia = '{ADVENTURE_NAME}/quests_dia.json'          # Quests & Dialogue
sav_spellbook = '{ADVENTURE_NAME}/spellbook.json'            # Spellbook
sav_chests = '{ADVENTURE_NAME}/chests.json'                  # Chest Info

# PCU Save Files
sav_play = '{ADVENTURE_NAME}/play_stats.json'        # Player Stats
sav_solou = '{ADVENTURE_NAME}/solou_stats.json'      # Solou's Stats
sav_xoann = '{ADVENTURE_NAME}/xoann_stats.json'      # Xoann's Stats
sav_chyme = '{ADVENTURE_NAME}/chyme_stats.json'      # Chyme's Stats
sav_ran_af = '{ADVENTURE_NAME}/ran_af_stats.json'    # Ran'af's Stats
sav_parsto = '{ADVENTURE_NAME}/parsto_stats.json'    # Parsto's Stats
sav_adorine = '{ADVENTURE_NAME}/adorine_stats.json'  # Adorine's Stats

adventure_name = ''
base_dir = "Content/Save Files"
temp_dir = "temp"

# Game Settings. Can be changed in the settings.cfg file.
music_vol = 1.0  # The volume of the game's Music, on a scale from 0 (muted) to 1.0 (loudest).
sound_vol = 1.0  # The volume of the game's SFX, on a scale from 0 (muted) to 1.0 (loudest).
divider_size = 25  # The number of dashes used for dividers between different UI elements
do_blip = True  # Determines whether or not a "blip" sound is made whenever you press enter


def set_adventure_name():
    # This function asks the player for an "adventure name". This is the
    # name of the directory in which his/her save files will be stored.
    global adventure_name

    while True:
        # Certain OSes don't allow certain characters, so this removes those characters
        # and replaces them with whitespace. The player is then asked if this is okay.
        choice = main.s_input("Finally, what do you want to name this adventure? | Input name: ")

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

        # You can't use blank adventure names. You also can't use "temp", because this is reserved for other features
        if (not ''.join(adventure_name.split()) and ''.join(choice.split())) or adventure_name == 'temp':
            print("\nPlease choose a different name, that one definitely won't do!")
            continue

        # Make sure that the folder doesn't already exist, because
        # certain OSes don't allow duplicate folder names.
        elif os.path.isdir('/'.join([base_dir, adventure_name])) and adventure_name:
            print("\nI've already read about adventures with that name; be original!\n")
            adventure_name = ''

            continue

        # Check if the modified adventure name is identical to the original one the player proposed
        elif adventure_name != choice:
            while True:
                y_n = main.s_input(f'\nI had to change some of that. Is "{adventure_name}" okay? | Y/N: ').lower()

                if y_n.startswith("y"):
                    format_save_names()

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
                y_n = main.s_input(f'You wish for your adventure to be known as "{choice}"? | Y/N: ').lower()

                if y_n.startswith("y"):
                    format_save_names()

                    return

                elif y_n.startswith("n"):
                    adventure_name = ''
                    print()

                    break


def format_save_names():
    # Replace "{ADVENTURE_NAME}" in the save-file paths to the player's adventure name.
    # e.g. "Save Files/{ADVENTURE_NAME}/sav_acquired_gems" --> "Save Files/ADV/sav_acquired_gems

    for x in sorted(['sav_acquired_gems', 'sav_def_bosses', 'sav_equip_items', 'sav_inventory', 'sav_misc_boss_info',
                     'sav_party_info', 'sav_spellbook', 'sav_quests_dia', 'sav_play', 'sav_solou', 'sav_xoann',
                     'sav_chyme', 'sav_adorine', 'sav_ran_af', 'sav_parsto', 'sav_chests'], key=str.lower):

        globals()[x] = globals()[x].format(ADVENTURE_NAME=adventure_name)


def change_settings():
    config = configparser.ConfigParser()

    if os.path.isfile("../settings.cfg"):
        config.read("../settings.cfg")
        config = config['settings']

        globals()['music_vol'] = float(config['music_vol'])/100
        globals()['sound_vol'] = float(config['sound_vol'])/100
        globals()['divider_size'] = int(config['divider_size'])
        globals()['do_blip'] = int(config['do_blip'])

        sounds.change_volume()


def save_game(verbose=True):
    # Save important game data to .json files
    # If verbose == True, then this function will print everything and use smart_sleep() functions
    # When set to False, this function can be used to auto-save the game

    save_file_list = [
        sav_acquired_gems, sav_def_bosses, sav_equip_items, sav_inventory, sav_misc_boss_info, sav_party_info,
        sav_quests_dia, sav_spellbook, sav_play, sav_solou, sav_xoann, sav_ran_af, sav_adorine, sav_parsto, sav_chyme,
        sav_chests
    ]

    while True:
        y_n = main.s_input('Do you wish to save your progress? | Y/N: ').lower() if verbose else 'y'

        if y_n.startswith('y'):
            print('Saving...') if verbose else ''
            main.smart_sleep(0.1) if verbose else ''

            # Check if the temp directory already exists, and create it if it doesn't
            try:
                os.makedirs('/'.join([base_dir, temp_dir, adventure_name]))

            except FileExistsError:
                pass

            format_save_names()
            serialize_all(verbose)

            try:
                os.makedirs('/'.join([base_dir, adventure_name]))

            except FileExistsError:
                pass

            # Move the files from their temporary destination to the real directory
            for file in save_file_list:
                shutil.move('/'.join([base_dir, temp_dir, file]), '/'.join([base_dir, file]))

            # Text used to give a preview of the save file, in case the player can't remember which one is which
            with open('/'.join([base_dir, adventure_name, 'menu_info.txt']), mode='w', encoding='utf-8') as f:
                f.write(f"NAME: {units.player.name} | LEVEL: {units.player.lvl} | CLASS: {units.player.class_.title()}")

            # Create a file with a disclaimer that warns against manually editing save files
            with open('/'.join([base_dir, "SAVE FILE README.txt"]), mode='w', encoding='utf-8') as f:
                f.write("""---IMPORTANT NOTE---
Editing these .json files is a VERY easy way to corrupt your save file. Many
parts of the save file are more essential than you'd think. For example, the
name of your class is used to check which abilities you can use, as well as
what kind of attack (melee/ranged) your character uses. The name of your party
members (aside from the one you name at the beginning) are also important,
being used to handle currently equipped items as well as temporary stats in
battle. Unless you are familiar with the inner-workings of the game and know
how to read/edit .json files, it's highly recommended that you do not edit
these files.""")

            # Delete the temp directory
            shutil.rmtree('/'.join([base_dir, temp_dir]))

            return

        elif y_n.startswith('n'):
            return


def load_game():  # Check for save files and load the game if they're found
    global adventure_name

    print('-'*divider_size)

    # Check each part of the save file
    print('Searching for valid save files...')
    main.smart_sleep(0.1)

    if not os.path.isdir(base_dir):

        print('No save files found. Starting new game...')
        main.smart_sleep(0.1)

        print('-'*divider_size)
        units.create_player()

        return

    save_files = {}
    menu_info = {}

    save_file_list = [
        sav_acquired_gems, sav_def_bosses, sav_equip_items, sav_inventory, sav_misc_boss_info, sav_party_info,
        sav_quests_dia, sav_spellbook, sav_play, sav_solou, sav_xoann, sav_ran_af, sav_adorine, sav_parsto, sav_chyme,
        sav_chests
    ]

    for folder in [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]:
        # If all save-file components exist...
        if all(map(os.path.isfile, ['/'.join([base_dir, x.format(ADVENTURE_NAME=folder)]) for x in save_file_list])):
            # ...then set the dictionary key equal to the newly-formatted save file names
            save_files[folder] = [x.format(ADVENTURE_NAME=folder) for x in save_file_list]

            try:
                with open('/'.join([base_dir, folder, "menu_info.txt"]), encoding='utf-8') as f:
                    menu_info[folder] = f.read()

            except FileNotFoundError:
                menu_info[folder] = "Unable to load preview info"

    main.smart_sleep(0.1)

    if not save_files:
        # If there are no found save files, then have the player make a new character
        print('No save files found. Starting new game...')
        print('-'*divider_size)
        main.smart_sleep(0.1)
        units.create_player()

        return

    print('-'*divider_size)
    print(f'Found {len(save_files)} valid save file(s): ')

    # padding is a number that the game uses to determine how much whitespace is needed
    # to make certain visual elements line up on the screen.
    padding = len(max([index for index in save_files], key=len))

    # Print information about each save file and allow the player to choose which
    # file to open
    for num, fol in enumerate([key for key in sorted(save_files)]):
        print(f"      [{num + 1}] {fol}{' '*(padding - len(fol))} | {menu_info[fol]}")

    while True:
        chosen = main.s_input('Input [#] (or type "create new"): ').lower()

        try:
            # Account for the fact that list indices start at 0
            adventure_name = sorted(save_files)[int(chosen) - 1]

        except (IndexError, ValueError):
            # Let the player create a new save file
            if chosen.startswith("c"):
                print('-'*divider_size)
                units.create_player()
                return

            continue

        print('-'*divider_size)
        print(f'Loading Save File: "{sorted(save_files)[int(chosen) - 1]}"...')
        main.smart_sleep(0.1)

        format_save_names()
        deserialize_all()

        return


def serialize_all(verbose=True):
    try:
        with open('/'.join([base_dir, temp_dir, sav_def_bosses]), mode='w', encoding='utf-8') as f:
            json.dump(units.defeated_bosses, f, indent=4, separators=(', ', ': '))

        json_party_info = {}

        for key in main.party_info:
            if key in ['current_tile', 'prev_town']:
                if isinstance(main.party_info[key], tiles.Tile):
                    json_party_info[key] = main.party_info[key].tile_id

                else:
                    json_party_info[key] = main.party_info[key]

            else:
                json_party_info[key] = main.party_info[key]

        with open('/'.join([base_dir, temp_dir, sav_party_info]), mode='w', encoding='utf-8') as f:
            json.dump(json_party_info, f, indent=4, separators=(', ', ': '))

        items.serialize_gems('/'.join([base_dir, temp_dir, sav_acquired_gems]))
        inv_system.serialize_equip('/'.join([base_dir, temp_dir, sav_equip_items]))
        inv_system.serialize_inv('/'.join([base_dir, temp_dir, sav_inventory]))
        npcs.serialize_dialogue('/'.join([base_dir, temp_dir, sav_quests_dia]))
        magic.serialize_sb('/'.join([base_dir, temp_dir, sav_spellbook]))
        units.serialize_bosses('/'.join([base_dir, temp_dir, sav_misc_boss_info]))
        towns.serialize_chests('/'.join([base_dir, temp_dir, sav_chests]))

        units.serialize_player('/'.join([base_dir, temp_dir, sav_play]),
                               '/'.join([base_dir, temp_dir, sav_solou]),
                               '/'.join([base_dir, temp_dir, sav_xoann]),
                               '/'.join([base_dir, temp_dir, sav_adorine]),
                               '/'.join([base_dir, temp_dir, sav_chyme]),
                               '/'.join([base_dir, temp_dir, sav_ran_af]),
                               '/'.join([base_dir, temp_dir, sav_parsto]))

        print('Save successful.') if verbose else ''

        return

    except (OSError, ValueError):
        logging.exception(f'Error saving game on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an error saving. Error message can be found in error_log.out') if verbose else ''
        main.s_input("\nPress enter/return ") if verbose else ''


def deserialize_all():
    try:
        with open('/'.join([base_dir, sav_def_bosses]), encoding='utf-8') as f:
            units.defeated_bosses = list(json.load(f))

        with open('/'.join([base_dir, sav_party_info]), encoding='utf-8') as f:
            main.party_info = json.load(f)

        main.party_info['current_tile'] = tiles.find_tile_with_id(main.party_info['current_tile'])
        main.party_info['prev_town'] = tiles.find_tile_with_id(main.party_info['prev_town'])

        # Call functions to serialize more advanced things
        items.deserialize_gems('/'.join([base_dir, sav_acquired_gems]))
        inv_system.deserialize_equip('/'.join([base_dir, sav_equip_items]))
        inv_system.deserialize_inv('/'.join([base_dir, sav_inventory]))
        units.deserialize_bosses('/'.join([base_dir, sav_misc_boss_info]))
        npcs.deserialize_dialogue('/'.join([base_dir, sav_quests_dia]))
        magic.deserialize_sb('/'.join([base_dir, sav_spellbook]))
        towns.deserialize_chests('/'.join([base_dir, sav_chests]))

        units.deserialize_player('/'.join([base_dir, sav_play]),
                                 '/'.join([base_dir, sav_solou]),
                                 '/'.join([base_dir, sav_xoann]),
                                 '/'.join([base_dir, sav_adorine]),
                                 '/'.join([base_dir, sav_chyme]),
                                 '/'.join([base_dir, sav_ran_af]),
                                 '/'.join([base_dir, sav_parsto]))

        print('Load successful.')

        return

    except (OSError, ValueError):
        logging.exception(f'Error loading game on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an error loading your game. Please reload game.')
        print('Error message can be found in the error_log.out file.')
        main.s_input("\nPress enter/return ")

        # A file failing to load screws up some internal values, so the entire game needs to be reloaded
        raise
