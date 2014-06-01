import sys
import random
import time
import math
from copy import copy as _c

import pygame

import inv_system
import monsters
import magic
import world
import bosses
import pets
import sounds


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

monster = ''
player = ''
static = ''
position = ''

vowels = 'AEIOU'
temp_stats = ''

if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]


def setup_vars():
    global position
    global static
    global player
    global monster

    monster = monsters.monster
    player = main.player
    static = main.static
    position = main.position


def update_stats():  # Forces stats to return to normal when battle is finished
    global temp_stats
    temp_stats = {'attk': _c(player.attk), 'm_attk': _c(player.m_attk),
                  'dfns': _c(player.dfns), 'm_dfns': _c(player.m_dfns),
                  'spd': _c(player.spd), 'evad': _c(player.evad)}


def player_choice():
    while True:
        move = input('1: Attack; 2: Use Magic; 3: Wait; 4. Use Items; 5: Run | Input #(1-5): ')
        if move.isdigit() and int(move) in range(1, 6):
        # Only return if "move" refers to a valid move
            return move


def battle_system(is_boss=False):
    if is_boss:  # Bosses have different battle music than normal enemies
        pygame.mixer.music.load('Music/Terrible Tarantuloid.ogg')
        pygame.mixer.music.play(-1)
        print('The legendary {0} has awoken!'.format(monster.name))
    else:
        pygame.mixer.music.load('Music/Jumpshot.ogg')
        pygame.mixer.music.play(-1)

        if monster.name[0] in vowels:
        # Remember to use proper grammar!
            a_an = 'An '
        else:
            a_an = 'A '

        print('{0}{1} suddenly appeared out of nowhere!'.format(a_an, monster.name))
    time.sleep(0.5)
    update_stats()
    # Record the player's non-hp/mp stats (e.g. defense)
    # So they can go back to normal after the battle

    while player.hp > 0 and monster.hp > 0:  # Continue the battle until someone dies

        bat_stats()
        # First, display the Player and Monster's stats

        move = player_choice()
        # Second, get the player's decision on moves

        var = random.randint(-1, 1)
        # var is how much less/more the attacks will deal than normal.
        # This makes the battle less predictable and more interesb
        # ting.

        dodge = random.randint(0, 250)
        # If dodge is in a certain range, the attack will miss

        if move == '4':  # Use the Battle Inventory
            if battle_inventory() and monster.hp > 0:
                input('\nPress Enter/Return ')
                enemy_turn(var, dodge)
                if player.hp > 0:
                    input('\nPress Enter/Return ')
            continue

        elif move == '5':
            run = run_away()  # Attempt to run...
            if run:
                # If it succeeds, end the battle without giving the player a reward
                print('-'*25)
                pygame.mixer.music.load(position['reg_music'])
                pygame.mixer.music.play(-1)
                return
            enemy_turn(var, dodge)
            if player.hp > 0:
                input('\nPress Enter/Return ')
            # If it fails, the enemy will attack you and skip your turn
            continue

        elif temp_stats['spd'] > monster.spd or move == '2':
            # The player goes first if they have a higher speed
            if player_turn(var, dodge, move) and monster.hp > 0:
                input('\nPress Enter/Return ')
                enemy_turn(var, dodge)
                if player.hp > 0:
                    input('\nPress Enter/Return ')
            continue

        else:
            # Otherwise, the monster will go first
            enemy_turn(var, dodge)
            if player.hp > 0:
                input('\nPress Enter/Return ')
                player_turn(var, dodge, move)
                input('\nPress Enter/Return ')

    else:
        if after_battle(is_boss) != 'dead':
            print('-'*25)


def player_turn(var, dodge, move):
    global player
    global monster
    while True:
        print('\n-Player Turn-') if move != '2' else ''
        # "2" refers to magic, which will print this later

        if move == '1':  # Attack
            if inv_system.equipped['weapon'].type_ in ['melee', 'magic']:
                sounds.sword_slash.play()
                print('You begin to fiercely attack the {0} using your {1}...'.format(
                    monster.name, str(inv_system.equipped['weapon'])))
            else:
                sounds.aim_weapons.play()
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
                print('The {0} dodges your attack with ease!'.format(monster.name))

        elif move == '2':  # Magic
            magic.pick_cat(var, dodge)

        elif move == '3':  # Wait
            print('You wait for your turn to end while you gather your strength.')
            player.hp += 2
            player.mp += 2

        else:
            return False
        player.current_pet.use_ability() if player.current_pet else ''
        return True


def enemy_turn(var, dodge):
    # This is the Enemy's AI.
    global player
    global monster
    print('\n-Enemy Turn-')
    if monster.hp <= int(static['hp_m']/4) and monster.mp >= 5:
        # Magic heal
        sounds.magic_healing.play()
        heal = int(((monster.m_attk + monster.m_dfns)/2) + monster.lvl/2)
        if heal < 5:
            heal = 5
        monster.hp += heal
        monster.mp -= 5
        print('The {0} casts a healing spell!'.format(monster.name))

    elif monster.attk >= monster.m_attk:
        # Physical Attack
        monster.monst_attk(var, dodge)

    elif int((monster.dfns + monster.m_dfns)/2) <= int(player.lvl/3):
        # Defend
        monster.dfns += random.randint(1, 2)
        monster.m_dfns += random.randint(1, 2)
        print("The {0} assumes a more defensive stance! (+DEF, +M'DEF)".format(monster.name))

    elif monster.m_attk >= monster.attk and monster.mp >= 2:
        # Magic Attack
        sounds.magic_attack.play()
        print('The {0} is attempting to cast a strange spell...'.format(monster.name))
        time.sleep(0.75)
        if dodge in range(temp_stats['evad'], 250):
            dealt = monster.monst_magic(var)
            player.hp -= dealt
            sounds.enemy_hit.play()
            print("The {0}'s spell succeeds, and deals {1} damage to you!".format(monster.name, dealt))
        else:
            print("The spell misses you by a landslide!")
        monster.mp -= 2

    else:
        monster.monst_attk(var, dodge)


