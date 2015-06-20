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
import msvcrt
import pygame

import battle
import monsters
import towns
import bosses
import sounds
import inv_system
import magic
import pets

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

position = ''


def setup_vars():
    global position
    global misc_vars
    global player

    position = main.position
    misc_vars = main.misc_vars
    player = main.player


def movement_system():
    # Adjust the player's x/y coordinates based on inputted direction.
    global position

    setup_vars()

    pygame.mixer.music.load(position['reg_music'])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(main.music_vol)

    while True:
        towns.search_towns(position['x'], position['y'])

        if position['x'] >= 0:
            position['h'] = "\u00b0E"
        else:
            position['h'] = "\u00b0W"

        if position['y'] >= 0:
            position['v'] = "\u00b0N"
        else:
            position['v'] = "\u00b0S"

        while True:
            direction = input('{0}{1}, {2}{3} | {4} | Input Dir. (N, S, E, W), \
[P]layer, [T]ools, [R]est: '.format(position['y'], position['v'],
                                    position['x'], position['h'],
                                    position['reg']))

            direction = direction.lower()

            if any(map(direction.startswith, ['n', 's', 'w', 'e'])):

                sounds.foot_steps.play()
                # The in-game map is square due to simplify things.
                # Map of the Arcadian Continent: http://tinyurl.com/arcadia-map-v5
                if direction.startswith('n'):

                    if position['y'] < 125 if not position['is_aethus'] else 50:
                        position['y'] += 1

                    else:
                        print('-'*25)

                        if position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if position['x'] <= 42:
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
                    if position['y'] > -125 if not position['is_aethus'] else -50:
                        position['y'] -= 1

                    else:
                        print('-'*25)

                        if position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if position['x'] <= 42:
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
                    if position['x'] > -125 if not position['is_aethus'] else -50:
                        position['x'] -= 1

                    else:
                        print('-'*25)

                        if position['is_aethus']:  # Aethus is a floating island in the sky
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
                    if position['x'] < 125 if not position['is_aethus'] else 50:
                        position['x'] += 1

                    else:
                        print('-'*25)

                        if position['is_aethus']:  # Aethus is a floating island in the sky
                            print("""\
Continuing to walk in that direction would cause you to fall to your death.
It's probably in your best interests that you not do that.
-------------------------""")

                            continue

                        if position['y'] >= 42:
                            nation = 'Hillsbrad'

                        elif position['y'] <= -42:
                            nation = 'Maranon'

                        else:
                            nation = 'Elysium'

                        print('You come across the border between {0} and Pythonia.'.format(
                            nation))
                        print('Despite your pleading, the border guards will not let you pass.')
                        print('-'*25)

                        continue

                position['avg'] = int(((abs(position['x'])) +
                                       (abs(position['y'])))/2)

                if not any([check_region(),
                           bosses.check_bosses(position['x'], position['y']),
                           towns.search_towns(position['x'], position['y'], enter=False)]
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
                    decision = input(
                        'View [i]nventory, [s]tats, or [m]agic? | Input Letter (or type "exit"): ')

                    decision = decision.lower()

                    if decision.startswith('i'):
                        print('-'*25)
                        inv_system.pick_category()
                        print('-'*25)

                    elif decision.startswith('s'):
                        print('-'*25)
                        main.player.player_info()
                        print('-'*25)

                    elif decision.startswith('m'):
                        if magic.spellbook['Healing']:
                            magic.pick_spell('Healing', 0, 0, False)
                        else:
                            print('-'*25)
                            print('You have no overworld-allowed spells available.')

                    elif decision in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
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
    global position
    x, y = position['x'], position['y']
    if position['is_aethus']:
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

    if position['reg'] != region:
        print('-'*25)
        print('You have left the {0} and are now entering the {1}.'.format(
            position['reg'], region))

        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)

        position['reg'] = region
        position['reg_music'] = reg_music
        save_coords(position['x'], position['y'])

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
    global position
    position['prev_town'][0], position['prev_town'][1] = x, y


def back_to_coords():
    global position
    position['x'] = position['prev_town'][0]
    position['y'] = position['prev_town'][1]


def rest():
    # Attempt to re-gain health on the world map. There is a chance to get ambushed by an enemy
    # when doing this.

    setup_vars()
    print('-'*25)

    if player.hp == misc_vars['hp_p'] and player.mp == misc_vars['mp_p']:
        print('You feel fine, and decide not to rest.')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)
        return

    print('You set up camp and begin to rest.')

    time.sleep(1)

    while msvcrt.kbhit():
        msvcrt.getwch()

    player.hp += int(misc_vars['hp_p']/4)
    player.mp += int(misc_vars['mp_p']/4)

    # Make sure that the player doesn't have more than the max HP/MP
    if player.hp > misc_vars['hp_p']:
        player.hp -= (player.hp - misc_vars['hp_p'])
    if player.mp > misc_vars['mp_p']:
        player.mp -= (player.mp - misc_vars['mp_p'])

    is_battle = not random.randint(0, 3)

    if is_battle:
        monsters.spawn_monster()
        battle.setup_vars()
        battle.battle_system(ambush=True)

    else:
        print('You rested well and decide to continue on your way.')
        if not towns.search_towns(main.position['x'], main.position['y'], enter=False):
            print('-'*25)
