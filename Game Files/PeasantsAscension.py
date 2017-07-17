#!/usr/bin/env python
# Peasants' Ascension v1.0.0 Beta
# --------------------------------------------------------------------------- #
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
# --------------------------------------------------------------------------- #
# Music by Ben Landis: http://www.benlandis.com/
# And Eric Skiff: http://ericskiff.com/music/
# --------------------------------------------------------------------------- #
# Contact me via Twitter (@TheFrozenMawile) or email (ninjafurret@gmail.com)
# for questions/feedback. Visit the subreddit at http://reddit.com/PeasantsAscension
# --------------------------------------------------------------------------- #
# Notes for people reading this code:
#  1. print('-'*save_load.divider_size) <-- This line appears constantly in my
#     code. It's purpose is to enhance readability and organization for people
#     playing the game.
#
#  2. I am completely open to any and all criticism! I'm still pretty new to
#     programming, so I need all the advice I can get. Bug reports are great
#     too! Contact information is near the top of this module.
#
#  3. If you encounter an error message at any point when playing this, please
#     email the error code to me. If you could provide a description of what
#     you did to cause the bug, that'd be great. Contact information is near
#     the top of the module.
#
#  4. I made an attempt to comment most of my code, and hopefully the rest is
#     pretty self-explanatory. But if you have any questions about how something
#     works or why something is the way it is, feel free to ask me! I love
#     answering questions!
# --------------------------------------------------------------------------- #

import ctypes
import logging
import msvcrt
import sys
import time
import traceback
import random

import pygame

# Some of the files are in different folders for some reason.
# Adding those folders to the path allows us to use the import statement to access them.
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Content")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Scripts")
sys.path.append("C:\\Users\Stephen Center\\Documents\\Peasants' Ascension\\Game Files\\Classes")

import tiles
import title_screen
import save_load
import towns
import sounds
import units
import battle
import inv_system
import ascii_art
import magic

# Log everything and send it to stderr.
logging.basicConfig(filename='../error_log.out', level=logging.DEBUG, format="\n%(message)s")

# Setup Pygame audio
pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# A dictionary containing generic information about the player's party
party_info = {'biome': 'forest',
              'music': 'Content/Music/Through the Forest.ogg',
              'prov': "Province of Overshire",
              'prev_town': tiles.in_for_c,
              'p_town_xyz': [0, 0, 0],
              'is_aethus': False,
              'gp': 20,
              'visited_towns': [],
              'current_tile': tiles.in_for_c,
              'x': 0, 'y': 0, 'z': 0,
              'steps_without_battle': 0,
              'do_monster_spawns': True,
              'scout_list': []}

# Set to 1 when auto-testing
do_debug = 0

# A list of usernames that my friend has used in the past. Adds a few easter eggs.
friend_names = ["apollo kalar", "apollokalar", "apollo_kalar",
                "flygon jones", "flygonjones", "flygon_jones",
                "cynder887", "gabe", "gabriel"]


def s_input(string):
    # Custom input, plays a "blip" sound after the player presses enter.
    # Also can be used to automatically play the game and find crashes.
    if do_debug:
        print(string, end='')
        char = random.choice('0123456789ynxpsewrtbu')
        print(char)

        return char

    x = input(string)

    if save_load.do_blip:
        sounds.item_pickup.play()

    return x


def smart_sleep(duration):
    # "Pauses" the game for a specific duration, and then does some magic to make everything work correctly

    if do_debug:
        duration = 0.05

    time.sleep(duration)

    # I have no idea how this works but I found it on Stack Overflow and it makes the text sync properly
    while msvcrt.kbhit():
        msvcrt.getwch()


def chop_by_79(string, padding=0, num=79):
    # Takes a string and coverts it into a list, cutting off at every 79th character.
    # Also does some magic to make sure that sentences don't get cut off mid w
    # ord
    sentences = []
    current_sentence = ''

    for word in string.split():
        if len(current_sentence + word) > num - padding:
            sentences.append(current_sentence)
            current_sentence = ''

        current_sentence += f'{word} '

    sentences.append(current_sentence) if current_sentence else ''

    return sentences


