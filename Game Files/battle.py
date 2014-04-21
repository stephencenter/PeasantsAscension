import sys
import math
import random
import monsters
import inv_system
import magic
import world
import winsound
from copy import copy as _c

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

    player = main.player
    static = main.static
    position = main.position
    monster = monsters.monster

def update_stats(): # Forces stats to be returned to normal when battle is finished
    global temp_stats
    temp_stats = {'attk':_c(player.attk), 'm_attk':_c(player.m_attk), 'dfns':_c(player.dfns),
                  'evad':_c(player.evad), 'm_dfns':_c(player.m_dfns), 'spd':_c(player.spd)}

def battle_system():
    winsound.PlaySound(None, winsound.SND_ASYNC)
    winsound.PlaySound('Music\\Jumpshot.wav', winsound.SND_ASYNC | winsound.SND_LOOP)

    if monster.name[0] in vowels: # Remember to use proper grammar!
        a_an = 'An '
    else:
        a_an = 'A '

    print('-'*25)
    print('%s%s suddenly appeared out of nowhere!' % (a_an, monster.name))
    update_stats()

    while player.hp > 0 and monster.hp > 0: # Continue the battle until someone dies
        bat_stats() # First, display the Player and Monster's stats
        move = player_choice() # Second, get the player's decision on moves

        var = random.randint(-1, 1) # Var is how much less/more the attacks will deal than normal
                                    # This makes the battle less predictable

        dodge = random.randint(0, 250) # If dodge is in a certain range, the attack will miss

        if move == '4':
            run = run_away() # Attempt to run...
            if run: # If it succeeds, end the battle without giving the player a reward
                print('-'*25)
                winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_LOOP)
                winsound.PlaySound(position['reg_music'], winsound.SND_ASYNC | winsound.SND_LOOP)
                return

            enemy_turn(var, dodge) # If it fails, the enemy will attack you and skip your turn
            continue

        if monster.spd > player.spd: # If the monster is faster, it goes first...
            enemy_turn(var, dodge)
            if player.hp > 0:
                player_turn(var, dodge, move)

        else: # Otherwise, the player will go first
            player_turn(var, dodge, move)
            if monster.hp > 0:
                enemy_turn(var, dodge)
    else:
        after_battle()
        print('-'*25)

def player_choice():
    while True:
        move = input('1: Attack; 2: Use Magic; 3: Wait; 4: Run | Input #(1-4): ')
        if move.isdigit() and int(move) in range(1, 5): # Only return if "move" refers to a valid move
            return move

def player_turn(var, dodge, move):
    global player
    global monster
    while True:
        if move != '2': # "2" refers to magic, which will print this later
            print()
            print('-Player Turn-')

        if move == '1': # Attack
            print('You begin to fiercly attack the %s using your %s!' % (monster.name, str(inv_system.equipped['weapon'])))
            if dodge in range(monster.evad, 250):
                dealt = player.player_damage(var)
                monster.hp -= dealt
                print('Your attack connects with the %s, dealing %s damage!' % (monster.name, dealt))
            else:
                print('The %s dodges your attack with ease!' % (monster.name))
            return

        elif move == '2': # Magic
            if magic.pick_cat(var, dodge):
                return
            else:
                move = input('1: Attack; 2: Use Magic; 3: Wait; 4: Run | Input #(1-4): ')
                if move.isdigit() and int(move) in range(1, 5): # Yes, it's redundant, but it works.
                    continue

        elif move == '3': # Wait
            print('You passively wait for your turn to end while you gather your strength. (+3 HP, +2 MP)')
            player.hp += 3
            player.mp += 2
            return

