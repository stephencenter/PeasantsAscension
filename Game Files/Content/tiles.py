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

import random
import sys

import pygame

import ascii_art
import battle
import inv_system
import magic
import save_load
import sounds
import towns
import units
from TileClass import Tile

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# -- INNER CENTRAL FOREST -- #
icf_desc = """Your party lies in the inner portion of the Central Forest. This very forest
is home to thousands of people and animal species, and, unfortunately, several kinds
of monsters. There are trees in all directions as far as the eye can see, each
towering over a hundred feet tall. The ground is scattered with the occasional rock
and a plentiful supply of leaves twigs. In other words, it's your standard forest.
The Inner Central Forest makes up only a small fraction of the 150 million acre
Central Forest, and is surrounded by a 12-foot wide moat."""

in_for_n = Tile("Inner Central Forest", "I-CF-N", "Central Forest", icf_desc, 1,
                to_s="I-CF-C",
                to_e="Nearton",
                to_w="I-CF-NW",
                to_n="I-CF-Bridge")
in_for_s = Tile("Inner Central Forest", "I-CF-S", "Central Forest", icf_desc, 1,
                to_n="I-CF-C",
                to_w="Southford",
                to_e="I-CF-SE")
in_for_e = Tile("Inner Central Forest", "I-CF-E", "Central Forest", icf_desc, 1,
                to_n="Nearton",
                to_w="I-CF-C",
                to_s="I-CF-SE")
in_for_w = Tile("Inner Central Forest", "I-CF-W", "Central Forest", icf_desc, 1,
                to_s="Southford",
                to_e="I-CF-C",
                to_n="I-CF-NW")
in_for_c = Tile("Inner Central Forest", "I-CF-C", "Central Forest", icf_desc, 1,
                to_n="I-CF-N",
                to_w="I-CF-W",
                to_e="I-CF-E",
                to_s="I-CF-S")
in_for_nw = Tile("Inner Central Forest", "I-CF-NW", "Central Forest", icf_desc, 2,
                 to_s="I-CF-W",
                 to_e="I-CF-N")
in_for_se = Tile("Inner Central Forest", "I-CF-SE", "Central Forest", icf_desc, 2,
                 to_w="I-CF-S",
                 to_n="I-CF-E")

nearton_tile = Tile("Town of Nearton", "Nearton", "Central Forest", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2,
                    town_list=[towns.town_nearton],
                    to_s="I-CF-E",
                    to_w="I-CF-N")

southford_tile = Tile("Town of Southford", "Southford", "Central Forest", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2,
                      town_list=[towns.town_southford],
                      to_e="I-CF-S",
                      to_n="I-CF-W")

icf_bridge = Tile("Inner Forest Bridge", "I-CF-Bridge", "Central Forest", icf_desc + """\n
This bridge extends over the 12ft-wide moat surrounding the Inner Central Forest, meant
to help protect its citizens from the harmful monsters outside it. Weaker monsters still
manage to make their way in though.""", 0,
                  to_s="I-CF-N",
                  to_n="W-CF-2")

# -- WEST OF THE HYTHOS RIVER -- #
whr_desc = """The Central Forest is divided into two smaller regions by the
immeasurably-large Hythos River. Your party lies to the West of this river,
in an area aptly-referred to as "West of the Hythos River". Known to the
denizens as "West Hythos", this land is home to dozens of towns and - despite
the efforts of the Harconian Militia - uncountable swaths of evils beasts.
While not nearly as dense tree-wise as the Inner Forest, West Hythos more than
makes makes up for it in size. Around 70% of the 150-million acre Central
Forest lies right here in West Hythos. Without a compass it would be incredibly
difficult to maintain ones whereabouts here."""

whr_tile2 = Tile("West of the Hythos River", "W-CF-1", "Central Forest", whr_desc, 3,
                 to_e="W-CF-2",
                 to_n="W-CF-4")
whr_tile1 = Tile("West of the Hythos River", "W-CF-2", "Central Forest", whr_desc, 3,
                 to_s="I-CF-Bridge",
                 to_w="W-CF-1",
                 to_e="W-CF-3",
                 to_n="W-CF-5")
whr_tile3 = Tile("West of the Hythos River", "W-CF-3", "Central Forest", whr_desc, 3,
                 to_w="W-CF-2",
                 to_n="W-CF-6")
whr_tile4 = Tile("West of the Hythos River", "W-CF-4", "Central Forest", whr_desc, 4,
                 to_s="W-CF-1",
                 to_e="W-CF-5")
whr_tile5 = Tile("West of the Hythos River", "W-CF-5", "Central Forest", whr_desc, 3,
                 to_s="W-CF-2",
                 to_w="W-CF-4",
                 to_e="W-CF-6")
