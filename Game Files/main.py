# Pythonius; v0.0.8 Alpha
# Programmed in Python 3 by Stephen Center, (c)2013-2014
# Music by Ben Landis: http://www.benlandis.com/
# And Eric Skiff: http://ericskiff.com/music/
#-----------------------------------------------------------------------------#
# Contact me via Twitter (@RbwNjaFurret) or email (ninjafurret@gmail.com)
# for questions/feedback.
#-----------------------------------------------------------------------------#
# Notes for people reading this code:
#  1. print('-'*25) <-- This line appears constantly in my code. It's purpose
#     is to enhance readability and organization for people playing the game.
#  2. I am completely open to any and all criticism! I'm still pretty new to
#     programming, so I need all the advice I can get. Bug reports are great
#     too! Contact information is near the top of this module.
#  3. If you encounter an error message at any point when playing this, please
#     email the error code to me. If you could provide a description of what
#     you did to cause the bug, that'd be great. Contact information is near
#     the top of the module.
#-----------------------------------------------------------------------------#

import sys
import os
import random
import math
import time
import json
import winsound
import copy

import towns
import monsters
import battle
import world
import inv_system
import magic
import bosses

# Establish "player" as a global variable
player = ''

# A dictionary containing player variables that don't change until
# level-up, as well as GP
static = {'hp_p': '', 'hp_m': '', 'mp_p': '', 'mp_m': '', 'r_xp': 3,
          'int': 1, 'str': 1, 'con': 1, 'dex': 1, 'luc': 1, 'gp': 0}

# A dictionary containing all information related to the player's position
position = {'x': 0, 'y': 0, 'avg': '', 'reg': 'Forest',
            'reg_music': 'Music\\Through the Forest.wav',
            'h': '', 'v': '', 'prev_town': [0, 0]}

# Identify the player's OS and set their save destination
if os.name == 'nt':  # Windows
    sav1 = 'C:\\Pythonius\\Save Files\\sav_a.json'  # Misc Variables
    sav2 = 'C:\\Pythonius\\Save Files\\sav_b.json'  # Position
    sav3 = 'C:\\Pythonius\\Save Files\\sav_c.json'  # Inventory
    sav4 = 'C:\\Pythonius\\Save Files\\sav_d.json'  # Equipped Items
    sav5 = 'C:\\Pythonius\\Save Files\\sav_e.json'  # Player Stats
    sav6 = 'C:\\Pythonius\\Save Files\\sav_f.json'  # Spellbook
    sav7 = 'C:\\Pythonius\\Save Files\\sav_g.json'  # Defeated Bosses

else:
    raise OSError('This game is not supported by your operating system.')
    input('Press enter to exit')
    sys.exit()