def enemy_turn(var, dodge): # This is the Enemy's AI.
                            # (I need to implement this into the "Monster" class later)
    global player
    global monster
    print()
    print('-Enemy Turn-')

    if monster.hp <= int(static['hp_m']/4) and monster.mp >= 5: # Magic heal
        heal = int(((monster.m_attk + monster.m_dfns)/2) + monster.lvl/2)
        if heal < 5:
            heal = 5
        monster.hp += heal
        monster.mp -= 5
        print('The %s casts a healing spell!' % (monster.name))

    elif monster.attk >= monster.m_attk: # Physical Attack
        monster.monst_attk(var, dodge)

    elif int((monster.dfns + monster.m_dfns)/2) <= int(player.lvl/3): # Defend
        monster.dfns += random.randint(1, 2)
        monster.m_dfns += random.randint(1, 2)
        print("The %s assumes a more defensive stance! (+DEF, +M'DEF)" % (monster.name))

    elif monster.m_attk >= monster.attk and monster.mp >= 2: # Magic Attack
        print('The %s is attempting to cast a strange spell!' % (monster.name))
        if dodge in range(temp_stats['evad'], 250):
            dealt = monster.monst_magic(var)
            player.hp -= dealt
            print("The %s's spell succeeds, and deals %s damage to you!" % (monster.name, dealt))
        else:
            print("The spell doesn't appear to have had any effect...")
        monster.mp -= 2

    else:
        monster.monst_attk(var, dodge)

def after_battle(): # Assess the results of the battle
    global player
    global position

    update_stats()
    winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_LOOP)
    winsound.PlaySound('Music\\Adventures in Pixels', winsound.SND_ASYNC | winsound.SND_LOOP)
    while True:
        if monster.hp > 0 and player.hp <= 0:
            winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_LOOP)
            winsound.PlaySound('Music\\Power-Up.wav', winsound.SND_ASYNC | winsound.SND_LOOP)
            print('Despite your best efforts, the %s has bested you. You are dead.' % (monster.name))
            print('-'*25)
            while True:
                y_n = input('Do you wish to continue playing? | Yes or No: ')
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n in 'yes': # If you die, you return to the X, Y coordinates of O, O at half health/mana
                    world.back_to_coords()
                    player.hp = int(static['hp_p']/2)
                    player.mp = int(static['mp_p']/2)
                    winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_LOOP)
                    winsound.PlaySound(position['reg_music'], winsound.SND_ASYNC | winsound.SND_LOOP)
                    return
                elif y_n in 'no':
                    sys.exit()

        elif monster.hp <= 0 and player.hp > 0:
            print('The %s falls to the ground, dead as a stone.' % (monster.name))
            print('-'*25)
            if monster.items:
                cat = monster.items.cat
                inv_system.inventory[cat].append(_c(monster.items))
                print('The %s drops a %s! You put it in your inventory for safe keeping.' % (monster.name, str(monster.items)))
            gold = player.give_gold()
            if gold > 0:
                print('You received %s GP!' % (gold))
            try:
                reward = int(math.sqrt(monster.lvl - (player.lvl/2) + 1.5) + player.ext_exp)*2
            except ValueError:
                reward = random.randint(1, 2)
            if reward <= 0:
                reward = random.randint(1, 2)
            player.exp += reward
            print("You've gained %s experience point%s!" % (reward, 's' if reward > 1 else ''))
            player.level_up()
            winsound.PlaySound(None, winsound.SND_ASYNC | winsound.SND_LOOP)
            winsound.PlaySound(position['reg_music'], winsound.SND_ASYNC | winsound.SND_LOOP)
            return

        elif player.hp <= 0 and monster.hp <= 0:
            player.hp = 1

def run_away():
    print('You begin to flee.')
    if random.randint(1, 100) in range(50, 101): # There's a 50% change that running will fail
        print('Your attempt to escape failed!')
        return False
    else:
        print('You manage to escape from the %s!' % (monster.name))
        return True

def bat_stats(): # Makes sure that the player and monster never have negative stats
                 # Display their stats after they're fixed
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
    print('%s: %s/%s HP | %s/%s MP  LVL: %s' % (player.name, player.hp, static['hp_p'], player.mp, static['mp_p'], player.lvl))
    print('%s: %s/%s HP | %s/%s MP  LVL: %s' % (monster.name, monster.hp, static['hp_m'], monster.mp, static['mp_m'], monster.lvl))
    print('-'*25)