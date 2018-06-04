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

import math
import random
import sys
from copy import copy as _c

import pygame

import ascii_art
import items
import save_load
import sounds
import units

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

temp_stats = ''
vowels = 'AEIOU'
m_list = []
enabled_pcus = []
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
            'attributes': _c(units.player.attributes)
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
            'attributes': _c(units.solou.attributes)
        },
        'Chili': {
            'attk': _c(units.chili.attk),
            'dfns': _c(units.chili.dfns),
            'p_attk': _c(units.chili.p_attk),
            'p_dfns': _c(units.chili.p_dfns),
            'm_attk': _c(units.chili.m_attk),
            'm_dfns': _c(units.chili.m_dfns),
            'spd': _c(units.chili.spd),
            'evad': _c(units.chili.evad),
            'attributes': _c(units.chili.attributes)
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
            'attributes': _c(units.chyme.attributes)
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
            'attributes': _c(units.parsto.attributes)
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
            'attributes': _c(units.ran_af.attributes)
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
            'attributes': _c(units.player.attributes)
        }

    }

    for pcu in enabled_pcus:
        pcu.reset_ability_vars()


def battle_system(is_boss=False, ambush=False):
    global m_list
    global enabled_pcus
    global turn_counter

    enabled_pcus = [x for x in [units.player,
                                units.solou,
                                units.chili,
                                units.chyme,
                                units.ran_af,
                                units.adorine,
                                units.parsto] if x.enabled]
    turn_counter = 0

    # Bosses use a different battle music than when battling normal enemies
    if is_boss:
        m_list = ([units.monster] + units.monster.lackies) if units.monster.lackies else [units.monster]

        print(ascii_art.monster_art[units.monster.m_name] % '')

        if len(m_list) > 2:
            print(f'The legendary {units.monster.name} and its lackys have awoken!')

        elif len(m_list) == 2:
            print(f'The legendary {units.monster.name} and its lacky have awoken!')

        else:
            print(f'The legendary {units.monster.name} has awoken!')

        main.smart_sleep(0.35)

    else:
        # Add monsters to the battle.
        m_list = [units.monster]
        if random.randint(0, 1):
            m_list.append(units.monster_2)

            if random.randint(0, 1):
                m_list.append(units.monster_3)

        print(ascii_art.monster_art[units.monster.m_name] % '')

        if len(m_list) == 3:
            if ambush:
                print(f'A {units.monster.name} and 2 other monsters ambushed you while you were resting!')

            else:
                print(f'A {units.monster.name} and 2 other monsters suddenly appeared out of nowhere!')

        elif len(m_list) == 2:
            if ambush:
                print(f'A {units.monster.name} and 1 other monster ambushed you while you were resting!')

            else:
                print(f'A {units.monster.name} and 1 other monster suddenly appeared out of nowhere!')

        else:
            if ambush:
                print(f'A {units.monster.name} ambushed you while you were resting!')

            else:
                print(f'A {units.monster.name} suddenly appeared out of nowhere!')

        sounds.play_music('../Music/Ruari 8-bit Battle.ogg')

        main.smart_sleep(1)

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    set_temp_stats()
    main.party_info['gamestate'] = 'battle'

    # While all active party members are alive, continue the battle
    while any([mstr.hp > 0 for mstr in m_list]) and any([char.hp > 0 for char in enabled_pcus]):
        turn_counter += 1

        # A list of the battle participants sorted by speed. Updates once per turn.
        speed_list = sorted(m_list + enabled_pcus,
                            key=lambda x: 0.5*x.spd if "paralyzed" in x.status_ail else x.spd,
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
            if 'dead' not in character.status_ail:
                character.player_choice()

                if num + 1 < len([x for x in enabled_pcus if x.status_ail != 'dead']):
                    print('-'*save_load.divider_size)

        # Make sure each participant in the battle goes according to who's fastest
        for char in speed_list:
            if 'dead' not in char.status_ail:
                if all(x.hp <= 0 for x in m_list):
                    break

                print('-'*save_load.divider_size)

                if ((isinstance(char, units.PlayableCharacter) and char.battle_turn() == 'Ran') or
                        (isinstance(char, units.Monster) and char.base_turn() == 'Ran')):
                    return

                if any(x.hp > 0 for x in enabled_pcus):
                    if any(x.hp > 0 for x in m_list) and 'dead' not in char.status_ail:
                        main.s_input('\nPress enter/return ')

                    elif all(x.hp <= 0 for x in m_list):
                        break

                else:
                    break

            # Check if any characters died on the participants turn
            for char_2 in speed_list:
                if isinstance(char_2, units.PlayableCharacter) and char_2.hp <= 0 and 'dead' not in char_2.status_ail:
                    char_2.hp = 0
                    char_2.status_ail = ['dead']
                    sounds.ally_death.play()

                    print('-'*save_load.divider_size)
                    print(f"{char_2.name} has fallen to the monsters!")
                    main.s_input("\nPress enter/return ")

                if isinstance(char_2, units.Monster) and char_2.hp <= 0 and 'dead' not in char_2.status_ail:
                    char_2.hp = 0
                    char_2.status_ail = ['dead']
                    sounds.enemy_death.play()

                    print('-'*save_load.divider_size)
                    print(f"The {char_2.name} was defeated by your party!")
                    main.s_input("\nPress enter/return ")

    after_battle(is_boss)


def run_away(runner):
    print(ascii_art.player_art[runner.class_.title()] % f"{runner.name} is making a move!\n")
    print(f'Your party starts to run away from the {units.monster.name}...')
    sounds.foot_steps.play()

    main.smart_sleep(0.75)

    if 'paralyzed' in runner.status_ail:
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
        main.s_input("\nPress enter/return ")
        return True

    else:
        sounds.debuff.play()
        print("Your party's attempt to escape failed!")
        return False


def after_battle(is_boss):
    # Assess the results of the battle
    print('-'*save_load.divider_size)

    for unit in enabled_pcus + m_list:
        if unit.hp <= 0 and 'dead' not in unit.status_ail:
            unit.hp = 0
            unit.status_ail = ['dead']

    while True:
        # If the monster wins...
        if any(['dead' not in m.status_ail for m in m_list]) and all(['dead' in x.status_ail for x in enabled_pcus]):
            sounds.play_music('../Music/Power-Up.ogg')

            print(f'Despite your best efforts, the {units.monster.name} has killed your party.')
            print('-'*save_load.divider_size)

            auto_yes = False
            while True:
                if auto_yes:
                    y_n = 'y'

                else:
                    y_n = main.s_input('Do you wish to continue playing? | Y/N: ').lower()

                if y_n.startswith('y'):
                    # If you die, you return to the last town visited or 0'N, 0'W if you haven't been to a town yet.

                    main.party_info['current_tile'] = main.party_info['prev_town']
                    units.heal_pcus(1)

                    sounds.play_music(main.party_info['music'])

                    return

                elif y_n.startswith('n'):
                    while True:
                        y_n = main.s_input('Are you sure you want to quit and lose unsaved progress? |  Y/N: ').lower()

                        if y_n.startswith('n') or main.do_debug:
                            auto_yes = True

                            break

                        elif y_n.startswith('y'):
                            pygame.quit()
                            sys.exit()

        # If the player wins...
        elif all(['dead' in m.status_ail for m in m_list]) and any(['dead' not in x.status_ail for x in enabled_pcus]):
            sounds.play_music('../Music/Python_RM.ogg')

            if not is_boss:
                print(f'The {units.monster.name} falls to the ground, dead as a stone.')

            else:
                print(f'The almighty {units.monster.name} has been slain!')
                units.defeated_bosses.append(units.monster.name)
                units.monster.upon_defeating()

            # Formulas for item, gold, and experience drops
            gold_drops = math.ceil(sum([max(1, x.gold, 2.5*x.lvl) for x in m_list]))
            expr_drops = math.ceil(sum([max(1, y.experience, 1.5**y.lvl)/2 for y in m_list]))
            item_drops = [(z.name, z.items) for z in m_list if z.items]

            main.party_info['gp'] += gold_drops
            main.s_input(f'Your party has gained {gold_drops} GP! ')

            # Each party member gets their own XP
            for character in enabled_pcus:
                character.exp += expr_drops
                main.s_input(f'{character.name} gained {expr_drops} XP! ')

            # Each monster can drop their own item
            for drop in item_drops:
                print(f"The {drop[0]} dropped a {drop[1].name}! ")
                items.inventory[drop[1].cat].append(drop[1])

            for character in enabled_pcus:
                character.level_up()

            sounds.play_music(main.party_info['music'])

            return

        else:
            units.player.hp = 1
            units.player.status_ail = ['alive']

            continue


def battle_inventory(user):
    # The player can use items from the Consumables category of their inventory during battles.
    while True:
        print('Battle Inventory: ')

        for x, y in enumerate(items.inventory['consumables']):
            print(f'      [{x + 1}] {y.name}')

        while True:
            item = main.s_input('Input [#] (or type "exit"): ').lower()

            try:
                item = items.inventory['consumables'][int(item) - 1]

            except (IndexError, ValueError):
                if item in ['e', 'x', 'exit', 'b', 'back']:
                    print('-'*save_load.divider_size)
                    return False

                continue

            if isinstance(item, items.StatusPotion):
                if item.status != user.status_ail:
                    print(f'{user.name} is not {user.status} - they have no reason to drink that.')
                    break

            print('-' * save_load.divider_size)
            item.use_item(user, is_battle=True)
            return True


def bat_stats():
    units.fix_stats()

    print('-'*save_load.divider_size)

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    first_padding = max([len(x.name) for x in enabled_pcus + m_list])

    second_padding = len(max([f'{units.player.hp}/{units.player.max_hp} HP' if units.player.enabled else '',
                              f'{units.solou.hp}/{units.solou.max_hp} HP' if units.solou.enabled else '',
                              f'{units.chili.hp}/{units.chili.max_hp} HP' if units.chili.enabled else '',
                              f'{units.adorine.hp}/{units.adorine.max_hp} HP' if units.adorine.enabled else '',
                              f'{units.chyme.hp}/{units.chyme.max_hp} HP' if units.chyme.enabled else '',
                              f'{units.ran_af.hp}/{units.ran_af.max_hp} HP' if units.ran_af.enabled else '',
                              f'{units.parsto.hp}/{units.parsto.max_hp} HP' if units.parsto.enabled else '',
                              f'{units.monster_2.hp}/{units.monster_2.max_hp} HP' if units.monster_2 in m_list else '',
                              f'{units.monster_3.hp}/{units.monster_3.max_hp} HP' if units.monster_3 in m_list else '',
                              f'{units.monster.hp}/{units.monster.max_hp} HP'], key=len))

    third_padding = len(max([f'{units.player.mp}/{units.player.max_mp} MP' if units.player.enabled else '',
                             f'{units.solou.mp}/{units.solou.max_mp} MP' if units.solou.enabled else '',
                             f'{units.chili.mp}/{units.chili.max_mp} MP' if units.chili.enabled else '',
                             f'{units.adorine.mp}/{units.adorine.max_mp} MP' if units.adorine.enabled else '',
                             f'{units.chyme.mp}/{units.chyme.max_mp} MP' if units.chyme.enabled else '',
                             f'{units.ran_af.mp}/{units.ran_af.max_mp} MP' if units.ran_af.enabled else '',
                             f'{units.parsto.mp}/{units.parsto.max_mp} MP' if units.parsto.enabled else '',
                             f'{units.monster_2.mp}/{units.monster_2.max_mp} MP' if units.monster_2 in m_list else '',
                             f'{units.monster_3.mp}/{units.monster_3.max_mp} MP' if units.monster_3 in m_list else '',
                             f'{units.monster.mp}/{units.monster.max_mp} MP'], key=len))
    # Player Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          units.player.name, units.player.hp,
          units.player.max_hp, units.player.mp,
          units.player.max_mp, units.player.lvl,
          ', '.join([x.title() for x in units.player.status_ail]),
          pad1=' '*(first_padding - len(units.player.name)),
          pad2=' '*(second_padding - len(f'{units.player.hp}/{units.player.max_hp} HP')),
          pad3=' '*(third_padding - len(f'{units.player.mp}/{units.player.max_mp} MP'))))

    if units.solou.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.solou.name, units.solou.hp,
              units.solou.max_hp, units.solou.mp,
              units.solou.max_mp, units.solou.lvl,
              ', '.join([x.title() for x in units.solou.status_ail]),
              pad1=' '*(first_padding - len(units.solou.name)),
              pad2=' '*(second_padding - len(f'{units.solou.hp}/{units.solou.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.solou.mp}/{units.solou.max_mp} MP'))))

    if units.chili.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.chili.name, units.chili.hp,
              units.chili.max_hp, units.chili.mp,
              units.chili.max_mp, units.chili.lvl,
              ', '.join([x.title() for x in units.chili.status_ail]),
              pad1=' '*(first_padding - len(units.chili.name)),
              pad2=' '*(second_padding - len(f'{units.chili.hp}/{units.chili.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.chili.mp}/{units.chili.max_mp} MP'))))

    if units.chyme.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.chyme.name, units.chyme.hp,
              units.chyme.max_hp, units.chyme.mp,
              units.chyme.max_mp, units.chyme.lvl,
              ', '.join([x.title() for x in units.chyme.status_ail]),
              pad1=' '*(first_padding - len(units.chyme.name)),
              pad2=' '*(second_padding - len(f'{units.chyme.hp}/{units.chyme.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.chyme.mp}/{units.chyme.max_mp} MP'))))

    if units.parsto.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.parsto.name, units.parsto.hp,
              units.parsto.max_hp, units.parsto.mp,
              units.parsto.max_mp, units.parsto.lvl,
              ', '.join([x.title() for x in units.parsto.status_ail]),
              pad1=' '*(first_padding - len(units.parsto.name)),
              pad2=' '*(second_padding - len(f'{units.parsto.hp}/{units.parsto.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.parsto.mp}/{units.parsto.max_mp} MP'))))

    if units.adorine.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.adorine.name, units.adorine.hp,
              units.adorine.max_hp, units.adorine.mp,
              units.adorine.max_mp, units.adorine.lvl,
              ', '.join([x.title() for x in units.adorine.status_ail]),
              pad1=' '*(first_padding - len(units.adorine.name)),
              pad2=' '*(second_padding - len(f'{units.adorine.hp}/{units.adorine.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.adorine.mp}/{units.adorine.max_mp} MP'))))

    if units.ran_af.enabled:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              units.ran_af.name, units.ran_af.hp,
              units.ran_af.max_hp, units.ran_af.mp,
              units.ran_af.max_mp, units.ran_af.lvl,
              ', '.join([x.title() for x in units.ran_af.status_ail]),
              pad1=' '*(first_padding - len(units.ran_af.name)),
              pad2=' '*(second_padding - len(f'{units.ran_af.hp}/{units.ran_af.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{units.ran_af.mp}/{units.ran_af.max_mp} MP'))))

    # Monster Stats
    for each_monster in m_list:
        print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
              each_monster.name, each_monster.hp,
              each_monster.max_hp, each_monster.mp,
              each_monster.max_mp, each_monster.lvl,
              ', '.join([x.title() for x in each_monster.status_ail]),
              pad1=' '*(first_padding - len(each_monster.name)),
              pad2=' '*(second_padding - len(f'{each_monster.hp}/{each_monster.max_hp} HP')),
              pad3=' '*(third_padding - len(f'{each_monster.mp}/{each_monster.max_mp} MP'))))

    print('-'*save_load.divider_size)
