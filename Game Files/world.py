#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
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
# ------------------------------------------------------------------------ #
# Map of the Arcadian Continent: http://tinyurl.com/arcadia-map-v5

import sys
import random
import time
import math
import pygame

import battle
import units
import towns
import bosses
import sounds
import inv_system
import magic
import ascii_art

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


class Tile:
    def __init__(self, name, tile_id, region, desc, m_level, to_n=None, to_s=None, to_e=None, to_w=None, to_up=None,
                 to_dn=None, town_list=(), visited=False, enterable=True, level_req=1):

        self.name = name
        self.tile_id = tile_id
        self.region = region
        self.desc = desc
        self.m_level = m_level
        self.to_n = to_n
        self.to_s = to_s
        self.to_e = to_e
        self.to_w = to_w
        self.to_up = to_up
        self.to_dn = to_dn
        self.visited = visited
        self.enterable = enterable
        self.town_list = town_list
        self.level_req = level_req

# -- INNER CENTRAL FOREST -- #
icf_desc = """Your party lies in the inner portion of the Central Forest. This very forest
is home to thousands of people and animal species, and, unfortunately, several kinds
of monsters. There are trees in all directions as far as the eye can see, each
towering over a hundred feet tall. The ground is scattered with the occasional rock
and a plentiful supply of leaves twigs. In other words, it's your standard forest."""

in_for_n = Tile("Inner Central Forest", "I-CF-N", "Central Forest", icf_desc, 1,
                to_s="I-CF-C",
                to_e="Nearton",
                to_w="I-CF-NW")
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

nearton_tile = Tile("Town of Nearton", "Nearton", "Central Forest", icf_desc + """
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2, town_list=[towns.town_nearton],
                    to_s="I-CF-E",
                    to_w="I-CF-N")

southford_tile = Tile("Town of Southford", "Southford", "Central Forest", icf_desc + """
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2, town_list=[towns.town_southford],
                      to_e="I-CF-S",
                      to_n="I-CF-W")

icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s, in_for_n, in_for_se, in_for_nw]
all_tiles = icf_tiles # + other tiles lists as more tiles come into existance


