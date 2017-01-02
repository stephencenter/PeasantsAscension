#   This file is part of PythoniusRPG.
#
#	 PythoniusRPG is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PythoniusRPG is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PythoniusRPG.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------ #
# Map of the Arcadian Continent: http://tinyurl.com/arcadia-map-v5

import sys
import random
import time
import math
import pygame

import battle
import monsters
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


def movement_system():
    # Adjust the player's x/y coordinates based on inputted direction.

    pygame.mixer.music.load(main.position['reg_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(main.music_vol)

    while True:
        towns.search_towns(main.position['x'], main.position['y'])

        if main.position['x'] >= 0:
            main.position['h'] = "\u00b0E"
        else:
            main.position['h'] = "\u00b0W"

        if main.position['y'] >= 0:
            main.position['v'] = "\u00b0N"
        else:
            main.position['v'] = "\u00b0S"

        while True:
            direction = input('{0}{1}, {2}{3} | {4} | Input Dir. (N, S, E, W), \
[P]layer, [T]ools, [R]est: '.format(main.position['y'], main.position['v'],
                                    main.position['x'], main.position['h'],
                                    main.position['reg']))

            direction = direction.lower()

            if any(map(direction.startswith, ['n', 's', 'w', 'e'])):

                sounds.foot_steps.play()
                # The in-game map is square due to simplify things.
                # Map of the Arcadian Continent: http://tinyurl.com/arcadia-map-v5
                if direction.startswith('n'):

                    if main.position['y'] < 125 if not main.position['is_aethus'] else 50:
                        main.position['y'] += 1

                    else:
                        print('-'*25)

                        if main.position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if main.position['x'] <= 42:
                            print('Off in the distance, you see what appears to be a large')
                            print('island. According to your map, this island is known as')
                            print('Durcuba. You probably shouldn\'t go there.')

                        else:
                            print('You come across the border between Hillsbrad and Pythonia.')
                            print('Despite your pleading, the border guards will not let you \
pass.')

                        print('-'*25)

                        continue

                elif direction.startswith('s'):
                    if main.position['y'] > -125 if not main.position['is_aethus'] else -50:
                        main.position['y'] -= 1

                    else:
                        print('-'*25)

                        if main.position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if main.position['x'] <= 42:
                            print('You see a large island off in the distance. According to')
                            print('your map, this island appears to be Thex! Unfortunately,')
                            print("you don't have any way to cross the sea.")

                        else:
                            print('You come across the border between Maranon and Pythonia.')
                            print('Despite your pleading, the border guards will not let you \
pass.')
                        print('-'*25)

                        continue

                elif direction.startswith('w'):
                    if main.position['x'] > -125 if not main.position['is_aethus'] else -50:
                        main.position['x'] -= 1

                    else:
                        print('-'*25)

                        if main.position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        print('Ahead of you is a seemingly endless ocean. \
You cannot continue in this direction.')
                        print('-'*25)

                        continue

                elif direction.startswith('e'):
                    if main.position['x'] < 125 if not main.position['is_aethus'] else 50:
                        main.position['x'] += 1

                    else:
                        print('-'*25)

                        if main.position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if main.position['y'] >= 42:
                            nation = 'Hillsbrad'

                        elif main.position['y'] <= -42:
                            nation = 'Maranon'

                        else:
                            nation = 'Elysium'

                        print('You come across the border between {0} and Pythonia.'.format(
                            nation))
                        print('Despite your pleading, the border guards will not let you pass.')
                        print('-'*25)

                        continue

                main.position['avg'] = int(((abs(main.position['x'])) + (abs(main.position['y'])))/2)

                if not any([check_region(),
                           bosses.check_bosses(main.position['x'], main.position['y']),
                           towns.search_towns(main.position['x'], main.position['y'], enter=False)]
                           ):

                    # If none of the previous statements return True, then a battle can occur.
                    # There is a 1 in 7 chance for a battle to occur (14.285714...%)
                    is_battle = not random.randint(0, 6)

                    if is_battle:
                        print('-'*25)
                        monsters.spawn_monster()
                        battle.setup_vars()
                        battle.battle_system()

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
                            main.player,
                            main.solou,
                            main.xoann,
                            main.adorine,
                            main.ran_af,
                            main.parsto,
                            main.randall] if x.enabled
                        ]

                        if len(target_options) == 1:
                            target = main.player

                        else:
                            print("Select Character:")
                            print("     ", "\n      ".join(
                                ["[{0}] {1}".format(int(num) + 1, character.name)
                                 for num, character in enumerate(target_options)]))

                            while True:
                                target = input('Input [#] (or type "exit"): ')

                                if target.lower() in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                                    print('-'*25)

                                    break

                                try:
                                    target = int(target) - 1
                                except ValueError:
                                    continue

                                try:
                                    target = target_options[target]
                                except IndexError:
                                    continue

                                break

                        if isinstance(target, main.PlayableCharacter):
                            print('-'*25)
                            target.player_info()
                            print('-'*25)

                    if decision.startswith('m'):
                        user_options = [x for x in [
                            main.player,
                            main.solou,
                            main.xoann,
                            main.adorine,
                            main.ran_af,
                            main.parsto,
                            main.randall] if x.enabled
                        ]

                        if len(user_options) == 1:
                            user = main.player

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

                        if magic.spellbook[
                            user.name if user != main.player else 'player'
                        ]['Healing']:

                            magic.pick_spell('Healing', user, False)

                        else:
                            print('-'*25)
                            print('You have no overworld-allowed spells available.')

                    if decision in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                        print('-'*25)
                        break

            elif direction.startswith('t'):
                inv_system.tools_menu()
                if towns.search_towns(main.position['x'], main.position['y'], enter=False):
                    print('-'*25)

            elif direction.startswith('r'):
                rest()
                if towns.search_towns(main.position['x'], main.position['y'], enter=False):
                    print('-'*25)