class PlayerCharacter:  # The Player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns,
                 spd, evad, lvl, exp, ext_ski, ext_gol, ext_exp,
                 _class=''):
        self.name = name         # Name
        self.hp = hp             # Health
        self.mp = mp             # Mana Points
        self.attk = attk         # Attack
        self.dfns = dfns         # Defense
        self.m_attk = m_attk     # Magic Attack
        self.m_dfns = m_dfns     # Magic Defense
        self.spd = spd           # Speed
        self.evad = evad         # Evasion
        self.lvl = lvl           # Level
        self.exp = exp           # Experience
        self.ext_ski = ext_ski   # Skill Points
        self.ext_gol = ext_gol   # Extra Gold Pieces
        self.ext_exp = ext_exp   # Extra Experience
        self._class = _class     # Player Class

    def player_damage(self, var):  # The formula for the player dealing damage
        try:
            phys_dealt = int(math.sqrt(self.attk +
                                       self.lvl -
                                       battle.monster.dfns) + 3) + var
        except ValueError:  # Just incase math.sqrt recieves a negative number
            phys_dealt = 1
        phys_dealt = magic.eval_element(p_elem=inv_system.equipped['weapon'].element,
                                        m_elem=battle.monster.element,
                                        p_dmg=phys_dealt)[0]
        return phys_dealt


    def choose_name(self):
        while True:
            self.name = input('What is your name, young adventurer? | Input Name: ')
            while True:
                y_n = input('So, your name is %s? | Yes or No: ' % (self.name))
                try:
                   y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n in 'yes':
                    return self.name
                elif y_n in 'no':
                    break


    def choose_class(self):
        while True:
            _class = input('Well then, %s, which class would you like to begin training in? | Warrior or Mage: '
                           % (self.name))
            try:
                _class = _class.lower()
            except AttributeError:
                continue
            if _class in ['warrior', 'mage']:
                while True:
                    y_n = input('You wish to be of the %s class? | Yes or No: '
                                % (_class.title()))
                    try:
                       y_n = y_n.lower()
                    except AttributeError:
                        continue
                    if y_n in 'yes':
                        return _class
                    elif y_n in 'no':
                        break


    def level_up(self):
        global static
        if self.exp >= static['r_xp']:
            self.hp = static['hp_p']
            self.mp = static['mp_p']
            temp_ski = 0  # Temporary Skill Points
            while self.exp >= static['r_xp']:
                self.lvl += 1
                static['r_xp'] = int((math.pow(self.lvl*2, 1.8) - (self.lvl)))
                self.attk += random.randint(1, 2)
                self.dfns += random.randint(0, 2)
                self.m_attk += random.randint(1, 2)
                self.m_dfns += random.randint(0, 2)
                self.spd += random.randint(1, 2)
                self.evad += random.randint(0, 1)
                self.hp += random.randint(0, 1)
                self.mp += random.randint(1, 2)
                temp_ski += self.ext_ski
                print("You've advanced to level %s!" % (self.lvl))
                magic.new_spells()
            print('-'*25)
            self.skill_points(temp_ski)
            static['hp_p'] = self.hp
            static['mp_p'] = self.mp
            print('-'*25)
            save_game()
            return


    def skill_points(self, temp_ski):
        global static
        intelligence = ['int', 'intel', 'intelligence']
        strength = ['str', 'strength']
        constitution = ['con', 'const', 'constitution']
        dexterity = ['dex', 'dexterity']
        luck = ['luc', 'luck', 'lucky']
        while temp_ski > 0:
            print()
            print('You have %s skill points left to spend.' % (temp_ski))
            while temp_ski > 0:
                skill = input('INT, STR, CON, DEX, LUC | Choose one skill to advance: ')
                try:
                    skill = skill.lower()
                except AttributeError:
                    continue
                if skill in intelligence:
                    self.m_dfns += 1
                    self.m_attk += 1
                    self.mp += random.randint(3, 5)
                    static['int'] += 1
                elif skill in strength:
                    self.attk += 1
                    self.dfns += 1
                    static['str'] += 1
                elif skill in constitution:
                    self.hp += random.randint(4, 6)
                    self.dfns += random.randint(0, 1)
                    self.m_dfns += random.randint(0, 1)
                    static['con'] += 1
                elif skill in dexterity:
                    self.spd += 1
                    self.evad += 1
                    static['dex'] += 1
                elif skill in luck:
                    self.ext_ski += random.choice([0, 0, 0, 1])
                    self.ext_gol += random.randint(0, 2)
                    self.ext_exp += random.randint(0, 1)
                    static['luc'] += 1
                else:
                    continue
                print('Your experience in %s has increased.' % (skill.upper()))
                temp_ski -= 1
                break
        print()
        print('You are out of skill points.')


    def player_info(self):
        print("-%s's Stats-" % (self.name))
        print('Level: %s | Class: %s' % (self.lvl, self._class.title()))
        print('HP: %s/%s | MP: %s/%s' % (self.hp, static['hp_p'],
                                         self.mp, static['mp_p']))
        print('Attack: %s | M. Attack: %s' % (self.attk, self.m_attk))
        print('Defense: %s | M. Defense: %s' % (self.dfns, self.m_dfns))
        print('Speed: %s | Evasion: %s' % (self.spd, self.evad))
        print('INT: %s | STR: %s | CON: %s | DEX: %s | LUC: %s'
              % (static['int'], static['str'],
                 static['con'], static['dex'],
                 static['luc']))
        print('Experience Pts: %s/%s | Gold Pieces: %s' % (self.exp,
                                                           static['r_xp'],
                                                           static['gp']))
        print()
        print('-Equipped Items-')
        print('Weapon: %s' % (str(inv_system.equipped['weapon'])))
        print('Armor:')
        print('  Head: %s' % (str(inv_system.equipped['head'])))
        print('  Body: %s' % (str(inv_system.equipped['body'])))
        print('  Legs: %s' % (str(inv_system.equipped['legs'])))


