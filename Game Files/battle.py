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
import units
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
        units.player.name: {
            'attk': _c(units.player.attk),
            'dfns': _c(units.player.dfns),
            'p_attk': _c(units.player.p_attk),
            'p_dfns': _c(units.player.p_dfns),
            'm_attk': _c(units.player.m_attk),
            'm_dfns': _c(units.player.m_dfns),
            'spd': _c(units.player.spd),
            'evad': _c(units.player.evad),
            'ability_used': False
        },
        'Solou': {
            'attk': _c(units.solou.attk),
            'dfns': _c(units.solou.dfns),
            'p_attk': _c(units.solou.p_attk),
            'p_dfns': _c(units.solou.p_dfns),
            'm_attk': _c(units.solou.m_attk),
            'm_dfns': _c(units.solou.m_dfns),
            'spd': _c(units.solou.spd),
            'evad': _c(units.solou.evad),
            'ability_used': False
        },
        'Xoann': {
            'attk': _c(units.xoann.attk),
            'dfns': _c(units.xoann.dfns),
            'p_attk': _c(units.xoann.p_attk),
            'p_dfns': _c(units.xoann.p_dfns),
            'm_attk': _c(units.xoann.m_attk),
            'm_dfns': _c(units.xoann.m_dfns),
            'spd': _c(units.xoann.spd),
            'evad': _c(units.xoann.evad),
            'ability_used': False
        },

        'Chyme': {
            'attk': _c(units.chyme.attk),
            'dfns': _c(units.chyme.dfns),
            'p_attk': _c(units.chyme.p_attk),
            'p_dfns': _c(units.chyme.p_dfns),
            'm_attk': _c(units.chyme.m_attk),
            'm_dfns': _c(units.chyme.m_dfns),
            'spd': _c(units.chyme.spd),
            'evad': _c(units.chyme.evad),
            'ability_used': False
        },

        'Parsto': {
            'attk': _c(units.parsto.attk),
            'dfns': _c(units.parsto.dfns),
            'p_attk': _c(units.parsto.p_attk),
            'p_dfns': _c(units.parsto.p_dfns),
            'm_attk': _c(units.parsto.m_attk),
            'm_dfns': _c(units.parsto.m_dfns),
            'spd': _c(units.parsto.spd),
            'evad': _c(units.parsto.evad),
            'ability_used': False
        },

        "Ran'af": {
            'attk': _c(units.ran_af.attk),
            'dfns': _c(units.ran_af.dfns),
            'p_attk': _c(units.ran_af.p_attk),
            'p_dfns': _c(units.ran_af.p_dfns),
            'm_attk': _c(units.ran_af.m_attk),
            'm_dfns': _c(units.ran_af.m_dfns),
            'spd': _c(units.ran_af.spd),
            'evad': _c(units.ran_af.evad),
            'ability_used': False
        },

        'Adorine': {
            'attk': _c(units.adorine.attk),
            'dfns': _c(units.adorine.dfns),
            'p_attk': _c(units.adorine.p_attk),
            'p_dfns': _c(units.adorine.p_dfns),
            'm_attk': _c(units.adorine.m_attk),
            'm_dfns': _c(units.adorine.m_dfns),
            'spd': _c(units.adorine.spd),
            'evad': _c(units.adorine.evad),
            'ability_used': False
        }
    }


