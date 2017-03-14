import configparser
import json
import logging
import os
import re
import sys
import time

import pygame

import inv_system
import items
import magic
import npcs
import sounds
import tiles
import units

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# Save File information
save_dir = 'Content/Save Files'
adventure_name = ''

# General Save Files
sav_acquired_gems = 'Content/Save Files//{ADVENTURE_NAME}/acquired_gems.json'    # Acquired Gems
sav_def_bosses = 'Content/Save Files/{ADVENTURE_NAME}/def_bosses.json'          # Defeated Bosses
sav_equip_items = 'Content/Save Files/{ADVENTURE_NAME}/equip_items.json'        # Equipped Items
sav_inventory = 'Content/Save Files/{ADVENTURE_NAME}/inventory.json'            # Inventory
sav_misc_boss_info = 'Content/Save Files/{ADVENTURE_NAME}/misc_boss_info.json'  # Misc Boss Info
sav_party_info = 'Content/Save Files/{ADVENTURE_NAME}/party_info.json'          # Party Info
sav_quests_dia = 'Content/Save Files/{ADVENTURE_NAME}/quests_dia.json'          # Quests & Dialogue
sav_spellbook = 'Content/Save Files/{ADVENTURE_NAME}/spellbook.json'            # Spellbook

# PCU Save Files
sav_play = 'Content/Save Files/{ADVENTURE_NAME}/play_stats.json'        # Player Stats
sav_solou = 'Content/Save Files/{ADVENTURE_NAME}/solou_stats.json'      # Solou's Stats
sav_xoann = 'Content/Save Files/{ADVENTURE_NAME}/xoann_stats.json'      # Xoann's Stats
sav_chyme = 'Content/Save Files/{ADVENTURE_NAME}/chyme_stats.json'      # Chyme's Stats
sav_ran_af = 'Content/Save Files/{ADVENTURE_NAME}/ran_af_stats.json'    # Ran'af's Stats
sav_parsto = 'Content/Save Files/{ADVENTURE_NAME}/parsto_stats.json'    # Parsto's Stats
sav_adorine = 'Content/Save Files/{ADVENTURE_NAME}/adorine_stats.json'  # Adorine's Stats

# Game Settings. Can be changed in the settings.cfg file.
music_vol = 1.0  # The volume of the game's Music, on a scale from 0 (muted) to 1.0 (loudest).
sound_vol = 1.0  # The volume of the game's SFX, on a scale from 0 (muted) to 1.0 (loudest).
divider_size = 25  # The number of dashes used for dividers between different UI elements


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
                y_n = input(f'\nI had to change some of that. Is "{adventure_name}" okay? | Yes or No: ').lower()

                if y_n.startswith("y"):
                    format_save_names()

                    if units.player.name.lower() == "give me the gold":
                        print("Gold cheat enabled, you now have 99999 gold!")
                        main.party_info['gp'] = 99999

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
                        main.party_info['gp'] = 99999

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
                     'sav_chyme', 'sav_adorine', 'sav_ran_af', 'sav_parsto'], key=str.lower):

        globals()[x] = globals()[x].format(ADVENTURE_NAME=adventure_name)


def change_settings():
    config = configparser.ConfigParser()

    if os.path.isfile("../settings.cfg"):
        config.read("../settings.cfg")

        for x in config['volume_levels']:
            globals()[x] = float(config['volume_levels'][x])/100

        for x in config['divider_size']:
            globals()[x] = int(config['divider_size'][x])

        sounds.change_volume()


def save_game(verbose=True):
    # Save important game data to .json files
    # If verbose == True, then this function will print everything and use smart_sleep() functions
    # When set to False, this function can be used to auto-save the game
    while True:
        y_n = input('Do you wish to save your progress? | Yes or No: ').lower() if verbose else 'y'

        if y_n.startswith('y'):
            print('Saving...') if verbose else ''
            main.smart_sleep(0.1) if verbose else ''

            # Check if the save directory already exists, and create it if it doesn't
            try:
                os.makedirs('/'.join([save_dir, adventure_name]))

            except FileExistsError:
                pass

            format_save_names()
            serialize_all(verbose)

            return

        elif y_n.startswith('n'):
            return


