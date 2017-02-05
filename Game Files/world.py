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
                 to_dn=None, town_list=(), boss_list=(), gem_list=(), enterable=True, level_req=1):

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
        self.enterable = enterable
        self.town_list = town_list
        self.boss_list = boss_list
        self.gem_list = gem_list
        self.level_req = level_req

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
there might be a smart idea.""", 2, town_list=[towns.town_nearton],
                    to_s="I-CF-E",
                    to_w="I-CF-N")

southford_tile = Tile("Town of Southford", "Southford", "Central Forest", icf_desc + """\n
The town of Nearton is mere minutes away from this point! Stopping by
there might be a smart idea.""", 2, town_list=[towns.town_southford],
                      to_e="I-CF-S",
                      to_n="I-CF-W")

icf_bridge = Tile("Inner Forest Bridge", "I-CF-Bridge", "Central Forest", icf_desc + """\n
This bridge extends over the 12ft-wide moat surrounding the Inner Central Forest, meant
to help protect its citizens from the harmful monsters outside it. Weaker monsters still
manage to make their way in though.""", 0,
                     to_s="I-CF-N",
                     to_n="WH-CF-ICF Bridge Exit")

# -- CENTRAL FOREST TILESETS -- #

# Inner Central Forest
icf_tiles = [nearton_tile, southford_tile, in_for_c, in_for_w, in_for_e, in_for_s, in_for_n, in_for_se, in_for_nw,
             icf_bridge]

# West of the Hythos River
whr_tiles = []

# West of the Hythos River
ehr_tiles = []


all_tiles = icf_tiles + whr_tiles + ehr_tiles  # + other tiles lists as more tiles come into existance


def movement_system():
    pygame.mixer.music.load(main.party_info['reg_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(main.music_vol)

    while True:
        towns.search_towns()

        print(f"-CURRENT LOCATION-")

        mpi = main.party_info
        tile = mpi['current_tile']

        no_adj_tiles = len([t for t in [tile.to_up,
                                        tile.to_dn,
                                        tile.to_w,
                                        tile.to_s,
                                        tile.to_n,
                                        tile.to_e] if t is not None])

        # Calculate which tile ascii art to display
        if no_adj_tiles == 1:
            if tile.to_n:
                print("""
    | N |
    |   |
    | X |
    |___| X = Player Party\n""")
            elif tile.to_s:
                print("""
     ___
    |   |
    | X |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_w:
                print("""
________
W     X |
________| X = Player Party\n""")
            elif tile.to_e:
                print("""
     ________
    | X     E
    |________ X = Player Party\n""")
            elif tile.to_dn or tile.to_up:
                print("""
     ___
    | X |
    |___| X = Player Party\n""")

        elif no_adj_tiles == 2:
            if tile.to_n and tile.to_w:
                print("""
    | N |
____|   |
W     X |
________| X = Player Party\n""")
            elif tile.to_n and tile.to_e:
                print("""
    | N |
    |   |____
    | X    E
    |________ X = Player Party\n""")
            elif tile.to_n and tile.to_s:
                print("""
    | N |
    |   |
    | X |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_w and tile.to_e:
                print("""
_____________
W     X     E
_____________ X = Player Party\n""")
            elif tile.to_w and tile.to_s:
                print("""
________
W     X |
____    |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_e and tile.to_s:
                print("""
     ________
    | X     E
    |    ____
    |   |
    | S | X = Player Party\n""")
            elif tile.to_up and tile.to_dn:
                print("""
     ___
    | X |
    |___| X = Player Party\n""")
            elif tile.to_n and (tile.to_up or tile.to_dn):
                print("""
    | N |
    |   |
    | X |
    |___| X = Player Party\n""")
            elif tile.to_s and (tile.to_up or tile.to_dn):
                print("""
     ___
    |   |
    | X |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_e and (tile.to_up or tile.to_dn):
                print("""
     ________
    | X     E
    |________ X = Player Party\n""")
            elif tile.to_w and (tile.to_up or tile.to_dn):
                print("""
________
W     X |
________| X = Player Party\n""")

        elif no_adj_tiles == 3:
            if tile.to_n and tile.to_w and tile.to_e:
                print("""
    | N |
____|   |____
W     X     E
_____________ X = Player Party\n""")
            elif tile.to_n and tile.to_w and tile.to_s:
                print("""
    | N |
____|   |
W     X |
____    |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_n and tile.to_e and tile.to_s:
                print("""
    | N |
    |   |____
    | X     E
    |    ____
    |   |
    | S | X = Player Party\n""")
            elif tile.to_w and tile.to_e and tile.to_s:
                print("""
_____________
W     X     E
____     ____
    |   |
    | S | X = Player Party\n""")

            elif tile.to_w and tile.to_n and (tile.to_up or tile.to_dn):
                print("""
    | N |
____|   |
W     X |
________| X = Player Party\n""")
            elif tile.to_w and tile.to_s and (tile.to_up or tile.to_dn):
                print("""
________
W     X |
____    |
    |   |
    | S | X = Player Party\n""")
            elif tile.to_w and tile.to_e and (tile.to_up or tile.to_dn):
                print("""
_____________
W     X     E
_____________ X = Player Party\n""")
            elif tile.to_n and tile.to_e and (tile.to_up or tile.to_dn):
                print("""
    | N |
    |   |____
    | X    E
    |________ X = Player Party\n""")
            elif tile.to_s and tile.to_e and (tile.to_up or tile.to_dn):
                print("""
     ________
    | X     E
    |    ____
    |   |
    | S | X = Player Party\n""")
            elif tile.to_n and tile.to_s and (tile.to_up or tile.to_dn):
                print("""
    | N |
    |   |
    | X |
    |   |
    | S | X = Player Party\n""")

        elif no_adj_tiles >= 4:
            if tile.to_n and tile.to_w and tile.to_e and tile.to_s:
                print("""
    | N |
____|   |____
W     X     E
____     ____
    |   |
    | S | X = Player Party\n""")

        # Calculate the character's X, Y, and Z coordinates and create a string from them. The Z coordinate does not
        # change nearly as often as the other two, so don't display it unless it != 0.
        coord_x = f"{mpi['x']}'{'W' if mpi['x'] < 0 else 'E'}{', ' if mpi['z'] != 0 else ''}"
        coord_y = f"{mpi['y']}'{'S' if mpi['y'] < 0 else 'N'}, "
        coord_z = f"""{mpi["z"] if mpi["z"] != 0 else ""}{"'UP" if mpi["z"] > 0 else "'DOWN" if mpi['z'] < 0 else ""}"""
        coordinates = ''.join([coord_y, coord_x, coord_z])

        print(f"Coordinates: {coordinates} | Region: [{tile.region}] | Subregion [{tile.name}]")

        # These lists will tell the game how to manipulate the players position in the next part of the function
        available_dirs = []
        coord_change = []

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

                if not any([check_region(), bosses.check_bosses(), towns.search_towns(enter=False)]):
                    # If none of the previous statements return True, then a battle can occur.
                    # There is a 1 in 7 chance for a battle to occur (14.285714...%)
                    is_battle = not random.randint(0, 6)

                    if is_battle and main.party_info['current_tile'].m_level != 0:
                        print('-'*25)
                        units.spawn_monster()
                        units.player.hp = 1
                        battle.battle_system()

                    else:
                        print()

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


def check_region():
    # Check the coordinates of the player and change the region to match.
    new_region = main.party_info['current_tile'].region

    if main.party_info['reg'] != new_region:
        print('-'*25)
        print(ascii_art.locations[new_region])
        print(f"You have left the {main.party_info['reg']} and are now entering the {new_region}.")

        main.party_info['reg'] = new_region
        main.party_info['reg_music'] = reg_music

        # Change the music & play it
        pygame.mixer.music.load(reg_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        if not towns.search_towns(enter=False):
            print('-'*25)

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
        if not towns.search_towns(enter=False):
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
        if not towns.search_towns(enter=False):
            print('-'*25)