def check_region():
    # Check the coordinates of the player and change the region to match.
    x, y = main.position['x'], main.position['y']

    if main.position['is_aethus']:
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
            region = 'Pythonian Coastline'
            reg_music = "Music/We're all under the stars.ogg"

    if main.position['reg'] != region:
        print('-'*25)
        print(ascii_art.locations[region])
        print('You have left the {0} and are now entering the {1}.'.format(
            main.position['reg'], region))

        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)

        main.position['reg'] = region
        main.position['reg_music'] = reg_music
        save_coords(main.position['x'], main.position['y'])

        # Change the music & play it
        pygame.mixer.music.load(reg_music)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        return True

    else:
        return False


def save_coords(x, y):
    # Mark the player's coordinates when they change regions or visit towns.
    # The player will return to these coordinates if they die.
    main.position['prev_town'][0], main.position['prev_town'][1] = x, y


def back_to_coords():
    main.position['x'] = main.position['prev_town'][0]
    main.position['y'] = main.position['prev_town'][1]


def rest():
    # Attempt to re-gain health on the world map. There is a chance to get ambushed by an enemy
    # when doing this.
    print('-'*25)

    if all([
        main.player.hp == main.player.max_hp and main.player.mp == main.player.max_mp,
        main.solou.hp == main.solou.max_hp and main.solou.mp == main.solou.max_mp,
        main.xoann.hp == main.xoann.max_hp and main.xoann.mp == main.xoann.max_mp,
        main.randall.hp == main.randall.max_hp and main.randall.mp == main.randall.max_mp,
        main.ran_af.hp == main.ran_af.max_hp and main.ran_af.mp == main.ran_af.max_mp,
        main.parsto.hp == main.parsto.max_hp and main.parsto.mp == main.parsto.max_mp,
        main.adorine.hp == main.adorine.max_hp and main.adorine.mp == main.adorine.max_mp
    ]):

        print('Your party feels fine and decides not to rest.')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)

        return

    print(ascii_art.locations['Campsite'])
    print('Your party sets up camp and begin to rest.')

    main.smart_sleep(1)

    main.player.hp += math.ceil(main.player.max_hp/3)
    main.player.mp += math.ceil(main.player.max_mp/3)
    main.solou.hp += math.ceil(main.solou.max_hp/3)
    main.solou.mp += math.ceil(main.solou.max_mp/3)
    main.xoann.hp += math.ceil(main.xoann.max_hp/3)
    main.xoann.mp += math.ceil(main.xoann.max_mp/3)
    main.randall.hp += math.ceil(main.randall.max_hp/3)
    main.randall.mp += math.ceil(main.randall.max_mp/3)
    main.ran_af.hp += math.ceil(main.ran_af.max_hp/3)
    main.ran_af.mp += math.ceil(main.ran_af.max_mp/3)
    main.parsto.hp += math.ceil(main.parsto.max_hp/3)
    main.parsto.mp += math.ceil(main.parsto.max_mp/3)
    main.adorine.hp += math.ceil(main.adorine.max_hp/3)
    main.adorine.mp += math.ceil(main.adorine.max_mp/3)

    # Make sure that the player doesn't have more than the max HP/MP
    if main.player.hp > main.player.max_hp:
        main.player.hp -= (main.player.hp - main.player.max_hp)
    if main.player.mp > main.player.max_mp:
        main.player.mp -= (main.player.mp - main.player.max_mp)

    if main.solou.hp > main.solou.max_hp:
        main.solou.hp -= (main.solou.hp - main.solou.max_hp)
    if main.solou.mp > main.solou.max_mp:
        main.solou.mp -= (main.solou.mp - main.solou.max_mp)

    if main.xoann.hp > main.xoann.max_hp:
        main.xoann.hp -= (main.xoann.hp - main.xoann.max_hp)
    if main.xoann.mp > main.xoann.max_mp:
        main.xoann.mp -= (main.xoann.mp - main.xoann.max_mp)

    if main.randall.hp > main.randall.max_hp:
        main.randall.hp -= (main.randall.hp - main.randall.max_hp)
    if main.randall.mp > main.randall.max_mp:
        main.randall.mp -= (main.randall.mp - main.randall.max_mp)

    if main.ran_af.hp > main.ran_af.max_hp:
        main.ran_af.hp -= (main.ran_af.hp - main.ran_af.max_hp)
    if main.ran_af.mp > main.ran_af.max_mp:
        main.ran_af.mp -= (main.ran_af.mp - main.ran_af.max_mp)

    if main.parsto.hp > main.parsto.max_hp:
        main.parsto.hp -= (main.parsto.hp - main.parsto.max_hp)
    if main.parsto.mp > main.parsto.max_mp:
        main.parsto.mp -= (main.parsto.mp - main.parsto.max_mp)

    if main.adorine.hp > main.adorine.max_hp:
        main.adorine.hp -= (main.adorine.hp - main.adorine.max_hp)
    if main.adorine.mp > main.adorine.max_mp:
        main.adorine.mp -= (main.adorine.mp - main.adorine.max_mp)

    # Revive any dead characters
    if main.player.status_ail == 'dead':
        main.player.status_ail = 'none'

    if main.solou.hp == 'dead':
        main.solou.status_ail = 'none'

    if main.xoann.hp == 'dead':
        main.xoann.status_ail = 'none'

    if main.randall.hp == 'dead':
        main.randall.status_ail = 'none'

    if main.ran_af.hp == 'dead':
        main.ran_af.status_ail = 'none'

    if main.parsto.hp == 'dead':
        main.parsto.status_ail = 'none'

    if main.adorine.hp == 'dead':
        main.adorine.status_ail = 'none'

    is_battle = not random.randint(0, 3)

    if is_battle:
        monsters.spawn_monster()
        battle.setup_vars()
        battle.battle_system(ambush=True)

    else:
        print('You rested well and decide to continue on your way.')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)