whr_tile6 = Tile("West of the Hythos River", "W-CF-6", "Central Forest", whr_desc, 4,
                 to_s="W-CF-3",
                 to_w="W-CF-5")


# -- CENTRAL FOREST TILESETS -- #

# Inner Central Forest
icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s,
             in_for_n, in_for_se, in_for_nw, icf_bridge]

# West of the Hythos River
whr_tiles = [whr_tile1, whr_tile2, whr_tile3, whr_tile4, whr_tile5, whr_tile6]

# East of the Hythos River
ehr_tiles = []


all_tiles = icf_tiles + whr_tiles + ehr_tiles  # + other tiles lists as more tiles come into existence


def movement_system():
    pygame.mixer.music.load(main.party_info['reg_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(save_load.music_vol)

    while True:
        if not towns.search_towns():
            print('-'*save_load.divider_size)

        # These lists will tell the game how to manipulate the players position in the next part of the function
        coord_change, available_dirs = movement_hud()

        while True:
            command = input('Input Command (type "help" to view command list): ').lower()

            if command == "debug-menu":
                debug_command()

            elif any(map(command.startswith, [x[0] for x in available_dirs])):
                move_command(coord_change, available_dirs, command)

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

            movement_hud()


# noinspection PyUnboundLocalVariable
def check_region():
    # Check the coordinates of the player and change the region to match.
    new_region = main.party_info['current_tile'].region

    if new_region == 'The Aethus':
        reg_music = 'Music/Island of Peace.ogg'

    elif new_region == 'Overshire Graveyard':
        reg_music = 'Music/Frontier.ogg'

    elif new_region == 'Central Forest':
        reg_music = 'Music/Through the Forest.ogg'

    elif new_region == 'Terrius Mt. Range':
        reg_music = 'Music/Mountain.ogg'

    elif new_region == 'Glacian Plains':
        reg_music = 'Music/Arpanauts.ogg'

    elif new_region == 'Arcadian Desert':
        reg_music = 'Music/Come and Find Me.ogg'

    elif new_region == 'Bogthorn Marsh':
        reg_music = 'Music/Digital Native.ogg'

    elif new_region == 'Harconian Coastline':
        reg_music = "Music/We're all under the stars.ogg"

    if main.party_info['reg'] != new_region:
        print('-'*save_load.divider_size)
        print(ascii_art.locations[new_region])
        print(f"You have left the {main.party_info['reg']} and are now entering the {new_region}.")

        main.party_info['reg'] = new_region
        main.party_info['reg_music'] = reg_music

        # Change the music & play it
        pygame.mixer.music.load(reg_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(save_load.music_vol)

        if not towns.search_towns(enter=False):
            print('-'*save_load.divider_size)

        return True

    else:
        return False


def movement_hud():
    available_dirs = []
    coord_change = ['x', 0]
    mpi = main.party_info
    tile = mpi['current_tile']

    print(f"-CURRENT LOCATION-")
    print(mpi['current_tile'].generate_ascii())

    # Calculate the character's X, Y, and Z coordinates and create a string from them. The Z coordinate does not
    # change nearly as often as the other two, so don't display it unless it != 0.
    coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
    coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
    coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""

    coordinates = ''.join([coord_y, coord_x, coord_z])

    print(f"Coordinates: {coordinates} | Region: [{tile.region}] | Subregion [{tile.name}]")

    for drc in [x for x in [tile.to_n, tile.to_s, tile.to_e, tile.to_w, tile.to_dn, tile.to_up] if x is not None]:
        if drc == tile.to_e:
            print("    To the [E]ast", end='')
            available_dirs.append(['e', drc])
            coord_change = ['x', 1]

        if drc == tile.to_w:
            print("    To the [W]est", end='')
            available_dirs.append(['w', drc])
            coord_change = ['x', -1]

        if drc == tile.to_n:
            print("    To the [N]orth", end='')
            available_dirs.append(['n', drc])
            coord_change = ['y', 1]

        if drc == tile.to_s:
            print("    To the [S]outh", end='')
            available_dirs.append(['s', drc])
            coord_change = ['y', -1]

        if drc == tile.to_up:
            print("    [U]pwards, above your party,", end='')
            available_dirs.append(['u', drc])
            coord_change = ['z', 1]

        if drc == tile.to_dn:
            print("    [D]ownwards, below your party,", end='')
            available_dirs.append(['d', drc])
            coord_change = ['z', -1]

        for t in all_tiles:
            if t.tile_id == drc:
                adj_tile = t

                break

        print(f" lies the {adj_tile.name}")

    return coord_change, available_dirs


def move_command(coord_change, available_dirs, command):
    sounds.foot_steps.play()

    main.party_info['current_tile'] = [b for b in all_tiles if b.tile_id in
                                       [a[1] for a in available_dirs if a[0] == command]][0]

    # Translate the player's commandal input into a coordinate change
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
    main.party_info[coord_change[0]] += 1 * coord_change[1]

    # If none of these fucntions return True, then a battle can occur.
    if not any([check_region(), units.check_bosses(), towns.search_towns(enter=False)]):

        # There is a 1 in 4 chance for a battle to occur (25%)
        # However, a battle cannot occur if the number of steps since the last battle is less than three,
        # and is guaranteed to occur if the number of steps is above 10.
        is_battle = random.randint(0, 3) == 0

        if main.party_info['steps_without_battle'] > 10:
            is_battle = True

        elif main.party_info['steps_without_battle'] < 3:
            is_battle = False

        # Certain tiles can have battling disabled on them
        if is_battle and main.party_info['current_tile'].m_level != -1:
            print('-' * save_load.divider_size)
            units.spawn_monster()
            battle.battle_system()
            main.party_info['steps_without_battle'] = 0

        else:
            main.party_info['steps_without_battle'] += 1


def help_command():
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

    input("\nPress enter/return ")


def stats_command():
    print('-' * 25)
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
            target = input('Input [#] (or type "exit"): ').lower()

            try:
                target = target_options[int(target) - 1]

            except (ValueError, IndexError):
                if target in ['e', 'x', 'exit', 'b', 'back']:
                    print('-' * 25)

                    break

                continue

            break

    if isinstance(target, units.PlayableCharacter):
        print('-' * 25)
        target.player_info()
        print('-' * 25)


def inv_command():
    inv_system.pick_category()
    print('-' * 25)


def magic_command():
    units.player.choose_target("Choose Spellbook:", ally=True, enemy=False)

    if magic.spellbook[units.player.target.name if units.player.target != units.player else 'player']['Healing']:
        magic.pick_spell('Healing', units.player.target, False)

    else:
        print('-' * 25)
        print(f'{units.player.target.name} has no overworld spells in their spellbook.')
        input("\nPress enter/return ")


def look_command():
    print('-' * 25)
    print(main.party_info['current_tile'].desc)
    input("\nPress enter/return ")
    print('-' * 25)


def rest_command():
    # Attempt to re-gain health on the world map. There is a chance to get ambushed by an enemy
    # when doing this.
    print('-'*save_load.divider_size)

    if all([units.player.hp == units.player.max_hp and units.player.mp == units.player.max_mp,
            units.solou.hp == units.solou.max_hp and units.solou.mp == units.solou.max_mp,
            units.xoann.hp == units.xoann.max_hp and units.xoann.mp == units.xoann.max_mp,
            units.chyme.hp == units.chyme.max_hp and units.chyme.mp == units.chyme.max_mp,
            units.ran_af.hp == units.ran_af.max_hp and units.ran_af.mp == units.ran_af.max_mp,
            units.parsto.hp == units.parsto.max_hp and units.parsto.mp == units.parsto.max_mp,
            units.adorine.hp == units.adorine.max_hp and units.adorine.mp == units.adorine.max_mp]):

        print('Your party feels fine and decides not to rest.')
        input("\nPress enter/return ")
        print('-'*save_load.divider_size)

        return

    print(ascii_art.locations['Campsite'])
    print('Your party sets up camp and begin to rest.')

    main.smart_sleep(1)

    is_battle = not random.randint(0, 3)

    if is_battle:
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

    print('-' * 25)

    if not available_tools:
        print('Your party has no available tools to use.')
        input('\nPress enter/return ')
        print('-' * 25)

        return

    while True:
        print('Tools: ')

        for x, y in enumerate(available_tools):
            print(f"      [{x + 1}] {y}")

        while True:
            tool = input('Input [#] (or type "exit"): ').lower()

            try:
                tool = available_tools[int(tool) - 1]

            except (IndexError, ValueError):
                if tool in ['e', 'x', 'exit', 'b', 'back']:
                    print('-' * 25)

                    return

                continue

            tool.use_item(units.player)

            print('-' * 25)

            break


def debug_command():
    # Opens the debug menu. Allows the player to enter in Python Code in order to manipulate in-game variables.
    # Extremely powerful, but can potentially ruin the game state if the player doesn't know what they're doing.
    # Use with caution.
    print('-'*save_load.divider_size)
    print('-DEBUG MENU-')
    while True:
        command = input('Input command (or type "exit"): ')

        if command in ['e', 'x', 'exit', 'b', 'back']:
            print('-' * 25)

            break

        try:
            print(ascii_art.colorize(f">{command}", 'green'))
            exec(command)

        except:
            print(ascii_art.colorize(f">Invalid Command, `{command}`", 'red'))


def find_tile_with_id(tile_id):
    # A very simple function that scans through a list of all existing Tile objects and returns the first
    # one it finds with the inputted tile_id

    for tile in all_tiles:
        if tile.tile_id == tile_id:
            return tile

    return False