def battle_system(is_boss=False, ambush=False):
    enabled_pcus = [x for x in [units.player,
                                units.solou,
                                units.xoann,
                                units.chyme,
                                units.ran_af,
                                units.adorine,
                                units.parsto] if x.enabled]

    # Bosses use a different battle music than when battling normal enemies
    if is_boss:
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[units.monster.monster_name] % '')
        print('The legendary {0} has awoken!'.format(units.monster.name))
        main.smart_sleep(0.35)

    else:
        print(ascii_art.monster_art[units.monster.monster_name] % '')

        if any(map(units.monster.name.startswith, vowels)):  # Remember to use proper grammar!
            a_an = 'An '

        else:
            a_an = 'A '

        if ambush:
            print('{0}{1} ambushed you while you were resting!'.format(a_an, units.monster.name))

        else:
            print('{0}{1} suddenly appeared out of nowhere!'.format(a_an, units.monster.name))

        pygame.mixer.music.load('Music/Ruari 8-bit Battle.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        main.smart_sleep(1)

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    set_temp_stats()

    # While all active party members are alive, continue the battle
    while units.monster.hp > 0 and any([char.hp > 0 for char in enabled_pcus]):

        # Check to see if any of your party members are have died, and alert the player
        # Then, check if any of them are asleep and do some powerful magic to make everything work
        for character in enabled_pcus:
            if character.enabled and character.status_ail == 'asleep':
                character.battle_turn()

                if character.status_ail == 'asleep':
                    print(ascii_art.player_art["Asleep"] % f"{character.name} is asleep, and cannot move!")
                    input("\nPress enter/return ")
                    sounds.poison_damage.play()

        # Display HP, MP, Levels, and Statuses for all battle participants
        bat_stats()

        for num, character in enumerate(enabled_pcus) :

            # If any of your party members are at less than 20% health, play a small jingle
            if 0 < character.hp <= 0.20 * character.max_hp:
                print(f"Warning: {character.name}'s HP is low, heal as soon as possible!\n")
                sounds.health_low.play()
                main.smart_sleep(1)

            # Let each awake and alive character choose their move
            if character.status_ail not in ['asleep', 'dead']:
                character.player_choice()

                if num + 1 < len(enabled_pcus):
                    print('-'*25)

        # Make sure each participant in the battle goes according to who's fastest
        for char in sorted([units.monster] + enabled_pcus,
                           key=lambda x: 0.5*x.spd if x.status_ail == "paralyzed" else x.spd, reverse=True):

            if char.status_ail != 'dead':
                if units.monster.hp <= 0:
                    break

                if isinstance(char, units.PlayableCharacter) and (char.status_ail == 'dead' or char.move in ['2', '4']):
                    continue

                if char.status_ail != 'asleep':
                    print('-'*25)
                    if char.battle_turn() == 'Ran':
                        return

                if any(x.hp > 0 for x in enabled_pcus):
                    if units.monster.hp > 0 and char.status_ail != 'asleep':
                        input('\nPress enter/return ')

                else:
                    break

            if isinstance(char, units.PlayableCharacter) and char.hp <= 0 and char.status_ail != 'dead':
                char.hp = 0
                char.status_ail = 'dead'
                sounds.ally_death.play()

                print("-"*25)
                print(f'{char.name} has fallen to the {units.monster.monster_name}!')
                input("\nPress enter/return ")

    else:
        if after_battle(is_boss) != 'dead':
            print('-'*25)


def run_away(runner):
    print(ascii_art.player_art[runner.class_.title()] % "{0} is making a move!\n".format(runner.name))
    print('Your party starts to run away from the {0}...'.format(units.monster.name))
    sounds.foot_steps.play()

    main.smart_sleep(0.75)

    if runner.status_ail == 'paralyzed':
        # 20% chance of success
        chance = 20

    elif bool(runner.spd > units.monster.spd) != bool(runner.evad > units.monster.evad):
        # 60% chance of success
        chance = 60

    elif runner.spd > units.monster.spd and runner.evad > units.monster.evad:
        # 80% chance of success
        chance = 80

    else:
        # 40% chance of success
        chance = 40

    if random.randint(0, 100) <= chance:
        print('Your party manages to escape from the {0}!'.format(units.monster.name))
        return True

    else:
        print("Your party's attempt to escape failed!")
        return False


def after_battle(is_boss):  # Assess the results of the battle
    print('-'*25)
    enabled_pcus = [x for x in [units.player,
                                units.solou,
                                units.xoann,
                                units.chyme,
                                units.ran_af,
                                units.adorine,
                                units.parsto] if x.enabled]

    while True:
        # If the monster wins...
        if units.monster.hp > 0 and all([0 >= x.hp for x in enabled_pcus]):
            pygame.mixer.music.load('Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            print('Despite your best efforts, the {0} has killed your party.'.format(units.monster.name))
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

                    for character in [units.player,
                                      units.solou,
                                      units.xoann,
                                      units.chyme,
                                      units.ran_af,
                                      units.parsto,
                                      units.adorine]:

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
        elif units.monster.hp <= 0 < units.player.hp:
            pygame.mixer.music.load('Music/Python_RM.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            if not is_boss:
                # Only do the following if the player defeated a normal enemy, and not a boss
                print('The {0} falls to the ground, dead as a stone.'.format(units.monster.name))

                # Enemies drop gold/exp based on the player/monster's levels
                gold = math.ceil(2.5*units.monster.lvl - units.player.lvl + random.randint(-1, 1))

                if gold <= 0:
                    gold = 1

            else:
                # Only do the following if the player defeated a boss
                bosses.defeated_bosses.append(units.monster.name)
                print('The almighty {0} has been slain!'.format(units.monster.name))

                # Bosses drop a set amount of gold
                gold = units.monster.gold

                # Check to see if the boss does anything special at death
                units.monster.upon_defeating()

            # If the monster has items, give them to the player
            if units.monster.items:
                cat = units.monster.items.cat
                inv_system.inventory[cat].append(_c(units.monster.items))

                sounds.item_pickup.play()
                input('The {0} dropped a {1}! Your party decides to take {2} | Press enter/return'.format(
                    units.monster.monster_name, str(units.monster.items),
                      'them' if str(units.monster.items).endswith('s') else 'it'))  # Grammar!!

            # Give the Player their GP
            main.party_info['gp'] += gold
            sounds.item_pickup.play()
            input('Your party has gained {0} GP | Press enter/return '.format(gold))

            for character in enabled_pcus:

                # Give the Player their XP
                if is_boss:
                    experience = units.monster.experience

                else:
                    experience = math.ceil((units.monster.lvl**1.5 + character.ext_exp)/2) + 1

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
    units.fix_stats()

    print('-'*25)

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    first_padding = len(max([units.player.name, units.solou.name, units.xoann.name, units.monster.name], key=len))

    second_padding = len(max(['{0}/{1} HP'.format(units.player.hp, units.player.max_hp)
                              if units.player.enabled else '',
                              '{0}/{1} HP'.format(units.solou.hp, units.solou.max_hp)
                              if units.solou.enabled else '',
                              '{0}/{1} HP'.format(units.xoann.hp, units.xoann.max_hp)
                              if units.xoann.enabled else '',
                              '{0}/{1} MP'.format(units.adorine.hp, units.adorine.max_hp)
                              if units.adorine.enabled else '',
                              '{0}/{1} MP'.format(units.chyme.hp, units.chyme.max_hp)
                              if units.chyme.enabled else '',
                              '{0}/{1} MP'.format(units.ran_af.hp, units.ran_af.max_hp)
                              if units.ran_af.enabled else '',
                              '{0}/{1} MP'.format(units.parsto.hp, units.parsto.max_hp)
                              if units.parsto.enabled else '',
                              '{0}/{1} HP'.format(units.monster.hp, units.monster.max_hp)], key=len))

    third_padding = len(max(['{0}/{1} MP'.format(units.player.mp, units.player.max_mp)
                             if units.player.enabled else '',
                             '{0}/{1} MP'.format(units.solou.mp, units.solou.max_mp)
                             if units.solou.enabled else '',
                             '{0}/{1} MP'.format(units.xoann.mp, units.xoann.max_mp)
                             if units.xoann.enabled else '',
                             '{0}/{1} MP'.format(units.adorine.mp, units.adorine.max_mp)
                             if units.adorine.enabled else '',
                             '{0}/{1} MP'.format(units.chyme.mp, units.chyme.max_mp)
                             if units.chyme.enabled else '',
                             '{0}/{1} MP'.format(units.ran_af.mp, units.ran_af.max_mp)
                             if units.ran_af.enabled else '',
                             '{0}/{1} MP'.format(units.parsto.mp, units.parsto.max_mp)
                             if units.parsto.enabled else '',
                             '{0}/{1} MP'.format(units.monster.mp, units.monster.max_mp)], key=len))

    # Player Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          units.player.name, units.player.hp,
          units.player.max_hp, units.player.mp,
          units.player.max_mp, units.player.lvl,
          units.player.status_ail.title(),
          pad1=' '*(first_padding - len(units.player.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.player.hp, units.player.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.player.mp, units.player.max_mp)))))

    if units.solou.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.solou.name, units.solou.hp,
              units.solou.max_hp, units.solou.mp,
              units.solou.max_mp, units.solou.lvl,
              units.solou.status_ail.title(),
              pad1=' '*(first_padding - len(units.solou.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.solou.hp, units.solou.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.solou.mp, units.solou.max_mp)))))

    if units.xoann.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.xoann.name, units.xoann.hp,
              units.xoann.max_hp, units.xoann.mp,
              units.xoann.max_mp, units.xoann.lvl,
              units.xoann.status_ail.title(),
              pad1=' '*(first_padding - len(xoann.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.xoann.hp, units.xoann.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.xoann.mp, units.xoann.max_mp)))))

    if units.chyme.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.chyme.name, units.chyme.hp,
              units.chyme.max_hp, units.chyme.mp,
              units.chyme.max_mp, units.chyme.lvl,
              units.chyme.status_ail.title(),
              pad1=' '*(first_padding - len(units.chyme.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.chyme.hp, units.chyme.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.chyme.mp, units.chyme.max_mp)))))

    if units.parsto.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.parsto.name, units.parsto.hp,
              units.parsto.max_hp, units.parsto.mp,
              units.parsto.max_mp, units.parsto.lvl,
              units.parsto.status_ail.title(),
              pad1=' '*(first_padding - len(units.parsto.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.parsto.hp, units.parsto.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.parsto.mp, units.parsto.max_mp)))))

    if units.adorine.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.adorine.name, units.adorine.hp,
              units.adorine.max_hp, units.adorine.mp,
              units.adorine.max_mp, units.adorine.lvl,
              units.adorine.status_ail.title(),
              pad1=' '*(first_padding - len(units.adorine.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.adorine.hp, units.adorine.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.adorine.mp, units.adorine.max_mp)))))

    if units.ran_af.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.ran_af.name, units.ran_af.hp,
              units.ran_af.max_hp, units.ran_af.mp,
              units.ran_af.max_mp, units.ran_af.lvl,
              units.ran_af.status_ail.title(),
              pad1=' '*(first_padding - len(units.ran_af.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.ran_af.hp, units.ran_af.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.ran_af.mp, units.ran_af.max_mp)))))

    # Monster Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5}".format(
          units.monster.name, units.monster.hp,
          units.monster.max_hp, units.monster.mp,
          units.monster.max_mp, units.monster.lvl,
          pad1=' '*(first_padding - len(units.monster.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.monster.hp, units.monster.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.monster.mp, units.monster.max_mp)))))

    print('-'*25)
