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

import sys
import random
import time
import math
import msvcrt
import re
from copy import copy as _c

import pygame

import inv_system
import monsters
import world
import bosses
import sounds
import ascii_art
import items

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

player = ''
solou = ''
xoann = ''

monster = ''
temp_stats = ''

vowels = 'AEIOU'
monk_tc = 0
turn_counter = 0

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


def setup_vars():
    global player
    global solou
    global xoann
    global monster

    monster = monsters.monster
    player = main.player
    solou = main.solou
    xoann = main.xoann


def update_stats():
    # Forces stats to return to normal when battle is finished
    global temp_stats
    temp_stats = {
        player.name: {
            'attk': _c(player.attk),
            'dfns': _c(player.dfns),
            'p_attk': _c(player.p_attk),
            'p_dfns': _c(player.p_dfns),
            'm_attk': _c(player.m_attk),
            'm_dfns': _c(player.m_dfns),
            'spd': _c(player.spd),
            'evad': _c(player.evad),
            'ability_used': False
        },
        'Solou': {
            'attk': _c(solou.attk),
            'dfns': _c(solou.dfns),
            'p_attk': _c(solou.p_attk),
            'p_dfns': _c(solou.p_dfns),
            'm_attk': _c(solou.m_attk),
            'm_dfns': _c(solou.m_dfns),
            'spd': _c(solou.spd),
            'evad': _c(solou.evad),
            'ability_used': False
        },
        'Xoann': {
            'attk': _c(xoann.attk),
            'dfns': _c(xoann.dfns),
            'p_attk': _c(xoann.p_attk),
            'p_dfns': _c(xoann.p_dfns),
            'm_attk': _c(xoann.m_attk),
            'm_dfns': _c(xoann.m_dfns),
            'spd': _c(xoann.spd),
            'evad': _c(xoann.evad),
            'ability_used': False
        }
    }


