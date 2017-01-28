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

import sys
import random
import time
import math
import re
import pygame
from copy import copy as _c

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

temp_stats = ''
vowels = 'AEIOU'
turn_counter = 0

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]


def set_temp_stats():
    # Makes a copy of everyones stats so that temporary stat changes don't carry over after battle
    global temp_stats

    temp_stats = {
        main.player.name: {
            'attk': _c(main.player.attk),
            'dfns': _c(main.player.dfns),
            'p_attk': _c(main.player.p_attk),
            'p_dfns': _c(main.player.p_dfns),
            'm_attk': _c(main.player.m_attk),
            'm_dfns': _c(main.player.m_dfns),
            'spd': _c(main.player.spd),
            'evad': _c(main.player.evad),
            'ability_used': False
        },
        'Solou': {
            'attk': _c(main.solou.attk),
            'dfns': _c(main.solou.dfns),
            'p_attk': _c(main.solou.p_attk),
            'p_dfns': _c(main.solou.p_dfns),
            'm_attk': _c(main.solou.m_attk),
            'm_dfns': _c(main.solou.m_dfns),
            'spd': _c(main.solou.spd),
            'evad': _c(main.solou.evad),
            'ability_used': False
        },
        'Xoann': {
            'attk': _c(main.xoann.attk),
            'dfns': _c(main.xoann.dfns),
            'p_attk': _c(main.xoann.p_attk),
            'p_dfns': _c(main.xoann.p_dfns),
            'm_attk': _c(main.xoann.m_attk),
            'm_dfns': _c(main.xoann.m_dfns),
            'spd': _c(main.xoann.spd),
            'evad': _c(main.xoann.evad),
            'ability_used': False
        },

        'Randall': {
            'attk': _c(main.randall.attk),
            'dfns': _c(main.randall.dfns),
            'p_attk': _c(main.randall.p_attk),
            'p_dfns': _c(main.randall.p_dfns),
            'm_attk': _c(main.randall.m_attk),
            'm_dfns': _c(main.randall.m_dfns),
            'spd': _c(main.randall.spd),
            'evad': _c(main.randall.evad),
            'ability_used': False
        },

        'Parsto': {
            'attk': _c(main.parsto.attk),
            'dfns': _c(main.parsto.dfns),
            'p_attk': _c(main.parsto.p_attk),
            'p_dfns': _c(main.parsto.p_dfns),
            'm_attk': _c(main.parsto.m_attk),
            'm_dfns': _c(main.parsto.m_dfns),
            'spd': _c(main.parsto.spd),
            'evad': _c(main.parsto.evad),
            'ability_used': False
        },

        "Ran'af": {
            'attk': _c(main.ran_af.attk),
            'dfns': _c(main.ran_af.dfns),
            'p_attk': _c(main.ran_af.p_attk),
            'p_dfns': _c(main.ran_af.p_dfns),
            'm_attk': _c(main.ran_af.m_attk),
            'm_dfns': _c(main.ran_af.m_dfns),
            'spd': _c(main.ran_af.spd),
            'evad': _c(main.ran_af.evad),
            'ability_used': False
        },

        'Adorine': {
            'attk': _c(main.adorine.attk),
            'dfns': _c(main.adorine.dfns),
            'p_attk': _c(main.adorine.p_attk),
            'p_dfns': _c(main.adorine.p_dfns),
            'm_attk': _c(main.adorine.m_attk),
            'm_dfns': _c(main.adorine.m_dfns),
            'spd': _c(main.adorine.spd),
            'evad': _c(main.adorine.evad),
            'ability_used': False
        }
    }


