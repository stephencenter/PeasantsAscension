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
import magic
import world
import bosses
import pets
import sounds
import ascii_art

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam

# input = test_input

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Creates a lambda function that strips all non-numeric characters
# This fixes some (possible) problems later on
only_num = lambda x: re.compile(r'[^\d]+').sub('', x)

monster = ''
player = ''
misc_vars = ''
position = ''

vowels = 'AEIOU'
temp_stats = ''
ability_used = False

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


def setup_vars():
    global position
    global misc_vars
    global player
    global monster

    monster = monsters.monster
    player = main.player
    misc_vars = main.misc_vars
    position = main.position


def update_stats():
    # Forces stats to return to normal when battle is finished
    global temp_stats
    temp_stats = {'attk': _c(player.attk), 'm_attk': _c(player.m_attk),
                  'p_attk': _c(player.p_attk), 'p_dfns': _c(player.p_dfns),
                  'dfns': _c(player.dfns), 'm_dfns': _c(player.m_dfns),
                  'spd': _c(player.spd), 'evad': _c(player.evad),
                  'm_ispoisoned': False, 'turn_counter': 0}


def player_choice():
    print("""\
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""")

    while True:
        move = only_num(input("Input [#]: "))

        if move.isdigit() and int(move) in range(1, 6):
            # Only return if "move" refers to a valid move
            if temp_stats['spd'] > monster.spd:
                print('-'*25)
            return move


def battle_system(is_boss=False, ambush=False):
    global ability_used

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
        if random.randint(0, 1):
            song = 'Music/Jumpshot.ogg'

        else:
            song = 'Music/Ruari 8-bit Battle.ogg'

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[monster.monster_name] % '')

        if any(map(monster.name.startswith, vowels)):  # Remember to use proper grammar!
            a_an = 'An '
        else:
            a_an = 'A '

        if ambush:
            print('{0}{1} ambushed you while you were resting!'.format(
                a_an, monster.name))
            time.sleep(0.35)

            while msvcrt.kbhit():
                msvcrt.getwch()

        else:
            print('{0}{1} suddenly appeared out of nowhere!'.format(
                a_an, monster.name))
            time.sleep(0.35)

            while msvcrt.kbhit():
                msvcrt.getwch()

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    update_stats()

    ability_used = False

    while player.hp > 0 and monster.hp > 0:  # Continue the battle until someone dies
        if player.hp <= 0.20*misc_vars["hp_p"]:
            print("Warning: HP is low, heal as soon as possible!")
            sounds.health_low.play()

        bat_stats()

        if player.status_ail == 'asleep':
            if not random.randint(0, 2):
                sounds.buff_spell.play()
                print('\n-Player Turn-')
                input('You start to regain conciousness! | Press enter/return ')

                player.status_ail = 'none'
                bat_stats()
                move = player_choice()

            else:
                print('-Player Turn-')
                print(ascii_art.player_art["Asleep"] % "{0} is asleep!\n ".format(player.name))
                input("You're too tired to do anything! | Press Enter/Return ")
                move = ''
        else:
            move = player_choice()

        # var is how much less/more the attacks will deal than normal.
        # This makes the battle less predictable and more interesting.
        var = random.randint(-1, 1)

        # m_var is the same as var, except it applies to the enemy instead of the player
        m_var = random.randint(-1, 1)

        # If dodge is in a certain range, the attack will miss
        dodge = random.randint(0, 250)
        m_dodge = random.randint(0, 250)

        if move == '4':  # Use the Battle Inventory

            if battle_inventory() and monster.hp > 0:
                input('\nPress Enter/Return ')
                monster.enemy_turn(m_var, m_dodge)

                if player.hp > 0:
                    input('\nPress Enter/Return ')

            continue

        elif move == '5':

            if run_away():  # Attempt to run.
                # If it succeeds, end the battle without giving the player a reward
                print('-'*25)
                pygame.mixer.music.load(position['reg_music'])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(main.music_vol)

                return

            # If it fails, the enemy will attack you and skip your turn
            monster.enemy_turn(m_var, m_dodge)

            if player.hp > 0:
                input('\nPress Enter/Return ')

            continue

        # The player goes first if they have a higher speed
        elif (temp_stats['spd'] > monster.spd or move == '2' or move == '3') \
                and player.status_ail != 'asleep':

            if move and player_turn(var, dodge, move) and monster.hp > 0:
                input('\nPress Enter/Return ')
                monster.enemy_turn(m_var, m_dodge)

                if player.hp > 0:
                    input('\nPress Enter/Return ')

            continue

        # Otherwise, the monster will go first
        else:
            if monster.spd < temp_stats['spd'] and player.status_ail != 'asleep':
                print('-'*25)

            monster.enemy_turn(m_var, m_dodge)

            if player.hp > 0:
                if player.status_ail != 'asleep':
                    input('\nPress Enter/Return ')
                    move = player_choice()
                    player_turn(var, dodge, move)

                if monster.hp > 0:
                    input('\nPress Enter/Return ')

    else:
        if after_battle(is_boss) != 'dead':
            print('-'*25)