def movement_system():
    pygame.mixer.music.load(main.party_info['reg_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(main.music_vol)

    while True:
        available_dirs = []
        coord_change = []

        mpi = main.party_info
        tile = mpi['current_tile']

        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"{mpi['z'] if mpi['z'] != 0 else ''}'{'UP' if mpi['z'] > 0 else 'DOWN' if mpi['z'] < 0 else ''}"
        coordinates = ''.join([coord_y, coord_x, coord_z])
        towns.search_towns()

        print(f"  -CURRENT LOCATION-")
        print(f"Coordinates: {coordinates} Region: [{tile.region}] | Subregion [{tile.name}]")
        for drc in [x for x in [tile.to_n, tile.to_s, tile.to_e, tile.to_w, tile.to_dn, tile.to_up] if x is not None]:
            if drc == tile.to_e:
                print("          To the [E]ast", end='')
                available_dirs.append(['e', drc])
                coord_change = ['x', 1]

            if drc == tile.to_w:
                print("          To the [W]est", end='')
                available_dirs.append(['w', drc])
                coord_change = ['x', -1]

            if drc == tile.to_n:
                print("          To the [N]orth", end='')
                available_dirs.append(['n', drc])
                coord_change = ['y', 1]

            if drc == tile.to_s:
                print("          To the [S]outh", end='')
                available_dirs.append(['s', drc])
                coord_change = ['y', -1]

            if drc == tile.to_up:
                print("                 [U]pwards, above your party,", end='')
                available_dirs.append(['u', drc])
                coord_change = ['z', 1]

            if drc == tile.to_dn:
                print("                 [D]ownwards, below your party,", end='')
                available_dirs.append(['d', drc])
                coord_change = ['z', -1]

            for t in all_tiles:
                if t.tile_id == drc:
                    adj_tile = t

                    break

            print(f" lies the {adj_tile.name}")

        while True:
            direction = input('Input Direction ([N], [S], [E], [W]) or [P]layer, [T]ools, [L]ook, [R]est: ').lower()

            if any(map(direction.startswith, [x[0] for x in available_dirs])):
                sounds.foot_steps.play()
                main.party_info['current_tile'] = [b for b in all_tiles if b.tile_id in
                                                   [a[1] for a in available_dirs if a[0] == direction]][0]

                for drc in [a[0] for a in available_dirs]:
                    if drc == direction == 'e':
                        coord_change = ['x', 1]
                    elif drc == direction == 'w':
                        coord_change = ['x', -1]
                    elif drc == direction == 'n':
                        coord_change = ['y', 1]
                    elif drc == direction == 's':
                        coord_change = ['y', -1]
                    elif drc == direction == 'u':
                        coord_change = ['z', 1]
                    elif drc == direction == 'd':
                        coord_change = ['z', -1]

                main.party_info[coord_change[0]] += 1*coord_change[1]

                if not towns.search_towns(enter=False):
                    print('-'*25)

                break

            elif direction.startswith('p'):
                print('-'*25)
                print('You stop to rest for a moment.')

                while True:
                    decision = input('View [i]nventory, [s]tats, or [m]agic? | Input Letter (or type "exit"): ')
                    decision = decision.lower()

                    if decision.startswith('i'):
                        print('-'*25)
                        inv_system.pick_category()
                        print('-'*25)

                    if decision.startswith('s'):
                        target_options = [x for x in [
                            units.player,
                            units.solou,
                            units.xoann,
                            units.adorine,
                            units.ran_af,
                            units.parsto,
                            units.chyme] if x.enabled
                        ]

                        if len(target_options) == 1:
                            target = units.player

                        else:
                            print("Select Character:")
                            print("     ", "\n      ".join(
                                ["[{0}] {1}".format(int(num) + 1, character.name)
                                 for num, character in enumerate(target_options)]))

                            while True:
                                target = input('Input [#] (or type "exit"): ')

                                try:
                                    target = target_options[int(target) - 1]

                                except (ValueError, IndexError):
                                    if target.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                        print('-'*25)

                                        break

                                    continue

                                break

                        if isinstance(target, units.PlayableCharacter):
                            print('-'*25)
                            target.player_info()
                            print('-'*25)

                    if decision.startswith('m'):
                        user_options = [x for x in [
                            units.player,
                            units.solou,
                            units.xoann,
                            units.adorine,
                            units.ran_af,
                            units.parsto,
                            units.chyme] if x.enabled
                        ]

                        if len(user_options) == 1:
                            user = units.player

                        else:
                            print('-'*25)
                            print("Select Spellbook:")
                            print("     ", "\n      ".join(
                                ["[{0}] {1}'s Spells".format(int(num) + 1, character.name)
                                 for num, character in enumerate(user_options)]))

                            while True:
                                user = input("Input [#]: ")
                                try:
                                    user = int(user) - 1
                                except ValueError:
                                    continue

                                try:
                                    user = user_options[user]
                                except IndexError:
                                    continue

                                break

                        if magic.spellbook[user.name if user != units.player else 'player']['Healing']:
                            magic.pick_spell('Healing', user, False)

                        else:
                            print('-'*25)
                            print('You have no overworld-allowed spells available.')

                    if decision in ['e', 'x', 'exit', 'b', 'back']:
                        print('-'*25)
                        break

            elif direction.startswith('t'):
                inv_system.tools_menu()
                if towns.search_towns(enter=False):
                    print('-'*25)

            elif direction.startswith('l'):
                print('-'*25)
                print(tile.desc)
                input("\nPress enter/return ")
                print('-'*25)

                break

            elif direction.startswith('r'):
                rest()
                if towns.search_towns(enter=False):
                    print('-'*25)


# def OLD_movement_system():
#     # Adjust the player's x/y coordinates based on inputted direction.
#
#     pygame.mixer.music.load(main.party_info['reg_music'])
#     pygame.mixer.music.play(-1)
#     pygame.mixer.music.set_volume(main.music_vol)
#
#     while True:
#         towns.search_towns(main.party_info['x'], main.party_info['y'])
#
#         if main.party_info['x'] >= 0:
#             main.party_info['h'] = "\u00b0E"
#         else:
#             main.party_info['h'] = "\u00b0W"
#
#         if main.party_info['y'] >= 0:
#             main.party_info['v'] = "\u00b0N"
#         else:
#             main.party_info['v'] = "\u00b0S"
#
#         print('Current Location: <{0}{1}, {2}{3}> in the <{4}>'.format(
#                 main.party_info['y'], main.party_info['v'],
#                 main.party_info['x'], main.party_info['h'],
#                 main.party_info['reg']))
#
#         while True:
#             direction = input('Input Direction ([N], [S], [E], [W]) or [P]layer, [T]ools, [L]ook, [R]est: ')
#             direction = direction.lower()
#
#             if any(map(direction.startswith, ['n', 's', 'w', 'e'])):
#                 sounds.foot_steps.play()
#
#                 # The in-game map is square to simplify things. The real map of the country is a lot different.
#                 if direction.startswith('n'):
#
#                     if main.party_info['y'] < 125 if not main.party_info['is_aethus'] else 50:
#                         main.party_info['y'] += 1
#
#                     else:
#                         print('-'*25)
#
#                         if main.party_info['is_aethus']:  # Aethus is a floating island in the sky
#                             print("""\
# Continuing to walk in that direction would cause you to fall to your death.
# It's probably in your best interests that you not do that.
# -------------------------""")
#
#                             continue
#
#                         if main.party_info['x'] <= 42:
#                             print('Off in the distance, you see what appears to be a large')
#                             print('island. According to your map, this island is known as')
#                             print('Durcuba. You probably shouldn\'t go there.')
#
#                         else:
#                             print('You come across the border between Hillsbrad and Harconia.')
#                             print('Despite your pleading, the border guards will not let you \
# pass.')
#
#                         print('-'*25)
#
#                         continue
#
#                 elif direction.startswith('s'):
#                     if main.party_info['y'] > -125 if not main.party_info['is_aethus'] else -50:
#                         main.party_info['y'] -= 1
#
#                     else:
#                         print('-'*25)
#
#                         if main.party_info['is_aethus']:  # Aethus is a floating island in the sky
#                             print("""\
# Continuing to walk in that direction would cause you to fall to your death.
# It's probably in your best interests that you not do that.
# -------------------------""")
#
#                             continue
#
#                         if main.party_info['x'] <= 42:
#                             print('You see a large island off in the distance. According to')
#                             print('your map, this island appears to be Thex! Unfortunately,')
#                             print("you don't have any way to cross the sea.")
#
#                         else:
#                             print('You come across the border between Maranon and Harconia.')
#                             print('Despite your pleading, the border guards will not let you \
# pass.')
#                         print('-'*25)
#
#                         continue
#
#                 elif direction.startswith('w'):
#                     if main.party_info['x'] > -125 if not main.party_info['is_aethus'] else -50:
#                         main.party_info['x'] -= 1
#
#                     else:
#                         print('-'*25)
#
#                         if main.party_info['is_aethus']:  # Aethus is a floating island in the sky
#                             print("""Continuing to walk in that direction would cause you to fall to your death.
# It's probably in your best interests that you not do that.
# -------------------------""")
#
#                             continue
#
#                         print('Ahead of you is a seemingly endless ocean. You cannot continue in this direction.')
#                         print('-'*25)
#
#                         continue
#
#                 elif direction.startswith('e'):
#                     if main.party_info['x'] < 125 if not main.party_info['is_aethus'] else 50:
#                         main.party_info['x'] += 1
#
#                     else:
#                         print('-'*25)
#
#                         if main.party_info['is_aethus']:  # Aethus is a floating island in the sky
#                             print("""Continuing to walk in that direction would cause you to fall to your death.
# It's probably in your best interests that you not do that.
# -------------------------""")
#
#                             continue
#
#                         if main.party_info['y'] >= 42:
#                             nation = 'Hillsbrad'
#
#                         elif main.party_info['y'] <= -42:
#                             nation = 'Maranon'
#
#                         else:
#                             nation = 'Elysium'
#
#                         print('You come across the border between {0} and Harconia.'.format(
#                             nation))
#                         print('Despite your pleading, the border guards will not let you pass.')
#                         print('-'*25)
#
#                         continue
#
#                 main.party_info['avg'] = int(((abs(main.party_info['x'])) + (abs(main.party_info['y'])))/2)
#
#                 if not any([check_region(),
#                            bosses.check_bosses(main.party_info['x'], main.party_info['y']),
#                            towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False)]
#                            ):
#
#                     # If none of the previous statements return True, then a battle can occur.
#                     # There is a 1 in 7 chance for a battle to occur (14.285714...%)
#                     is_battle = not random.randint(0, 6)
#
#                     if is_battle:
#                         print('-'*25)
#                         units.spawn_monster()
#                         battle.battle_system()
#
#                     else:
#                         print()
#
#                 break


def check_region():
    # Check the coordinates of the player and change the region to match.
    x, y = main.party_info['x'], main.party_info['y']

    if main.party_info['is_aethus']:
        region = 'Aethus'
        reg_music = 'Music/Island of Peace.ogg'

    else:
        if x in range(-15, -9) and y in range(5, 11):  # Micro-region in the Forest
            region = 'Overshire Graveyard'
            reg_music = 'Music/Frontier.ogg'

        elif x in range(-50, 51) and y in range(-50, 51):  # Center of World
            region = 'Central Forest'
            reg_music = 'Music/Through the Forest.ogg'

        elif x in range(-115, 1) and y in range(0, 116):  # Northwest of World
            region = 'Terrius Mt. Range'
            reg_music = 'Music/Mountain.ogg'

        elif x in range(-115, 0) and y in range(-115, 1):  # Southwest of World
            region = 'Glacian Plains'
            reg_music = 'Music/Arpanauts.ogg'

        elif x in range(0, 126) and y in range(0, 126):  # Northeast of world
            region = 'Arcadian Desert'
            reg_music = 'Music/Come and Find Me.ogg'

        elif x in range(0, 126) and y in range(-115, 1):  # Southeast of World
            region = 'Bogthorn Marsh'
            reg_music = 'Music/Digital Native.ogg'

        elif -1*abs(x) in range(-125, -115) or -1*abs(y) in range(-126, -115):  # Edges of World
            region = 'Harconian Coastline'
            reg_music = "Music/We're all under the stars.ogg"

    if main.party_info['reg'] != region:
        print('-'*25)
        print(ascii_art.locations[region])
        print('You have left the {0} and are now entering the {1}.'.format(
            main.party_info['reg'], region))

        if not towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False):
            print('-'*25)

        main.party_info['reg'] = region
        main.party_info['reg_music'] = reg_music
        main.party_info['prev_town'][0] = main.party_info['x']
        main.party_info['prev_town'][1] = main.party_info['y']

        # Change the music & play it
        pygame.mixer.music.load(reg_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        return True

    else:
        return False


def rest():
    # Attempt to re-gain health on the world map. There is a chance to get ambushed by an enemy
    # when doing this.
    print('-'*25)

    if all([units.player.hp == units.player.max_hp and units.player.mp == units.player.max_mp,
            units.solou.hp == units.solou.max_hp and units.solou.mp == units.solou.max_mp,
            units.xoann.hp == units.xoann.max_hp and units.xoann.mp == units.xoann.max_mp,
            units.chyme.hp == units.chyme.max_hp and units.chyme.mp == units.chyme.max_mp,
            units.ran_af.hp == units.ran_af.max_hp and units.ran_af.mp == units.ran_af.max_mp,
            units.parsto.hp == units.parsto.max_hp and units.parsto.mp == units.parsto.max_mp,
            units.adorine.hp == units.adorine.max_hp and units.adorine.mp == units.adorine.max_mp]):

        print('Your party feels fine and decides not to rest.')
        if not towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False):
            print('-'*25)

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
        if not towns.search_towns(main.party_info['x'], main.party_info['y'], enter=False):
            print('-'*25)