def after_battle(is_boss):  # Assess the results of the battle
    global player
    update_stats()  # Reset non-hp/mp stats to the way they were before battle
    print('-'*25)
    while True:
        if monster.hp > 0 >= player.hp:
            # If the monster wins...
            pygame.mixer.music.load('Music/Power-Up.ogg')
            pygame.mixer.music.play(-1)
            print('Despite your best efforts, the {0} has bested you. You are dead.'.format(monster.name))
            print('-'*25)
            while True:
                y_n = input('Do you wish to continue playing? | Yes or No: ')
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n in ['yes', 'y', 'yeah']:
                    # If you die, you return to the last town visited or 0'N, 0'E
                    # if you haven't been to a town yet.
                    world.back_to_coords()
                    player.hp = int(static['hp_p']/2)
                    player.mp = int(static['mp_p']/2)
                    pygame.mixer.music.load(position['reg_music'])
                    pygame.mixer.music.play(-1)
                    return 'dead'
                elif y_n in ['no', 'n', 'nope']:
                    sys.exit()

        elif monster.hp <= 0 < player.hp:
            # If the player wins...
            if not is_boss:
                # Only do the following if the player defeated a
                # normal enemy, and not a boss
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

                gold = monster.gold + player.ext_gol
                # Bosses drop a set amount of gold...
                experience = monster.experience
                # ...and exp

                try:
                    # Check to see if the boss does anything special at death
                    monster.upon_defeating()
                except AttributeError:
                    pass

            static['gp'] += gold + player.ext_gol
            player.exp += experience
            print("You've gained {0} GP!".format(gold))
            print("You've gained {0} experience point{1}!".format(
                experience, 's' if experience > 1 else ''))
            # Correct grammar is important

            if monster.items:
                # If the monster has items, give them to the player
                cat = monster.items.cat
                inv_system.inventory[cat].append(_c(monster.items))
                print('The {0} drops a {1}! You put it in your inventory for safe keeping.'.format(
                      monster.name, str(monster.items)))

            player.level_up()
            # Check to see if the player gained any levels

            pygame.mixer.music.load(position['reg_music'])
            pygame.mixer.music.play(-1)
            return
        elif player.hp <= 0 and monster.hp <= 0:
            # If the battle is a tie, the player wins
            player.hp = 1


def run_away():
    print('You begin to flee.')
    if random.randint(1, 100) in range(50, (101 - int(player.evad/2))) and player.evad < 100:
        # There's a 50% change that running will fail
        print('Your attempt to escape failed!')
        return False
    else:
        print('You manage to escape from the {0}!'.format(monster.name))
        return True


def battle_inventory():
    # The player can use certain items during battle
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
            except (TypeError, ValueError):
                try:
                    item = item.lower()
                except AttributeError:
                    continue
                if item in ['e', 'x', 'exit', 'c', 'cancel', 'b', 'back']:
                    return False
                else:
                    continue
            try:
                item = inv_system.inventory['consum'][item]
            except IndexError:
                continue
            print('\n-Player Turn-')
            item.consume_item()
            return True


def bat_stats():
    # Makes sure that the player and monster never have negative stats,
    # and then display their stats after they're fixed
    global player
    global monster
    if player.hp < 0:
        player.hp = 0
    if monster.hp < 0:
        monster.hp = 0
    if player.hp > static['hp_p']:
        player.hp -= (player.hp - static['hp_p'])
    if monster.hp > static['hp_m']:
        monster.hp -= (monster.hp - static['hp_m'])
    if player.mp < 0:
        player.mp = 0
    if monster.mp < 0:
        monster.mp = 0
    if player.mp > static['mp_p']:
        player.mp -= (player.mp - static['mp_p'])
    if monster.mp > static['mp_m']:
        monster.mp -= (monster.mp - static['mp_m'])
    print('-'*25)

    # Player Stats
    print('{0}: {1}/{2} HP | {3}/{4} MP  LVL: {5}'.format(
          player.name, player.hp,
          static['hp_p'], player.mp,
          static['mp_p'], player.lvl))
    # Pet Stats
    pet = player.current_pet
    if pet:
        if isinstance(player.current_pet, pets.Healer):
            print("{0}'s {1}: {2}/{3} MP LVL: {4}".format(player.name, pet.name, pet.mana, pet.max_m, pet.level))
    # Monster Stats
    print('{0}: {1}/{2} HP | {3}/{4} MP  LVL: {5}'.format(
          monster.name, monster.hp,
          static['hp_m'], monster.mp,
          static['mp_m'], monster.lvl))
    print('-'*25)