def player_turn(var, dodge, move):
    global player
    global monster

    while True:
        # "2" refers to magic, which will print this later
        if move != '2':
            print('\n-Player Turn-')

        if move == '1':
            print(ascii_art.player_art[player.class_.title()] %
                  "{0} is making a move!\n".format(player.name))

            if inv_system.equipped['weapon'].type_ in ['melee', 'magic']:
                sounds.sword_slash.play()
                print('You begin to fiercely attack the {0} using your {1}...'.format(
                    monster.name, str(inv_system.equipped['weapon'])))

            # Ranged weapons aren't swung, so play a different sound effect
            else:
                sounds.aim_weapon.play()
                print('You aim carefully at the {0} using your {1}...'.format(
                    monster.name, str(inv_system.equipped['weapon'])))

            time.sleep(0.75)

            while msvcrt.kbhit():
                msvcrt.getwch()

            if dodge in range(monster.evad, 250):
                dealt = player.player_damage(var)
                monster.hp -= dealt
                sounds.enemy_hit.play()
                print('Your attack connects with the {0}, dealing {1} damage!'.format(
                    monster.name, dealt))

            else:
                sounds.attack_miss.play()
                print('The {0} dodges your attack with ease!'.format(monster.name))

        elif move == '2':
            if not magic.pick_cat(var, dodge):
                return False

        elif move == '3':
            if not class_ability():
                return False

        else:
            return False

        if not isinstance(inv_system.equipped['pet'], pets.Steed) \
                and inv_system.equipped['pet'] != '(None)' \
                and monster.hp > 0:

            input('\nPress Enter/Return')
            print("\n-Pet Turn-")
            inv_system.equipped['pet'].use_ability()

        # Check to see if the player is poisoned
        if player.status_ail == 'poisoned' and monster.hp > 0:
            if random.randint(0, 3):
                time.sleep(0.5)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                sounds.poison_damage.play()

                poison_damage = int(math.ceil(misc_vars['hp_p']/10))
                print('You took poison damage! (-{0} HP)'.format(poison_damage))
                player.hp -= poison_damage

                if player.hp <= 0:
                    break

            else:
                time.sleep(0.5)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                sounds.buff_spell.play()
                input('You start to feel better! | Press enter/return ')
                player.status_ail = 'none'

        # Check to see if the player is silenced
        elif player.status_ail == 'silenced':
            if not random.randint(0, 3):

                time.sleep(0.5)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                sounds.buff_spell.play()

                input('You find yourself able to speak again! | Press enter/return ')
                player.status_ail = 'none'

        return True