def game_loop():
    pygame.mixer.music.load(party_info['music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(save_load.music_vol)

    while True:
        if not towns.search_towns():
            print('-'*save_load.divider_size)

        # These lists will tell the game how to manipulate the players position in the next part of the function
        available_dirs = game_ui()

        while True:
            command = s_input('Input Command (type "help" to view command list): ').lower()

            if command == "debug-menu":
                debug_command()

            elif any(map(command.startswith, [x[0] for x in available_dirs])):
                move_command(available_dirs, command[0])

                break

            elif command.startswith('p'):
                stats_command()

            elif command.startswith('m'):
                magic_command()

            elif command.startswith('i'):
                inv_command()

            elif command.startswith('t'):
                tools_command()

            elif command.startswith('l'):
                look_command()

            elif command.startswith('r'):
                rest_command()

            elif command.startswith('h'):
                help_command()

            else:
                continue

            game_ui()


def check_region():
    # Check the coordinates of the player and change the music to match
    # Also alerts the player when they change biomes/provinces
    new_province = party_info['current_tile'].province
    new_biome = party_info['current_tile'].biome

    if new_biome == 'sky':
        music = 'Content/Music/Island of Peace.ogg'

    elif new_biome == 'graveyard':
        music = 'Content/Music/song21_02.ogg'

    elif new_biome == 'forest':
        music = 'Content/Music/Through the Forest.ogg'

    elif new_biome == 'mountain':
        music = 'Content/Music/Mountain.ogg'

    elif new_biome == 'tundra':
        music = 'Content/Music/Arpanauts.ogg'

    elif new_biome == 'desert':
        music = 'Content/Music/Come and Find Me.ogg'

    elif new_biome == 'swamp':
        music = 'Content/Music/Digital Native.ogg'

    elif new_biome == 'shore':
        music = "Content/Music/We're all under the stars.ogg"

    elif new_biome == 'cave':
        # TODO!! get music!
        pass

    elif new_biome == 'underworld':
        # TODO!! get music!
        pass

    elif new_biome == 'castle':
        music = "Content/Music/Castle.ogg"
        pass

    else:
        logging.debug(f'No music for biome "{new_biome}" on {time.strftime("%m/%d/%Y at %H:%M:%S")}')
        music = 'Content/Music/Through the Forest.ogg'

    if party_info['prov'] != new_province or party_info['biome'] != new_biome:

        if party_info['biome'] != new_biome:
            print(ascii_art.locations['new_biome'])
            print(f"Looks like your party's entering a {new_biome.title()}.")

            party_info['biome'] = new_biome
            party_info['music'] = music

            # Play that funky music
            pygame.mixer.music.load(music)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(save_load.music_vol)

            if not towns.search_towns(enter=False):
                print('-'*save_load.divider_size)

        if party_info['prov'] != new_province:
            print('-'*save_load.divider_size)
            print(f"You have left the {party_info['prov']} and are now entering the {new_province}.")

        s_input("\nPress enter/return ")

        return True

    return False


def game_ui():
    available_dirs = []
    coord_change = ['x', 0]
    mpi = party_info
    tile = mpi['current_tile']

    print(f"-CURRENT LOCATION-")
    print(mpi['current_tile'].generate_ascii())

    # Calculate the character's X, Y, and Z coordinates and create a string from them. The Z coordinate does not
    # change nearly as often as the other two, so don't display it unless it != 0.
    coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
    coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
    coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

    coordinates = ''.join([coord_y, coord_x, coord_z])

    print(f"Coordinates: {coordinates} | Province: [{tile.province}] | Region [{tile.name}]")

    # Tells the player which directions are available to go in
    for drc in [x for x in [tile.to_n, tile.to_s, tile.to_e, tile.to_w, tile.to_dn, tile.to_up] if x is not None]:
        if drc == tile.to_e:
            print("    To the [E]ast", end='')
            available_dirs.append(['e', drc])

        if drc == tile.to_w:
            print("    To the [W]est", end='')
            available_dirs.append(['w', drc])

        if drc == tile.to_n:
            print("    To the [N]orth", end='')
            available_dirs.append(['n', drc])

        if drc == tile.to_s:
            print("    To the [S]outh", end='')
            available_dirs.append(['s', drc])

        if drc == tile.to_up:
            print("    [U]pwards, above your party,", end='')
            available_dirs.append(['u', drc])

        if drc == tile.to_dn:
            print("    [D]ownwards, below your party,", end='')
            available_dirs.append(['d', drc])

        adj_tile = tiles.find_tile_with_id(drc)
        print(f" lies the {adj_tile.name}")

    return available_dirs


def move_command(available_dirs, command):
    sounds.item_pickup.stop()
    sounds.foot_steps.play()

    party_info['current_tile'] = [b for b in tiles.all_tiles if b.tile_id in
                                  [a[1] for a in available_dirs if a[0] == command]][0]

    # Translate the player's commandal s_input into a coordinate change
    for drc in [a[0] for a in available_dirs]:
        if drc == command == 'e':
            coord_change = ['x', 1]
        elif drc == command == 'w':
            coord_change = ['x', -1]
        elif drc == command == 'n':
            coord_change = ['y', 1]
        elif drc == command == 's':
            coord_change = ['y', -1]
        elif drc == command == 'u':
            coord_change = ['z', 1]
        elif drc == command == 'd':
            coord_change = ['z', -1]

    # Change the player's coordinates
    # This is purely visual - tiles are completely independent of coordinates
    party_info[coord_change[0]] += 1 * coord_change[1]

    # If none of these fucntions return True, then a battle can occur.
    if not any([check_region(), units.check_bosses(), towns.search_towns(enter=False)]):

        # There is a 1 in 4 chance for a battle to occur (25%)
        # However, a battle cannot occur if the number of steps since the last battle is less than three,
        # and is guaranteed to occur if the number of steps is above 10.
        is_battle = random.randint(0, 3) == 0

        if party_info['steps_without_battle'] > 10:
            is_battle = True

        elif party_info['steps_without_battle'] < 3:
            is_battle = False

        # Certain tiles can have battling disabled on them
        if is_battle and party_info['current_tile'].m_level != -1 and party_info['do_monster_spawns']:
            print('-' * save_load.divider_size)
            units.spawn_monster()
            battle.battle_system()
            party_info['steps_without_battle'] = 0

        else:
            party_info['steps_without_battle'] += 1


def help_command():
    # Peasant's Ascension
    print('-'*save_load.divider_size)
    print("""Command List:
 [NSEW] - Moves your party if the selected direction is unobstructed
 [L]ook - Displays a description of your current location
 [P]arty Stats - Displays the stats of a specific party member
 [T]ool Menu - Allows you to quickly use tools without opening your inventory
 [M]agic - Allows you to use healing spells outside of battle
 [R]est - Heals your party member while in the overworld
 [I]nventory - Displays your inventory and lets you equip/use items
 [H]elp - Reopen this list of commands
Type the letter in brackets while on the overworld to use the command""")

    s_input("\nPress enter/return ")


def stats_command():
    print('-'*save_load.divider_size)
    print('You stop to rest for a moment.')

    target_options = [x for x in [units.player,
                                  units.solou,
                                  units.xoann,
                                  units.adorine,
                                  units.ran_af,
                                  units.parsto,
                                  units.chyme] if x.enabled]

    if len(target_options) == 1:
        target = units.player

    else:
        print("Select Character:")

        for num, character in enumerate(target_options):
            print(f"      [{int(num) + 1}] {character.name}")

        while True:
            target = s_input('Input [#] (or type "exit"): ').lower()

            try:
                target = target_options[int(target) - 1]

            except (IndexError, ValueError):
                if target in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)

                    break

                continue

            break

    if isinstance(target, units.PlayableCharacter):
        print('-'*save_load.divider_size)
        target.player_info()
        print('-'*save_load.divider_size)


def inv_command():
    print('-'*save_load.divider_size)
    inv_system.pick_category()
    print('-'*save_load.divider_size)


def magic_command():
    units.player.choose_target("Choose Spellbook:", ally=True, enemy=False)

    if magic.spellbook[units.player.target.name if units.player.target != units.player else 'player']['Healing']:
        magic.pick_spell('Healing', units.player.target, False)

    else:
        print('-'*save_load.divider_size)
        print(f'{units.player.target.name} has no overworld spells in their spellbook.')
        s_input("\nPress enter/return ")


def look_command():
    print('-'*save_load.divider_size)
    print(party_info['current_tile'].desc)
    s_input("\nPress enter/return ")
    print('-'*save_load.divider_size)


def rest_command():
    # Attempt to re-gain health on the world map. There is a chance to get ambushed by an enemy
    # when doing this.
    # TODO!! THIS DOESN'T WORK AT ALL!!
    print('-'*save_load.divider_size)

    if all([units.player.hp == units.player.max_hp and units.player.mp == units.player.max_mp,
            units.solou.hp == units.solou.max_hp and units.solou.mp == units.solou.max_mp,
            units.xoann.hp == units.xoann.max_hp and units.xoann.mp == units.xoann.max_mp,
            units.chyme.hp == units.chyme.max_hp and units.chyme.mp == units.chyme.max_mp,
            units.ran_af.hp == units.ran_af.max_hp and units.ran_af.mp == units.ran_af.max_mp,
            units.parsto.hp == units.parsto.max_hp and units.parsto.mp == units.parsto.max_mp,
            units.adorine.hp == units.adorine.max_hp and units.adorine.mp == units.adorine.max_mp]):

        print('Your party feels fine and decides not to rest.')
        s_input("\nPress enter/return ")
        print('-'*save_load.divider_size)

        return

    print(ascii_art.locations['Campsite'])
    print('Your party sets up camp and begin to rest.')

    smart_sleep(1)

    is_battle = not random.randint(0, 3)

    if is_battle and party_info['do_monster_spawns']:
        units.spawn_monster()
        battle.battle_system(ambush=True)

    else:
        units.fix_stats()

        # Revive any dead characters
        if units.player.status_ail == 'dead':
            units.player.status_ail = 'none'

        if units.solou.status_ail == 'dead':
            units.solou.status_ail = 'none'

        if units.xoann.status_ail == 'dead':
            units.xoann.status_ail = 'none'

        if units.chyme.status_ail == 'dead':
            units.chyme.status_ail = 'none'

        if units.ran_af.status_ail == 'dead':
            units.ran_af.status_ail = 'none'

        if units.parsto.status_ail == 'dead':
            units.parsto.status_ail = 'none'

        if units.adorine.status_ail == 'dead':
            units.adorine.status_ail = 'none'

        print('You rested well and decide to continue on your way.')
        if not towns.search_towns(enter=False):
            print('-'*save_load.divider_size)


def tools_command():
    tool_names = ['Divining Rod', 'Shovel', 'Magical Compass', 'Map of Fast Travel', 'Boots of Insane Speed']
    available_tools = []

    for cat in inv_system.inventory:
        if cat in ['coord', 'quests']:
            continue

        for item in inv_system.inventory[cat]:
            if item.name in tool_names:
                available_tools.append(item)

    print('-'*save_load.divider_size)

    if not available_tools:
        print('Your party has no available tools to use.')
        s_input('\nPress enter/return ')
        print('-'*save_load.divider_size)

        return

    while True:
        print('Tools: ')

        for x, y in enumerate(available_tools):
            print(f"      [{x + 1}] {y.name}")

        while True:
            tool = s_input('Input [#] (or type "exit"): ').lower()

            try:
                tool = available_tools[int(tool) - 1]

            except (IndexError, ValueError):
                if tool in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)

                    return

                continue

            tool.use_item(units.player)

            print('-'*save_load.divider_size)

            break


