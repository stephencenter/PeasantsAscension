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

import math
import random
import sys
from copy import copy as _c

import pygame

import ascii_art
import inv_system
import items
import sounds
import units

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

temp_stats = ''
vowels = 'AEIOU'
turn_counter = 0
m_list = []
enabled_pcus = []

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
    global m_list
    global enabled_pcus

    enabled_pcus = [x for x in [units.player,
                                units.solou,
                                units.xoann,
                                units.chyme,
                                units.ran_af,
                                units.adorine,
                                units.parsto] if x.enabled]

    # Add monsters to the battle.
    m_list = list()
    m_list.append(units.monster)
    if random.randint(0, 1):
        m_list.append(units.monster_2)
        if random.randint(0, 1):
            m_list.append(units.monster_3)

    # Bosses use a different battle music than when battling normal enemies
    if is_boss:
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[units.monster.monster_name] % '')

        if len(m_list) == 3:
            print(f'The legendary {units.monster.name} and 2 other monsters have awoken!')

        elif len(m_list) == 2:
            print(f'The legendary {units.monster.name} and 1 other monster have awoken!')

        else:
            print(f'The legendary {units.monster.name} has awoken!')

        main.smart_sleep(0.35)

    else:
        print(ascii_art.monster_art[units.monster.monster_name] % '')

        if any(map(units.monster.name.startswith, vowels)):  # Remember to use proper grammar!
            an_a = 'An'

        else:
            an_a = 'A'

        if len(m_list) == 3:
            if ambush:
                print(f'{an_a} {units.monster.name} and 2 other monsters ambushed you while you were resting!')

            else:
                print(f'{an_a} {units.monster.name} and 2 other monsters suddenly appeared out of nowhere!')

        elif len(m_list) == 2:
            if ambush:
                print(f'{an_a} {units.monster.name} and 1 other monster ambushed you while you were resting!')

            else:
                print(f'{an_a} {units.monster.name} and 1 other monster suddenly appeared out of nowhere!')

        else:
            if ambush:
                print(f'{an_a} {units.monster.name} ambushed you while you were resting!')

            else:
                print(f'{an_a} {units.monster.name} suddenly appeared out of nowhere!')

        pygame.mixer.music.load('Content/Music/Ruari 8-bit Battle.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        main.smart_sleep(1)

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    set_temp_stats()

    # While all active party members are alive, continue the battle
    while any([mstr.hp > 0 for mstr in m_list]) and any([char.hp > 0 for char in enabled_pcus]):
        # A list of the battle participants sorted by speed. Updates once per turn
        speed_list = sorted(m_list + enabled_pcus, key=lambda x: 0.5*x.spd if x.status_ail == "paralyzed" else x.spd,
                            reverse=True)

        # Display HP, MP, Levels, and Statuses for all battle participants
        bat_stats()

        for num, character in enumerate(enabled_pcus):
            # If any of your party members are at less than 20% health, play a small jingle
            if 0 < character.hp <= 0.20 * character.max_hp:
                print(f"Warning: {character.name}'s HP is low, heal as soon as possible!\n")
                sounds.health_low.play()
                main.smart_sleep(1)

            # Let each awake and alive character choose their move
            if character.status_ail != 'dead':
                character.player_choice()

                if num + 1 < len([x for x in enabled_pcus if x.status_ail != 'dead']):
                    print('-'*25)

        # Make sure each participant in the battle goes according to who's fastest
        for char in speed_list:
            if char.status_ail != 'dead':
                if all(x.hp <= 0 for x in m_list):
                    break

                print('-'*25)

                if char.battle_turn() == 'Ran':
                    return

                if any(x.hp > 0 for x in enabled_pcus):
                    if any(x.hp > 0 for x in m_list) and char.status_ail != 'dead':
                        input('\nPress enter/return ')

                    elif all(x.hp <= 0 for x in m_list):
                        break

                else:
                    break

            # Check if any characters died on the participants turn
            for char_2 in speed_list:
                if isinstance(char_2, units.PlayableCharacter) and char_2.hp <= 0 and char_2.status_ail != 'dead':
                    char_2.hp = 0
                    char_2.status_ail = 'dead'
                    sounds.ally_death.play()

                    print("-"*25)
                    print(f'{char_2.name} has fallen to the monsters!')
                    input("\nPress enter/return ")

                if isinstance(char_2, units.Monster) and char_2.hp <= 0 and char_2.status_ail != 'dead':
                    char_2.hp = 0
                    char_2.status_ail = 'dead'
                    sounds.buff_spell.play()

                    print("-"*25)
                    print(f'The {char_2.name} was defeated by your party!')
                    input("\nPress enter/return ")

    after_battle(is_boss)


def run_away(runner):
    print(ascii_art.player_art[runner.class_.title()] % f"{runner.name} is making a move!\n")
    print(f'Your party starts to run away from the {units.monster.name}...')
    sounds.foot_steps.play()

    main.smart_sleep(0.75)

    if runner.status_ail == 'paralyzed':
        # 20% chance of success
        chance = 20

    elif bool(runner.spd > sorted(m_list, key=lambda x: x.spd, reverse=True)[0].spd) != \
            bool(runner.evad > sorted(m_list, key=lambda x: x.evad, reverse=True)[0].spd):
        # 60% chance of success
        chance = 60

    elif runner.spd > sorted(m_list, key=lambda x: x.spd, reverse=True)[0].spd and \
            runner.evad > sorted(m_list, key=lambda x: x.evad, reverse=True)[0].spd:
        # 80% chance of success
        chance = 80

    else:
        # 40% chance of success
        chance = 40

    if random.randint(0, 100) <= chance:
        sounds.buff_spell.play()
        print(f'Your party manages to escape from the {units.monster.name}!')
        input("\nPress enter/return ")
        return True

    else:
        sounds.debuff.play()
        print("Your party's attempt to escape failed!")
        return False


def after_battle(is_boss):
    # Assess the results of the battle
    print('-'*25)

    for unit in enabled_pcus + m_list:
        if unit.hp <= 0 and unit.status_ail != 'dead':
            unit.hp = 0
            unit.status_ail = 'dead'

    while True:
        # If the monster wins...
        if any([m.status_ail != 'dead' for m in m_list]) and all([x.status_ail == 'dead' for x in enabled_pcus]):
            pygame.mixer.music.load('Content/Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            print(f'Despite your best efforts, the {units.monster.name} has killed your party.')
            print('-'*25)

            auto_yes = False
            while True:
                if auto_yes:
                    y_n = 'y'

                else:
                    y_n = input('Do you wish to continue playing? | Yes or No: ').lower()

                if y_n.startswith('y'):
                    # If you die, you return to the last town visited or 0'N, 0'E
                    # if you haven't been to a town yet.

                    main.party_info['current_tile'] = main.party_info['prev_town']
                    main.party_info['x'], main.party_info['y'], main.party_info['z'] = main.party_info['p_town_xyz']

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

                    return

                elif y_n.startswith('n'):
                    while True:
                        y_n = input('Are you sure you want to quit and lose all unsaved progress? | Yes or No: ')
                        y_n = y_n

                        if y_n.startswith('y'):
                            pygame.quit()
                            sys.exit()

                        elif y_n.startswith('n'):
                            auto_yes = True

                            break

        # If the player wins...
        elif all([m.status_ail == 'dead' for m in m_list]) and any([x.status_ail != 'dead' for x in enabled_pcus]):
            pygame.mixer.music.load('Content/Music/Python_RM.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            if not is_boss:
                # Only do the following if the player defeated a normal enemy, and not a boss
                print(f'The {units.monster.name} falls to the ground, dead as a stone.')

                # Enemies drop gold/exp based on the player/monster's levels
                gold = math.ceil(2.5*units.monster.lvl - units.player.lvl + random.randint(-1, 1))

                if gold <= 0:
                    gold = 1

            else:
                # Only do the following if the player defeated a boss
                units.defeated_bosses.append(units.monster.name)
                print(f'The almighty {units.monster.name} has been slain!')

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
            input(f'Your party has gained {gold} GP | Press enter/return ')

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

                input(f'{character.name} gained {experience} XP | Press enter/return ')

                # Check to see if the player gained any levels
                character.level_up()

            pygame.mixer.music.load(main.party_info['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            pygame.mixer.music.set_volume(main.music_vol)

            return

        else:
            units.player.hp = 1
            units.player.status_ail = 'none'

            continue


def battle_inventory(user):
    # The player can use items from the Consumables category of their inventory during battles.

    while True:
        print('Battle Inventory: \n      ', end='')
        print('\n      '.join([f'[{x + 1}] {y}' for x, y in enumerate(inv_system.inventory['consumables'])]))

        while True:
            item = input('Input [#] (or type "exit"): ').lower()

            try:
                item = inv_system.inventory['consumables'][int(item) - 1]

            except (ValueError, IndexError):
                if item in ['e', 'x', 'exit', 'b', 'back']:
                    return False

                continue

            print('\n-Player Turn-')

            if isinstance(item, items.StatusPotion):
                if item.status != user.status_ail:
                    print(f'{user.name} is not {user.status} - they have no reason to drink that.')
                    break

            item.use_item(user, is_battle=True)
            return True


def bat_stats():
    units.fix_stats()

    print('-'*25)

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    first_padding = max([len(x.name) for x in enabled_pcus + m_list])

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
                              '{0}/{1} HP'.format(units.monster_2.hp, units.monster_2.max_hp)
                              if units.monster_2 in m_list else '',
                              '{0}/{1} HP'.format(units.monster_3.hp, units.monster_3.max_hp)
                              if units.monster_3 in m_list else '',
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
                             '{0}/{1} HP'.format(units.monster_2.mp, units.monster_2.max_mp)
                             if units.monster_2 in m_list else '',
                             '{0}/{1} HP'.format(units.monster_3.mp, units.monster_3.max_mp)
                             if units.monster_3 in m_list else '',
                             '{0}/{1} MP'.format(units.monster.mp, units.monster.max_mp)], key=len))
    # Player Stats
    print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          units.player.name, units.player.hp,
          units.player.max_hp, units.player.mp,
          units.player.max_mp, units.player.lvl,
          units.player.status_ail.upper(),
          pad1=' '*(first_padding - len(units.player.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.player.hp, units.player.max_hp))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.player.mp, units.player.max_mp)))),
            "red" if units.player.status_ail == 'dead' else 'clear'))

    if units.solou.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.solou.name, units.solou.hp,
              units.solou.max_hp, units.solou.mp,
              units.solou.max_mp, units.solou.lvl,
              units.solou.status_ail.upper(),
              pad1=' '*(first_padding - len(units.solou.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.solou.hp, units.solou.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.solou.mp, units.solou.max_mp)))),
            "red" if units.solou.status_ail == 'dead' else 'clear'))

    if units.xoann.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.xoann.name, units.xoann.hp,
              units.xoann.max_hp, units.xoann.mp,
              units.xoann.max_mp, units.xoann.lvl,
              units.xoann.status_ail.upper(),
              pad1=' '*(first_padding - len(units.xoann.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.xoann.hp, units.xoann.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.xoann.mp, units.xoann.max_mp)))),
            "red" if units.xoann.status_ail == 'dead' else 'clear'))

    if units.chyme.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.chyme.name, units.chyme.hp,
              units.chyme.max_hp, units.chyme.mp,
              units.chyme.max_mp, units.chyme.lvl,
              units.chyme.status_ail.upper(),
              pad1=' '*(first_padding - len(units.chyme.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.chyme.hp, units.chyme.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.chyme.mp, units.chyme.max_mp)))),
            "red" if units.chyme.status_ail == 'dead' else 'clear'))

    if units.parsto.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.parsto.name, units.parsto.hp,
              units.parsto.max_hp, units.parsto.mp,
              units.parsto.max_mp, units.parsto.lvl,
              units.parsto.status_ail.upper(),
              pad1=' '*(first_padding - len(units.parsto.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.parsto.hp, units.parsto.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.parsto.mp, units.parsto.max_mp)))),
            "red" if units.parsto.status_ail == 'dead' else 'clear'))

    if units.adorine.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.adorine.name, units.adorine.hp,
              units.adorine.max_hp, units.adorine.mp,
              units.adorine.max_mp, units.adorine.lvl,
              units.adorine.status_ail.upper(),
              pad1=' '*(first_padding - len(units.adorine.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.adorine.hp, units.adorine.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.adorine.mp, units.adorine.max_mp)))),
            "red" if units.adorine.status_ail == 'dead' else 'clear'))

    if units.ran_af.enabled:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.ran_af.name, units.ran_af.hp,
              units.ran_af.max_hp, units.ran_af.mp,
              units.ran_af.max_mp, units.ran_af.lvl,
              units.ran_af.status_ail.upper(),
              pad1=' '*(first_padding - len(units.ran_af.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(units.ran_af.hp, units.ran_af.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(units.ran_af.mp, units.ran_af.max_mp)))),
            "red" if units.ran_af.status_ail == 'dead' else 'clear'))
    # Monster Stats
    for each_monster in m_list:
        print(ascii_art.colorize("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              each_monster.name, each_monster.hp,
              each_monster.max_hp, each_monster.mp,
              each_monster.max_mp, each_monster.lvl,
              each_monster.status_ail.upper(),
              pad1=' '*(first_padding - len(each_monster.name)),
              pad2=' '*(second_padding - len('{0}/{1} HP'.format(each_monster.hp, each_monster.max_hp))),
              pad3=' '*(third_padding - len('{0}/{1} MP'.format(each_monster.mp, each_monster.max_mp)))),
            "red" if each_monster.status_ail == 'dead' else 'clear'))

    print('-'*25)