def after_battle(is_boss):  # Assess the results of the battle
    global player

    update_stats()  # Reset non-hp/mp stats to the way they were before battle

    print('-'*25)

    while True:
        # If the monster wins...
        if monster.hp > 0 >= player.hp:
            pygame.mixer.music.load('Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)

            print('Despite your best efforts, the {0} has bested you. You are dead.'.format(
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

                    player.hp = int(misc_vars['hp_p']/1.5)
                    player.mp = int(misc_vars['mp_p']/1.5)

                    pygame.mixer.music.load(position['reg_music'])
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
                gold = int(random.randint(2, 3)*monster.lvl - player.lvl)

                if gold <= 0:
                    gold = random.randint(1, 2)
                experience = int(math.ceil((monster.lvl + 1.5 + player.ext_exp)/1.75))

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

            # Give the Player their GP
            misc_vars['gp'] += gold + player.ext_gol
            print("You've gained {0} GP!".format(gold), end='')
            sounds.item_pickup.play()
            input(' | Press Enter/Return ')

            # Give the Player their XP
            player.exp += experience
            print("You've gained {0} XP!".format(experience), end='')
            sounds.item_pickup.play()
            input(' | Press Enter/Return ')

            # If the monster has items, give them to the player
            if monster.items:
                cat = monster.items.cat
                inv_system.inventory[cat].append(_c(monster.items))

                print('The {0} dropped a {1}! You decide to take {2}.'.format(
                      monster.name, str(monster.items),
                      'them' if str(monster.items).endswith('s') else 'it'), end='')  # Grammar!!

                sounds.item_pickup.play()
                input(' | Press Enter/Return ')

            # Check to see if the player gained any levels
            player.level_up()

            pygame.mixer.music.load(position['reg_music'])
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(main.music_vol)
            pygame.mixer.music.set_volume(main.music_vol)

            return

        # If the battle is a tie, the player wins
        elif player.hp <= 0 and monster.hp <= 0:
            player.hp = 1


def class_ability():
    # Class abilities are special abilities only available to characters of certain classes.
    # Their purpose is to help make the characters more diverse, as well as encourage more
    # strategy being used.

    global ability_used

    if ability_used:
        # You can only use your ability once per battle.
        print('You feel drained, and are unable to call upon your class ability again.')
        return False

    else:
        ability_used = True

    print(ascii_art.player_art[player.class_.title()] %
          "{0} is making a move!\n".format(player.name))

    print("You use the knowledge you've gained to unleash your class ability!")

    if player.class_ == 'ranger':
        # The ranger class identifies their enemy and prints their stats.
        # This is really useful for defeating bosses, which are often weak to
        # certain types and elements of attacks.
        print('As a Ranger, you identify your enemy and meditate!')
        input("Press Enter/Return to view your enemy's stats ")

        print('-'*25)
        print("{0}'s STATS:".format(monster.name.upper()))

        print("""Attack: {0} | M. Attack: {1} | P. Attack: {2} | Speed: {3}
Defense: {4} | M. Defense: {5} | P. Defense: {6} | Evasion: {7}
Element: {8} | Elemental Weakness: {9}""".format(
            monster.attk, monster.m_attk, monster.p_attk, monster.spd,
            monster.dfns, monster.m_dfns, monster.p_dfns, monster.evad,
            monster.element.title(),
            {'fire': 'Water',
             'water': 'Electric',
             'electric': 'Earth',
             'earth': 'Grass',
             'grass': 'Wind',
             'wind': 'Ice',
             'ice': 'Fire',
             'none': 'None',
             'life': 'Death',
             'death': 'Life'}[monster.element]))

        player.hp += 3
        player.mp += 3

        if player.hp > misc_vars['hp_p']:
            player.hp -= (player.hp - misc_vars['hp_p'])
        if player.mp > misc_vars['mp_p']:
            player.mp -= (player.mp - misc_vars['mp_p'])

        return True

    elif player.class_ == 'warrior':
        player.hp += 10
        temp_stats['dfns'] += 3
        temp_stats['m_dfns'] += 3
        temp_stats['p_dfns'] += 3
        print('As a Warrior, you channel your inner-strength and increase your defense greatly!')

        if player.hp > misc_vars['hp_p']:
            player.hp -= (player.hp - misc_vars['hp_p'])
        if player.mp > misc_vars['mp_p']:
            player.mp -= (player.mp - misc_vars['mp_p'])

        return True

    elif player.class_ == "mage":
        player.mp = _c(misc_vars['mp_p'])
        temp_stats['m_attk'] += 2
        temp_stats['m_dfns'] += 2
        print('As a Mage, you focus intently and sharply increase your magical prowess!')

        return True

    elif player.class_ == "assassin":
        temp_stats['m_ispoisoned'] = True
        print('As an Assassin, you discreetly inject poison into your enemy!')

        return True


def run_away():
    print('You start to run away from the {0}...'.format(monster.name))

    sounds.foot_steps.play()
    time.sleep(0.75)

    while msvcrt.kbhit():
        msvcrt.getwch()

    if bool(player.spd > monster.spd) != bool(player.evad > monster.evad):  # 75% chance of success
        if random.randint(0, 3):
            print('You manage to escape from the {0}!'.format(monster.name))
            return True

        else:
            print('Your attempt to escape failed!')
            input("\nPress Enter/Return")
            return False

    elif player.spd > monster.spd and player.evad > monster.evad:  # 90% chance of success
        if random.randint(0, 9):
            print('You manage to escape from the {0}!'.format(monster.name))
            return True

        else:
            print('Your attempt to escape failed!')
            input("\nPress Enter/Return")
            return False

    else:  # 50% chance of success
        if random.randint(0, 1):
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
        print('Battle Inventory: \n      ' + '\n      '.join(
              ['[' + str(x + 1) + '] ' + str(y)
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
            item.use_item()
            return True


# Makes sure that the player and monster never have negative stats,
# and then display their stats after they're fixed
def bat_stats():
    global player
    global monster

    if player.hp < 0:
        player.hp = 0
    if monster.hp < 0:
        monster.hp = 0
    if player.hp > misc_vars['hp_p']:
        player.hp -= (player.hp - misc_vars['hp_p'])
    if monster.hp > misc_vars['hp_m']:
        monster.hp -= (monster.hp - misc_vars['hp_m'])
    if player.mp < 0:
        player.mp = 0
    if monster.mp < 0:
        monster.mp = 0
    if player.mp > misc_vars['mp_p']:
        player.mp -= (player.mp - misc_vars['mp_p'])
    if monster.mp > misc_vars['mp_m']:
        monster.mp -= (monster.mp - misc_vars['mp_m'])
    print('-'*25)

    pet = inv_system.equipped['pet']

    # Sorry this section is kinda complicated. Basically, this calculates the length of certain
    # strings to see how much padding (extra spaces) is needed to make things line up.
    if pet != '(None)':
        first_padding = len(max([''.join([player.name, "'s ", pet.name]),
                                 pet.name, monster.name], key=len))

        second_padding = len(max(['{0}/{1} HP'.format(player.hp, misc_vars['hp_p']),
                                  'LVL: {0}'.format(pet.level)
                                  if isinstance(pet, pets.Fighter)
                                  else '{0}/{1}'.format(pet.mana, pet.max_m)
                                  if isinstance(pet, pets.Healer)
                                  else '',
                                  '{0}/{1} HP'.format(monster.mp, misc_vars['mp_p'])], key=len))

    else:
        first_padding = len(max([player.name, monster.name], key=len))

        second_padding = len(max(['{0}/{1} HP'.format(player.hp, misc_vars['hp_p']),
                                  '{0}/{1} HP'.format(monster.mp, misc_vars['mp_p'])], key=len))

    third_padding = len(max(['{0}/{1} MP'.format(player.mp, misc_vars['mp_p']),
                             '{0}/{1} MP'.format(monster.mp, misc_vars['mp_m'])]))

    # Player Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5} | STATUS: {6}".format(
          player.name, player.hp,
          misc_vars['hp_p'], player.mp,
          misc_vars['mp_p'], player.lvl,
          player.status_ail.title(),
          pad1=' '*(first_padding - len(player.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(player.hp, misc_vars['hp_p']))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(player.mp, misc_vars['mp_p'])))))

    # Monster Stats
    print("{0}{pad1} | {1}/{2} HP {pad2}| {3}/{4} MP {pad3}| LVL: {5}".format(
          monster.name, monster.hp,
          misc_vars['hp_m'], monster.mp,
          misc_vars['mp_m'], monster.lvl,
          pad1=' '*(first_padding - len(monster.name)),
          pad2=' '*(second_padding - len('{0}/{1} HP'.format(monster.mp, misc_vars['mp_p']))),
          pad3=' '*(third_padding - len('{0}/{1} MP'.format(monster.mp, misc_vars['mp_m'])))))

    # Pet Stats
    if pet:
        if isinstance(pet, pets.Healer):
            print("{0}'s {1}{pad1} | {2}/{3} MP {pad2}| LVL: {4}".format(
                player.name, pet.name, pet.mana, pet.max_m, pet.level,
                pad1=' '*(first_padding - len(''.join([player.name, "'s ", pet.name]))),
                pad2=' '*(second_padding - len('{0}/{1}'.format(pet.mana, pet.max_m)))))

        elif isinstance(pet, pets.Fighter):
            print("{0}'s {1}{pad1} | LVL: {2} {pad2}| STATUS: {3}".format(
                player.name, pet.name, pet.level, 'Incapacitated' if pet.rt else 'None',
                pad1=' '*(first_padding - len(''.join([player.name, "'s ", pet.name]))),
                pad2=' '*(second_padding - len('LVL: {0}'.format(pet.level)))))

    print('-'*25)