def battle_system(is_boss=False, ambush=False):

    # Bosses use a different battle music than when battling normal enemies
    if is_boss:
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[monsters.monster.monster_name] % '')
        print('The legendary {0} has awoken!'.format(monster.name))
        main.smart_sleep(0.35)

    else:
        print(ascii_art.monster_art[monsters.monster.monster_name] % '')

        if any(map(monsters.monster.name.startswith, vowels)):  # Remember to use proper grammar!
            a_an = 'An '

        else:
            a_an = 'A '

        if ambush:
            print('{0}{1} ambushed you while you were resting!'.format(a_an, monsters.monster.name))

        else:
            print('{0}{1} suddenly appeared out of nowhere!'.format(a_an, monsters.monster.name))

        pygame.mixer.music.load('Music/Ruari 8-bit Battle.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        main.smart_sleep(1)

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    set_temp_stats()

    # While all active party members are alive, continue the battle
    while monsters.monster.hp > 0 and any([char.hp > 0 for char in [main.player,
                                                                    main.solou,
                                                                    main.xoann,
                                                                    main.randall,
                                                                    main.parsto,
                                                                    main.ran_af,
                                                                    main.adorine] if char.enabled]):

        # Check to see if any of your party members are have died, and alert the player
        # Then, check if any of them are asleep and do some powerful magic to make everything work
        for character in [x for x in [main.player,
                                      main.solou,
                                      main.xoann,
                                      main.randall,
                                      main.ran_af,
                                      main.adorine,
                                      main.parsto] if x.enabled]:

            if character.hp <= 0 and character.status_ail != 'dead':
                print('{0} has fallen to the {1}!'.format(character.name, monster.monster_name))
                sounds.ally_death.play()
                main.smart_sleep(0.75)

            if character.enabled and character.status_ail == 'asleep':
                character.battle_turn()

                if character.status_ail == 'asleep':
                    print(ascii_art.player_art["Asleep"] % "{0} is asleep, and cannot move!".format(character.name))
                    input("\nPress enter/return ")
                    sounds.poison_damage.play()

        # Display HP, MP, Levels, and Statuses for all battle participants
        bat_stats()

        # If any of your party members are at less than 20% health, play a small jingle
        for character in [x for x in [main.player,
                                      main.solou,
                                      main.xoann,
                                      main.randall,
                                      main.ran_af,
                                      main.adorine,
                                      main.parsto] if x.enabled]:

            if 0 < character.hp <= 0.20 * character.max_hp:
                print("Warning: {0}'s HP is low, heal as soon as possible!".format(character.name))
                sounds.health_low.play()
                main.smart_sleep(0.75)

        if character.status_ail != 'asleep':
            character.player_choice()

        # Make sure each participant in the battle goes according to who's fastest
        for unit in sorted([monsters.monster,
                            main.player,
                            main.solou,
                            main.xoann,
                            main.randall,
                            main.parsto,
                            main.ran_af,
                            main.adorine], key=lambda x: x.spd):

            if unit == monsters.monster or unit.enabled:
                if monsters.monster.hp <= 0:
                    break

                if isinstance(unit, main.PlayableCharacter) and (unit.status_ail == 'dead' or unit.move in ['2', '4']):
                    continue

                if unit.status_ail != 'asleep':
                    if unit.battle_turn() == 'Ran':
                        return

                if any(x.hp > 0 for x in [main.player,
                                          main.solou,
                                          main.xoann,
                                          main.randall,
                                          main.parsto,
                                          main.ran_af,
                                          main.adorine] if x.enabled):

                    if monsters.monster.hp > 0 and unit.status_ail != 'asleep':
                        input('\nPress enter/return ')

                else:
                    break

    else:
        if after_battle(is_boss) != 'dead':
            print('-'*25)


def run_away(runner):
    print(ascii_art.player_art[runner.class_.title()] % "{0} is making a move!\n".format(runner.name))
    print('Your party starts to run away from the {0}...'.format(monsters.monster.name))
    sounds.foot_steps.play()

    main.smart_sleep(0.75)

    if runner.status_ail == 'paralyzed':
        # 20% chance of success
        chance = 20

    elif bool(runner.spd > monsters.monster.spd) != bool(runner.evad > monsters.monster.evad):
        # 60% chance of success
        chance = 60

    elif runner.spd > monsters.monster.spd and runner.evad > monsters.monster.evad:
        # 80% chance of success
        chance = 80

    else:
        # 40% chance of success
        chance = 40

    if random.randint(0, 100) <= chance:
        print('Your party manages to escape from the {0}!'.format(monsters.monster.name))
        return True

    else:
        print("Your party's attempt to escape failed!")
        return False


def after_battle(is_boss):  # Assess the results of the battle
    print('-'*25)

    while True:
        # If the monster wins...
        if monsters.monster.hp > 0 and all([0 >= x.hp for x in [main.player,
                                                                main.solou,
                                                                main.xoann,
                                                                main.randall,
                                                                main.ran_af,
                                                                main.parsto,
                                                                main.adorine] if x.enabled]):
            pygame.mixer.music.load('Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            print('Despite your best efforts, the {0} has killed your party.'.format(monsters.monster.name))
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

                    main.party_info['x'] = main.party_info['prev_town'][0]
                    main.party_info['y'] = main.party_info['prev_town'][1]

                    for character in [main.player,
                                      main.solou,
                                      main.xoann,
                                      main.randall,
                                      main.ran_af,
                                      main.parsto,
                                      main.adorine]:

                        character.hp = _c(character.max_hp)
                        character.mp = _c(character.max_mp)
                        character.status_ail = "none"

                    pygame.mixer.music.load(main.party_info['reg_music'])
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
        elif monsters.monster.hp <= 0 < player.hp:
            pygame.mixer.music.load('Music/Python_RM.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            if not is_boss:
                # Only do the following if the player defeated a normal enemy, and not a boss
                print('The {0} falls to the ground, dead as a stone.'.format(monster.name))

                # Enemies drop gold/exp based on the player/monster's levels
                gold = 2.5*monster.lvl - main.player.lvl + random.randint(-1, 1)

                if gold <= 0:
                    gold = 1

            else:
                # Only do the following if the player defeated a boss
                bosses.defeated_bosses.append(monsters.monster.name)
                print('The almighty {0} has been slain!'.format(monsters.monster.name))

                # Bosses drop a set amount of gold
                gold = monsters.monster.gold

                # Check to see if the boss does anything special at death
                monsters.monster.upon_defeating()

            # If the monster has items, give them to the player
            if monsters.monster.items:
                cat = monsters.monster.items.cat
                inv_system.inventory[cat].append(_c(monsters.monster.items))

                sounds.item_pickup.play()
                input('The {0} dropped a {1}! Your party decides to take {2} | Press enter/return'.format(
                    monsters.monster.monster_name, str(monsters.monster.items),
                      'them' if str(monsters.monster.items).endswith('s') else 'it'))  # Grammar!!

            # Give the Player their GP
            main.party_info['gp'] += gold
            sounds.item_pickup.play()
            input('Your party has gained {0} GP | Press enter/return '.format(gold))

            for character in [x for x in [main.solou,
                                          main.xoann,
                                          main.player,
                                          main.randall,
                                          main.parsto,
                                          main.ran_af,
                                          main.adorine] if x.enabled]:

                # Give the Player their XP
                if is_boss:
                    experience = monsters.monster.experience

                else:
                    experience = math.ceil((monsters.monster.lvl**1.5 + character.ext_exp)/2) + 1

                if experience <= 0:
                    experience = 1

                character.exp += experience

                sounds.item_pickup.play()

                input('{0} gained {1} XP | Press enter/return '.format(character.name, experience))

                # Check to see if the player gained any levels
                character.level_up()

            pygame.mixer.music.load(main.party_info['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            pygame.mixer.music.set_volume(main.music_vol)

            return


def battle_inventory(user):
    # The player can use items from the "consum" category of their inventory during battles.
    if not inv_system.inventory['consum']:
        print('You have no battle-allowed items - the consumable category is empty!')
        print('-'*25)

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
                if item.status != user.status_ail:
                    print('{0} is not {1} - they have no reason to drink that.'.format(user.name, user.status))
                    print()
                    break

            item.use_item(user, is_battle=True)
            return True


def bat_stats():
    main.fix_stats()

    print('-'*25)

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    first_padding = len(max([main.player.name, main.solou.name, main.xoann.name, monsters.monster.name], key=len))

    second_padding = len(max(['{0}/{1} HP'.format(main.player.hp, main.player.max_hp)
                              if main.player.enabled else '',
                              '{0}/{1} HP'.format(main.solou.hp, main.solou.max_hp)
                              if main.solou.enabled else '',
                              '{0}/{1} HP'.format(main.xoann.hp, main.xoann.max_hp)
                              if main.xoann.enabled else '',
                              '{0}/{1} MP'.format(main.adorine.hp, main.adorine.max_hp)
                              if main.adorine.enabled else '',
                              '{0}/{1} MP'.format(main.randall.hp, main.randall.max_hp)
                              if main.randall.enabled else '',
                              '{0}/{1} MP'.format(main.ran_af.hp, main.ran_af.max_hp)
                              if main.ran_af.enabled else '',
                              '{0}/{1} MP'.format(main.parsto.hp, main.parsto.max_hp)
                              if main.parsto.enabled else '',
                              '{0}/{1} HP'.format(monsters.monster.hp, monsters.monster.max_hp)], key=len))

    third_padding = len(max(['{0}/{1} MP'.format(main.player.mp, main.player.max_mp)
                             if main.player.enabled else '',
                             '{0}/{1} MP'.format(main.solou.mp, main.solou.max_mp)
                             if main.solou.enabled else '',
                             '{0}/{1} MP'.format(main.xoann.mp, main.xoann.max_mp)
                             if main.xoann.enabled else '',
                             '{0}/{1} MP'.format(main.adorine.mp, main.adorine.max_mp)
                             if main.adorine.enabled else '',
                             '{0}/{1} MP'.format(main.randall.mp, main.randall.max_mp)
                             if main.randall.enabled else '',
                             '{0}/{1} MP'.format(main.ran_af.mp, main.ran_af.max_mp)
                             if main.ran_af.enabled else '',
                             '{0}/{1} MP'.format(main.parsto.mp, main.parsto.max_mp)
                             if main.parsto.enabled else '',
                             '{0}/{1} MP'.format(monsters.monster.mp, monsters.monster.max_mp)], key=len))

    # Player Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          main.player.name, main.player.hp,
          main.player.max_hp, main.player.mp,
          main.player.max_mp, main.player.lvl,
          main.player.status_ail.title(),
          pad1=' '*(first_padding - len(main.player.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.player.hp, main.player.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.player.mp, main.player.max_mp)))))

    if main.solou.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.solou.name, main.solou.hp,
              main.solou.max_hp, main.solou.mp,
              main.solou.max_mp, main.solou.lvl,
              main.solou.status_ail.title(),
              pad1=' '*(first_padding - len(main.solou.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.solou.hp, main.solou.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.solou.mp, main.solou.max_mp)))))

    if main.xoann.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.xoann.name, main.xoann.hp,
              main.xoann.max_hp, main.xoann.mp,
              main.xoann.max_mp, main.xoann.lvl,
              main.xoann.status_ail.title(),
              pad1=' '*(first_padding - len(xoann.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.xoann.hp, main.xoann.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.xoann.mp, main.xoann.max_mp)))))

    if main.randall.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.randall.name, main.randall.hp,
              main.randall.max_hp, main.randall.mp,
              main.randall.max_mp, main.randall.lvl,
              main.randall.status_ail.title(),
              pad1=' '*(first_padding - len(main.randall.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.randall.hp, main.randall.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.randall.mp, main.randall.max_mp)))))

    if main.parsto.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.parsto.name, main.parsto.hp,
              main.parsto.max_hp, main.parsto.mp,
              main.parsto.max_mp, main.parsto.lvl,
              main.parsto.status_ail.title(),
              pad1=' '*(first_padding - len(main.parsto.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.parsto.hp, main.parsto.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.parsto.mp, main.parsto.max_mp)))))

    if main.adorine.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.adorine.name, main.adorine.hp,
              main.adorine.max_hp, main.adorine.mp,
              main.adorine.max_mp, main.adorine.lvl,
              main.adorine.status_ail.title(),
              pad1=' '*(first_padding - len(main.adorine.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.adorine.hp, main.adorine.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.adorine.mp, main.adorine.max_mp)))))

    if main.ran_af.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              main.ran_af.name, main.ran_af.hp,
              main.ran_af.max_hp, main.ran_af.mp,
              main.ran_af.max_mp, main.ran_af.lvl,
              main.ran_af.status_ail.title(),
              pad1=' '*(first_padding - len(main.ran_af.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(main.ran_af.hp, main.ran_af.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(main.ran_af.mp, main.ran_af.max_mp)))))

    # Monster Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5}".format(
          monsters.monster.name, monsters.monster.hp,
          monsters.monster.max_hp, monsters.monster.mp,
          monsters.monster.max_mp, monsters.monster.lvl,
          pad1=' '*(first_padding - len(monsters.monster.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(monsters.monster.hp, monsters.monster.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(monsters.monster.mp, monsters.monster.max_mp)))))

    print('-'*25)