def debug_command():
    # Opens the debug menu. Allows the player to enter in Python Code in order to manipulate in-game variables.
    # Extremely powerful, but can potentially ruin the game state if the player doesn't know what they're doing.
    # Use with caution.
    print('-'*save_load.divider_size)
    print('-DEBUG MENU-')
    while True:
        command = s_input('Input command (or type "exit"): ')

        if command in ['e', 'x', 'exit', 'b', 'back']:
            print('-'*save_load.divider_size)

            break

        try:
            print(ascii_art.colorize(f">{command}", 'green'))
            exec(command)

        except:
            print(ascii_art.colorize(f">Invalid Command, `{command}`", 'red'))


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


def main():
    # main() handles all the setup for the game, and includes the main game loop.
    # Everything happens in this function in one way or another.

    set_prompt_properties()  # Set the CMD size and whatnot...
    save_load.change_settings()  # ...set the volume and save file settings...
    title_screen.show_title()  # ...display the titlescreen...
    save_load.load_game()  # ...check for save files...
    game_loop()  # ...and then start the game!


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    try:
        # Run the game.
        main()

    except Exception as e:
        # If an exception is raised and not caught, log the error message.
        logging.exception(f'Got exception of main handler on {time.strftime("%m/%d/%Y at %H:%M:%S")}:')

        # raise # Uncomment this if you're using the auto-s_input debugger

        print(traceback.format_exc())
        print("""\
Peasants' Ascension encountered an error and crashed! Send the error message
shown above to TheFrozenMawile (ninjafurret@gmail.com) to make sure the bug
gets fixed. The error message, along with any errors messages encountered,
can also be found in the error_log.out file.""")
        s_input("\nPress enter/return")

        pygame.quit()
        sys.exit()