def load_game():  # Check for save files and load the game if they're found
    global adventure_name

    print('-'*divider_size)

    # Check each part of the save file
    print('Searching for valid save files...')
    if not os.path.isdir(save_dir):
        main.smart_sleep(0.1)

        print('No save files found. Starting new game...')
        main.smart_sleep(0.1)

        print('-'*divider_size)
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
        if all(map(os.path.isfile, [x.format(ADVENTURE_NAME=directory) for x in save_file_list])):
            # ...then set the dictionary key equal to the newly-formatted save file names
            save_files[directory] = [x.format(ADVENTURE_NAME=directory) for x in save_file_list]

            try:
                with open('/'.join([save_dir, directory, "menu_info.txt"]),
                          encoding='utf-8') as f:
                    menu_info[directory] = f.read()

            except FileNotFoundError:
                menu_info[directory] = "Unable to load preview info"

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
        chosen = input('Input [#] (or type "create new"): ').lower()

        try:
            # Account for the fact that list indices start at 0
            adventure_name = sorted(save_files)[int(chosen) - 1]

        except (ValueError, IndexError):
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
        with open(sav_def_bosses, mode='w', encoding='utf-8') as f:
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

        with open(sav_party_info, mode='w', encoding='utf-8') as f:
            json.dump(json_party_info, f, indent=4, separators=(', ', ': '))

        items.serialize_gems(sav_acquired_gems)
        inv_system.serialize_equip(sav_equip_items)
        inv_system.serialize_inv(sav_inventory)
        npcs.serialize_dialogue(sav_quests_dia)
        magic.serialize_sb(sav_spellbook)
        units.serialize_bosses(sav_misc_boss_info)
        units.serialize_player(sav_play, sav_solou, sav_xoann, sav_adorine, sav_chyme, sav_ran_af, sav_parsto)

        with open('/'.join([save_dir, adventure_name, 'menu_info.txt']), mode='w', encoding='utf-8') as f:
            f.write(f"NAME: {units.player.name} | LEVEL: {units.player.lvl} | CLASS: {units.player.class_.title()}")

        print('Save successful.') if verbose else ''

        return

    except (OSError, ValueError):
        logging.exception(f'Error saving game on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an error in saving. Error message can be found in error_log.out') if verbose else ''
        input("\nPress enter/return ") if verbose else ''


def deserialize_all():
    try:
        with open(sav_def_bosses, encoding='utf-8') as f:
            units.defeated_bosses = list(json.load(f))

        with open(sav_party_info, encoding='utf-8') as f:
            main.party_info = json.load(f)

        for key in main.party_info:
            if key in ['current_tile', 'prev_town'] and main.party_info[key]:
                for tile in tiles.all_tiles:
                    if main.party_info[key] == tile.tile_id:
                        main.party_info[key] = tile

        # Call functions to serialize more advanced things
        items.deserialize_gems(sav_acquired_gems)
        inv_system.deserialize_equip(sav_equip_items)
        inv_system.deserialize_inv(sav_inventory)
        units.deserialize_bosses(sav_misc_boss_info)
        npcs.deserialize_dialogue(sav_quests_dia)
        magic.deserialize_sb(sav_spellbook)
        units.deserialize_player(sav_play, sav_solou, sav_xoann, sav_adorine, sav_chyme, sav_ran_af, sav_parsto)

        print('Load successful.')

        return

    except (OSError, ValueError):
        logging.exception(f'Error loading game on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')
        print('There was an error loading your game. Please reload game.')
        print('Error message can be found in the error_log.out file.')
        input("\nPress enter/return ")

        # A file failing to load screws up some internal values, so the entire game needs to be reloaded
        raise