def create_player():
    global player
    global static
    player = PlayerCharacter('', 15, 4, 4, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)
    static['hp_p'] = copy.copy(player.hp)
    static['mp_p'] = copy.copy(player.mp)
    player.name = player.choose_name()
    player._class = player.choose_class()
    if player._class == "warrior":
        static['hp_p'] += 5
        static['mp_p'] -= 2
        player.dfns += 2
        player.attk += 2
        player.spd -= 1
        player.evad -= 1
        player.m_dfns -= 1
        player.m_attk -= 1
        inv_system.equipped['weapon'] = copy.copy(inv_system.wdn_sht)
    elif player._class == "mage":
        static['mp_p'] += 5
        player.attk -= 1
        player.m_attk += 2
        player.dfns -= 1
        player.m_dfns += 2
        inv_system.equipped['weapon'] = copy.copy(inv_system.mag_twg)
    player.hp = copy.copy(static['hp_p'])
    player.mp = copy.copy(static['mp_p'])
    print('-'*25)


def check_save():  # Check for save files and load the game if they're found
    global static
    global position
    print('Loading...')
    winsound.PlaySound(None, winsound.SND_ASYNC)
    winsound.PlaySound("Music\\Prologue.wav", winsound.SND_ASYNC |
                                              winsound.SND_LOOP |
                                              winsound.SND_NODEFAULT)
    print('-'*25)
    # Check each part of the save file
    for file in [sav1, sav2, sav3, sav4, sav5, sav6, sav7]:
        if os.path.isfile(file):
            pass
        else:
            create_player()
            return
    print('It appears that you already have a save file for this game.')
    while True:
        y_n = input('Do you wish to load the previous save file? | Yes or No: ')
        try:
            y_n = y_n.lower()
        except AttributeError:
            continue
        if y_n in 'yes':
            print('Loading...')
            time.sleep(0.25)
            try:  # Attempt to open the save files and translate
                  # them into objects/dictionaries
                with open(sav1, mode='r', encoding='utf-8') as a:
                        static = json.load(a)
                with open(sav2, mode='r', encoding='utf-8') as b:
                        position = json.load(b)
                inv_system.deserialize_inv(sav3)
                inv_system.deserialize_equip(sav4)
                deserialize_player(sav5)
                magic.deserialize_sb(sav6)
                with open(sav7, mode='r', encoding='utf-8') as g:
                    bosses.defeated_bosses = list(json.load(g))
                print('Load successful.')
                if not towns.search_towns(position['x'], position['y'], enter=False):
                    print('-'*25)
                return
            except (IOError or OSError):
                print('There was an error loading your game.')
                print('-'*25)
                create_player()
                return
        elif y_n in 'no':
                print('-'*25)
                create_player()
                return


def save_game():
    while True:
        y_n = input('Do you wish to save your progress? | Yes or No: ')
        try:
            y_n = y_n.lower()
        except AttributeError:
            continue
        if y_n in 'yes':
            print('Saving...')
            time.sleep(0.25)
            # Check if the save directory already exists, and create it if it doesn't
            if not os.path.exists("c:\\Pythonius\\Save Files"):
                os.makedirs("c:\\Pythonius\\Save Files")
            try:
                with open(sav1, mode='w', encoding='utf-8') as a:
                    json.dump(static, a, indent=4, separators=(', ', ': '))
                with open(sav2, mode='w', encoding='utf-8') as b:
                    json.dump(position, b, indent=4, separators=(', ', ': '))
                inv_system.serialize_inv(sav3)
                inv_system.serialize_equip(sav4)
                serialize_player(sav5)
                magic.serialize_sb(sav6)
                with open(sav7, mode='w', encoding='utf-8') as g:
                    json.dump(dict(bosses.defeated_bosses), g,
                              indent=4, separators=(', ', ': '))
                print('Save successful.')
                return
            except (IOError or OSError):
                print('There was an error saving your game.')
        elif y_n in 'no':
            return


def serialize_player(path):  # Save the "PlayerCharacter" object as a JSON file
    with open(path, mode='w', encoding='utf-8') as e:
        json.dump(player.__dict__, e, indent=4, separators=(', ', ': '))


def deserialize_player(path):  # Load the JSON file and translate
                               # it into a "PlayerCharacter" object
    global player
    player = PlayerCharacter('', 15, 4, 4, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)
    with open(path, mode='r', encoding='utf-8') as e:
        player.__dict__ = json.load(e)


if __name__ == "__main__":
    check_save()  # Check for save files...
    world.movement_system()  # ...and then start the game
