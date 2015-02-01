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
                  'dfns': _c(player.dfns), 'm_dfns': _c(player.m_dfns),
                  'spd': _c(player.spd), 'evad': _c(player.evad),
                  'status_effect': 'none'}


def player_choice():
    while True:
        move = only_num(
            input('1: Attack; 2: Use Magic; 3: Wait; 4. Use Items; 5: Run | Input #(1-5): ')
        )
        if move.isdigit() and int(move) in range(1, 6):
        # Only return if "move" refers to a valid move
            return move


def battle_system(is_boss=False, ambush=False):
    if is_boss:  # Bosses have different battle music than normal enemies
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(main.music_vol)

        print(ascii_art.monster_art[monster.monster_name] % '')
        print('The legendary {0} has awoken!'.format(monster.name))

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
            print('{0}{1} ambushed you while you were resting!'.format(a_an, monster.name))
        else:
            print('{0}{1} suddenly appeared out of nowhere!'.format(a_an, monster.name))

    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle
    update_stats()

    while player.hp > 0 and monster.hp > 0:  # Continue the battle until someone dies
        if player.hp <= 0.20*misc_vars["hp_p"]:
            print("Warning: HP is low, heal as soon as possible!")
            sounds.health_low.play()

        if temp_stats['status_effect'] == 'asleep':
            is_woken_up = not random.randint(0, 2)
        else:
            is_woken_up = False

        # Display the Player and Monster's stats
        if not is_woken_up:
            bat_stats()

        # Check to see if the player is asleep
        if temp_stats['status_effect'] == 'asleep':

            if is_woken_up:
                print('\n-Player Turn-')
                print('You finally wake up!')

                temp_stats['status_effect'] = 'none'
                bat_stats()
                move = player_choice()

            else:
                print('-Player Turn-')
                print(ascii_art.player_art["Asleep"] % "{0} is asleep!".format(player.name))
                print("You're too tired to do anything!")
                input('\nPress Enter/Return')
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
        elif (temp_stats['spd'] > monster.spd or move == '2') \
                and temp_stats['status_effect'] != 'asleep':

            if move and player_turn(var, dodge, move) and monster.hp > 0:
                input('\nPress Enter/Return ')
                monster.enemy_turn(m_var, m_dodge)

                if player.hp > 0:
                    input('\nPress Enter/Return ')

            continue

        # Otherwise, the monster will go first
        else:
            monster.enemy_turn(m_var, m_dodge)

            if player.hp > 0:
                if temp_stats['status_effect'] != 'asleep':
                    input('\nPress Enter/Return ')
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
            print(ascii_art.player_art[player.class_.title()] %
                  "{0} is making a move!\n".format(player.name))

            print('You wait for your turn to end while you gather your strength.')
            player.hp += 2
            player.mp += 2

            if player.hp > misc_vars['hp_p']:
                player.hp -= (player.hp - misc_vars['hp_p'])
            if player.mp > misc_vars['mp_p']:
                player.mp -= (player.mp - misc_vars['mp_p'])

        else:
            return False

        if not isinstance(player.current_pet, pets.Steed) \
                and player.current_pet \
                and monster.hp > 0:

            input('\nPress Enter/Return')
            print("\n-Pet Turn-")
            player.current_pet.use_ability()

        # Check to see if the player is poisoned
        if temp_stats['status_effect'] == 'poisoned':
            if random.randint(0, 3):
                poison_damage = int(misc_vars['hp_p']/10)

                print('You took poison damage! (-{0} HP)'.format(poison_damage))

                player.hp -= poison_damage

                if player.hp <= 0:
                    break
            else:
                print('You start to feel better!')
                temp_stats['status_effect'] = 'none'

        # Check to see if the player is silenced
        elif temp_stats['status_effect'] == 'silenced':
            if not random.randint(0, 3):
                print('You find yourself able to speak again!')
                temp_stats['status_effect'] = 'none'

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


def run_away():
    print('You start to run away from the {0}...'.format(monster.name))

    sounds.foot_steps.play()
    time.sleep(0.75)

    # There's a 50% chance that running will fail. This is lowered/raised
    # based on the player's evasion stat. If the player has an evasion stat
    # of 120+, they always succeed.
    if random.randint(1, 100) in range(50, (101 - int(player.evad/2))) and player.evad < 120:
        print('Your attempt to escape failed!')
        input("\nPress Enter/Return")
        return False

    else:
        print('You manage to escape from the {0}!'.format(monster.name))
        return True


def battle_inventory():
    # The player can use items from the "consum" category of their inventory during battles.
    while True:
        print('-'*25)
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

    # Player Stats
    print("{0}: {1}/{2} HP | {3}/{4} MP | LVL: {5} | STATUS: {6}".format(
          player.name, player.hp,
          misc_vars['hp_p'], player.mp,
          misc_vars['mp_p'], player.lvl,
          temp_stats['status_effect'].title()))

    # Pet Stats
    pet = player.current_pet
    if pet:
        if isinstance(pet, pets.Healer):
            print("{0}'s {1}: {2}/{3} MP | LVL: {4}".format(
                player.name, pet.name, pet.mana, pet.max_m, pet.level))

        elif isinstance(pet, pets.Fighter):
            print("{0}'s {1}: | STATUS:  {2} | LVL: {3}".format(
                player.name, pet.name, 'Incapacitated' if pet.rt else 'Normal', pet.level))

    # Monster Stats
    print("{0}: {1}/{2} HP | {3}/{4} MP | LVL: {5}".format(
          monster.name, monster.hp,
          misc_vars['hp_m'], monster.mp,
          misc_vars['mp_m'], monster.lvl))

    print('-'*25)