def battle_system(is_boss=False, ambush=False):
    global ability_used
    global monk_tc

    if is_boss:  # Bosses have different battle music than normal enemies
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[monster.monster_name] % '')
        print('The legendary {0} has awoken!'.format(monster.name))
        time.sleep(0.35)

        while msvcrt.kbhit():
            msvcrt.getwch()

    else:
        print(ascii_art.monster_art[monster.monster_name] % '')

        if any(map(monster.name.startswith, vowels)):  # Remember to use proper grammar!
            a_an = 'An '
        else:
            a_an = 'A '

        if ambush:
            print('{0}{1} ambushed you while you were resting!'.format(
                a_an, monster.name))
            pygame.mixer.music.load('Music/Ruari 8-bit Battle.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            time.sleep(1)

            while msvcrt.kbhit():
                msvcrt.getwch()

        else:
            print('{0}{1} suddenly appeared out of nowhere!'.format(
                a_an, monster.name))
            pygame.mixer.music.load('Music/Ruari 8-bit Battle.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            time.sleep(1)

            while msvcrt.kbhit():
                msvcrt.getwch()

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    update_stats()

    ability_used = False

    # Continue the battle until one of a few conditions are met
    while not ((player.hp <= 0 or solou.hp <= 0 or xoann.hp <= 0) or
               (not is_boss and monster.hp <= 0) or
               (is_boss and (not monster.multiphase or monster.currphase == monster.multiphase)
                and monster.hp <= 0)):

        for character in [x for x in [solou, xoann, player] if x.enabled]:
            if 0 < character.hp <= 0.20*character.max_hp:
                print("Warning: {0}'s HP is low, heal as soon as possible!".format(character.name))
                sounds.health_low.play()

        for character in [x for x in [solou, xoann, player] if x.enabled]:
            if character.hp <= 0:
                character.status_ail = 'dead'

        bat_stats()

        # Increment the monk turn-counter for lower defense until it equals 3
        if player.class_ == 'monk' and ability_used:
            if monk_tc == 3:
                print('You recover from the usage of your class ability, and your')
                print('defenses return to normal.')

            monk_tc += 1

        # There is a 1/3 chance for the player to wake up each turn if they are asleep
        for character in [x for x in [player, solou, xoann]
                          if x.enabled and x.status_ail != 'dead']:
            if character.status_ail == 'asleep':
                # If dodge is in a certain range, the attack will miss
                character.dodge = random.randint(0, 512)
                monster.dodge = random.randint(0, 512)

                if not random.randint(0, 2):
                    sounds.buff_spell.play()
                    print('\n-Player Turn-')
                    input('You start to regain consciousness! | Press enter/return ')

                    character.status_ail = 'none'
                    bat_stats()
                    character.player_choice()

                else:
                    print('-Player Turn-')
                    print(ascii_art.player_art["Asleep"] % "{0} is asleep!\n ".format(
                        character.name))
                    input("You're too tired to do anything! | Press Enter/Return ")
                    character.move = ''

            else:
                # If dodge is in a certain range, the attack will miss
                character.dodge = random.randint(0, 512)
                monster.dodge = random.randint(0, 512)

                character.player_choice()

        for unit in sorted([monster] + [c for c in [player, solou, xoann] if c.enabled],
                           key=lambda x: x.spd):
            if isinstance(unit, main.PlayableCharacter) and unit.status_ail == 'dead':
                continue

            if unit.battle_turn(is_boss) == 'Ran':
                return

            if (monster.hp > 0) and any([player.hp > 0, solou.hp > 0, xoann.hp > 0]):
                input('\nPress enter/return ')

            else:
                break

    else:
        if after_battle(is_boss) != 'dead':
            print('-'*25)


def after_battle(is_boss):  # Assess the results of the battle
    global player

    update_stats()  # Reset non-hp/mp stats to the way they were before battle

    print('-'*25)

    while True:
        # If the monster wins...
        if monster.hp > 0 >= player.hp and 0 >= solou.hp and 0 >= xoann.hp:
            pygame.mixer.music.load('Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            print('Despite your best efforts, the {0} has bested your party. You are dead.'.format(
                monster.name))
            print('-'*25)

            spam = True
            while True:
                if spam:
                    y_n = input('Do you wish to continue playing? | Yes or No: ')
                    y_n = y_n.lower()

                else:
                    y_n = 'y'

                if y_n.startswith('y'):
                    # If you die, you return to the last town visited or 0'N, 0'E
                    # if you haven't been to a town yet.
                    world.back_to_coords()

                    player.hp = _c(player.max_hp)
                    player.mp = _c(player.max_mp)

                    player.status_ail = "none"

                    pygame.mixer.music.load(main.position['reg_music'])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(main.music_vol)

                    return 'dead'

                elif y_n.startswith('n'):
                    print('Are you sure you want to quit? You will lose all unsaved progress.')

                    while True:
                        y_n = input("Quit? | Yes or No: ")

                        y_n = y_n.lower()

                        if y_n.startswith('y'):
                            pygame.quit()
                            sys.exit()

                        elif y_n.startswith('n'):
                            spam = False
                            break

        # If the player wins...
        elif monster.hp <= 0 < player.hp:
            pygame.mixer.music.load('Music/Python_RM.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            if not is_boss:
                # Only do the following if the player defeated a normal enemy, and not a boss
                print('The {0} falls to the ground, dead as a stone.'.format(monster.name))

                # Enemies drop gold/exp based on the player/monster's levels
                gold = math.ceil(random.randint(2, 3)*monster.lvl - player.lvl) + player.ext_gol

                if gold <= 0:
                    gold = random.randint(1, 2)

                experience = math.ceil((monster.lvl**1.5 + player.ext_exp)/1.5)

                if experience <= 0:
                    experience = random.randint(1, 2)

            else:
                # Only do the following if the player defeated a boss
                bosses.defeated_bosses.append(monster.name)
                print('The almighty {0} has been slain!'.format(monster.name))

                # Bosses drop a set amount of gold...
                gold = monster.gold + player.ext_gol

                # ...and exp
                experience = monster.experience

                # Check to see if the boss does anything special at death
                monster.upon_defeating()

            # If the monster has items, give them to the player
            if monster.items:
                cat = monster.items.cat
                inv_system.inventory[cat].append(_c(monster.items))

                print('The {0} dropped a {1}! Your party decides to take {2}.'.format(
                      monster.name, str(monster.items),
                      'them' if str(monster.items).endswith('s') else 'it'), end='')  # Grammar!!

                sounds.item_pickup.play()
                input(' | Press Enter/Return ')

            # Give the Player their GP
            main.misc_vars['gp'] += gold + player.ext_gol
            print("Your party has gained {0} GP!".format(gold), end='')
            sounds.item_pickup.play()
            input(' | Press Enter/Return ')

            for character in [x for x in [solou, xoann, player] if x.enabled]:
                # Give the Player their XP
                character.exp += experience
                print("{0} gained {1} XP!".format(character.name, experience), end='')
                sounds.item_pickup.play()
                input(' | Press Enter/Return ')

                # Check to see if the player gained any levels
                character.level_up()

            pygame.mixer.music.load(main.position['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            pygame.mixer.music.set_volume(main.music_vol)

            return


def run_away(runner):
    print(ascii_art.player_art[runner.class_.title()] %
          "{0} is making a move!\n".format(runner.name))
    print()
    print('Your party starts to run away from the {0}...'.format(monster.name))

    sounds.foot_steps.play()
    time.sleep(0.75)

    while msvcrt.kbhit():
        msvcrt.getwch()

    if player.status_ail == 'paralyzed':
        # 25% chance of success
        chance = 25

    elif bool(player.spd > monster.spd) != bool(player.evad > monster.evad):
        # 75% chance of success
        chance = 75

    elif player.spd > monster.spd and player.evad > monster.evad:
        # 90% chance of success
        chance = 90

    else:
        # 50% chance of success
        chance = 50

    if random.randint(0, 100) <= chance:
        print('You manage to escape from the {0}!'.format(monster.name))
        return True

    else:
        print('Your attempt to escape failed!')
        input("\nPress Enter/Return")
        return False


def battle_inventory():
    # The player can use items from the "consum" category of their inventory during battles.
    if not inv_system.inventory['consum']:
        print('You have no battle-allowed items! The Consumable category is empty.')
        return False

    while True:
        print('Battle Inventory: \n      ', end='')
        print('\n      '.join(['[{0}] {1} {2}'.format(x + 1, y, '| Item Power: ' + str(
            max(y.heal, y.mana)) if isinstance(y, items.Consumable) else '')

            for x, y in enumerate(inv_system.inventory['consum'])]))

        while True:
            item = input('Input [#] (or type "cancel"): ')
            try:
                item = int(item) - 1
                if item < 0:
                    continue

            except ValueError:
                item = item.lower()

                if item in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return False

                else:
                    continue
            try:
                item = inv_system.inventory['consum'][item]
            except IndexError:
                continue

            print('\n-Player Turn-')

            if isinstance(item, inv_system.i.StatusPotion):
                if item.status != player.status_ail:
                    print('You are not {0} - you have no reason to drink that.'.format(item.status))
                    print()
                    break

            item.use_item(is_battle=True)
            return True


def bat_stats():
    # Makes sure that that no-one ever has negative stats,
    # and then display their stats after they're fixed
    global player
    global solou
    global xoann
    global monster

    if player.hp < 0:
        player.hp = 0
    if solou.hp < 0:
        solou.hp = 0
    if xoann.hp < 0:
        xoann.hp = 0
    if monster.hp < 0:
        monster.hp = 0

    if player.hp > player.max_hp:
        player.hp -= (player.hp - player.max_hp)
    if solou.hp > solou.max_hp:
        solou.hp -= (solou.hp - solou.max_hp)
    if xoann.hp > xoann.max_hp:
        xoann.hp -= (xoann.hp - xoann.max_hp)
    if monster.hp > monster.max_hp:
        monster.hp -= (monster.hp - monster.max_hp)

    if player.mp < 0:
        player.mp = 0
    if solou.mp < 0:
        solou.mp = 0
    if xoann.mp < 0:
        xoann.mp = 0
    if monster.mp < 0:
        monster.mp = 0

    if player.mp > player.max_mp:
        player.mp -= (player.mp - player.max_mp)
    if solou.hp > solou.max_hp:
        solou.hp -= (solou.mp - solou.max_mp)
    if xoann.hp > xoann.max_hp:
        xoann.hp -= (xoann.mp - xoann.max_mp)
    if monster.mp > monster.max_mp:
        monster.mp -= (monster.mp - monster.max_mp)

    print('-'*25)

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    first_padding = len(max([player.name, solou.name, xoann.name, monster.name], key=len))

    second_padding = len(max(['{0}/{1} HP'.format(player.hp, player.max_hp),
                              '{0}/{1} HP'.format(solou.hp, solou.max_hp),
                              '{0}/{1} HP'.format(xoann.hp, xoann.max_hp),
                              '{0}/{1} HP'.format(monster.hp, monster.max_hp)], key=len))

    third_padding = len(max(['{0}/{1} MP'.format(player.mp, player.max_mp),
                             '{0}/{1} MP'.format(solou.mp, solou.max_mp),
                             '{0}/{1} MP'.format(xoann.mp, xoann.max_mp),
                             '{0}/{1} MP'.format(monster.mp, monster.max_mp)], key=len))

    # Player Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          player.name, player.hp,
          player.max_hp, player.mp,
          player.max_mp, player.lvl,
          player.status_ail.title(),
          pad1=' '*(first_padding - len(player.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(player.hp, player.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(player.mp, player.max_mp)))))

    if solou.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              solou.name, solou.hp,
              solou.max_hp, solou.mp,
              solou.max_mp, solou.lvl,
              solou.status_ail.title(),
              pad1=' '*(first_padding - len(solou.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(solou.hp, solou.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(solou.mp, solou.max_mp)))))

    if xoann.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              xoann.name, xoann.hp,
              xoann.max_hp, xoann.mp,
              xoann.max_mp, xoann.lvl,
              xoann.status_ail.title(),
              pad1=' '*(first_padding - len(xoann.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(xoann.hp, xoann.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(xoann.mp, xoann.max_mp)))))

    # Monster Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5}".format(
          monster.name, monster.hp,
          monster.max_hp, monster.mp,
          monster.max_mp, monster.lvl,
          pad1=' '*(first_padding - len(monster.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(monster.hp, monster.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(monster.mp, monster.max_mp)))))

    print('-'*25)
