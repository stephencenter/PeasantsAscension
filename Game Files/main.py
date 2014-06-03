# Pythonius; v0.3.4 Alpha
game_version = 'v0.3.4'
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
#
#  2. I am completely open to any and all criticism! I'm still pretty new to
#     programming, so I need all the advice I can get. Bug reports are great
#     too! Contact information is near the top of this module.
#
#  3. If you encounter an error message at any point when playing this, please
#     email the error code to me. If you could provide a description of what
#     you did to cause the bug, that'd be great. Contact information is near
#     the top of the module.
#-----------------------------------------------------------------------------#
# Explanation of the number-based selection system:
#
#   The number-based selection system is a heavy improvement over the previous
#   word-based selection system. Previously, when confronted with options, you
#   had to type out the entire word (there were a few exceptions), unnecessarily
#   wasting time. For example, when going to view your inventory, selecting an
#   item looked like this:
#       Item Category: Item 1, Item 2, Item 3, Item 4, etc... | Input item name:
#
#   This was very-much time consuming and gets tedious quickly. As such, I
#   decided to improve it:

#       Item category:
#             [1] Item 1
#             [2] Item 2
#             [3] Item 3
#       Input [#]:
#
#   Not only does this save time, but it also looks much more visually
#   appealing in my opinion. I felt the need to explain this, I don't know why.
#-----------------------------------------------------------------------------#

import sys
import os
import random
import math
import time
import json
import copy

import pygame

import battle
import world
import inv_system
import magic
import bosses
import npcs
import pets
import items

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

# Establish "player" as a global variable
player = ''

# A dictionary containing player variables that don't change until
# level-up, as well as GP
static = {'hp_p': '', 'hp_m': '', 'mp_p': '', 'mp_m': '', 'r_xp': 3,
          'int': 1, 'str': 1, 'con': 1, 'dex': 1, 'luc': 1, 'gp': 20}

# A dictionary containing all information related to the player's position
position = {'x': 0, 'y': 0, 'avg': '', 'reg': 'Forest',
            'reg_music': 'Music/Through the Forest.ogg',
            'h': '', 'v': '', 'prev_town': [0, 0]}

# Identify the player's OS and set their save destination
if os.name == 'nt':  # Windows devices
    sav1 = 'Save Files\\misc_vars.json'  # Misc Variables
    sav2 = 'Save Files\\postition.json'  # Position
    sav3 = 'Save Files\\inventory.json'  # Inventory
    sav4 = 'Save Files\\equip_items.json'  # Equipped Items
    sav5 = 'Save Files\\play_stats.json'  # Player Stats
    sav6 = 'Save Files\\spellbook.json'  # Spellbook
    sav7 = 'Save Files\\def_bosses.json'  # Defeated Bosses
    sav8 = 'Save Files\\quests_dia.json'  # Quests & Dialogue
    sav9 = 'Save Files\\misc_boss_info.json'  # Misc Boss Info

elif os.name == 'posix':  # Unix-based devices
    sav1 = 'Save Files/misc_vars.json'  # Misc Variables
    sav2 = 'Save Files/postition.json'  # Position
    sav3 = 'Save Files/inventory.json'  # Inventory
    sav4 = 'Save Files/equip_items.json'  # Equipped Items
    sav5 = 'Save Files/play_stats.json'  # Player Stats
    sav6 = 'Save Files/spellbook.json'  # Spellbook
    sav7 = 'Save Files/def_bosses.json'  # Defeated Bosses
    sav8 = 'Save Files/quests_dia.json'  # Quests & Dialogue
    sav9 = 'Save Files/misc_boss_info.json'  # Misc Boss Info

# NOTE: If one of these files is missing, the entire game won't work,
# and as such will not be recognized as a save file anymore.

# NOTE 2: It is entirely possible (and actually very easy) to modify these
# save files to change your character's stats, items, etc. However, it CAN also
# cause the file to become corrupted if it is done incorrectly, so backup your
# files before doing so.

else:
    raise OSError('This game is not supported by your operating system.')


class PlayerCharacter:  # The Player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns,
                 spd, evad, lvl, exp, ext_ski, ext_gol, ext_exp,
                 class_=''):
        self.name = name  # Name
        self.hp = hp  # Health
        self.mp = mp  # Mana Points
        self.attk = attk  # Attack
        self.dfns = dfns  # Defense
        self.m_attk = m_attk  # Magic Attack
        self.m_dfns = m_dfns  # Magic Defense
        self.spd = spd  # Speed
        self.evad = evad  # Evasion
        self.lvl = lvl  # Level
        self.exp = exp  # Experience
        self.ext_ski = ext_ski  # Skill Points
        self.ext_gol = ext_gol  # Extra Gold Pieces
        self.ext_exp = ext_exp  # Extra Experience
        self.class_ = class_  # Player Class
        self.current_pet = ''  # Current Pet

    def player_damage(self, var):  # The formula for the player dealing damage
        phys_dealt = int((battle.temp_stats['attk']/2) -
                         (battle.monster.dfns/3) + (self.lvl/3) + var + 1)
        phys_dealt = magic.eval_element(
            p_elem=inv_system.equipped['weapon'].element,
            m_elem=battle.monster.element, p_dmg=phys_dealt)[0]
        if phys_dealt < 1:
            phys_dealt = 1
        return phys_dealt

    def choose_name(self):
        while True:
            self.name = input('What is your name, young adventurer? | Input Name: ')
            if not ''.join(self.name.split()):
                continue
            while True:
                y_n = input('So, your name is {0}? | Yes or No: '.format(self.name))
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n.startswith('y'):
                    return self.name
                elif y_n in ['no', 'n', 'nope']:
                    break

    def choose_class(self):
        while True:
            class_ = input(
                'Well then, {0}, which class would you like to begin training in? | Warrior, Mage, or Rogue: '.format(
                self.name))
            try:
                class_ = class_.lower()
            except AttributeError:
                continue
            classes = ['warrior', 'mage', 'rogue']
            spam = False
            for x, y in enumerate(['w', 'm', 'r']):
                if class_.startswith(y):
                    class_ = classes[x]
                    spam = True
            if not spam:
                continue
            while True:
                y_n = input('You wish to be of the {0} class? | Yes or No: '.format(class_.title()))
                try:
                    y_n = y_n.lower()
                except AttributeError:
                    continue
                if y_n.startswith('y'):
                    return class_
                elif y_n in ['no', 'n', 'nope']:
                    break

    def level_up(self):
        global static
        if self.exp >= static['r_xp']:
            pygame.mixer.music.load('Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            self.hp = static['hp_p']
            self.mp = static['mp_p']
            temp_ski = 0  # Temporary Skill Points
            while self.exp >= static['r_xp']:
                self.lvl += 1
                print("You've advanced to level {0}!".format(self.lvl))
                if self.class_ == 'warrior':
                    self.attk += random.randint(2, 3)
                    self.dfns += random.randint(2, 3)
                    self.m_attk += random.randint(0, 2)
                    self.m_dfns += random.randint(1, 2)
                    self.spd += random.randint(1, 2)
                    self.evad += random.randint(0, 1)
                    self.hp += random.randint(1, 2)
                    self.mp += random.randint(1, 2)
                elif self.class_ == 'mage':
                    self.attk += random.randint(0, 2)
                    self.dfns += random.randint(1, 2)
                    self.m_attk += random.randint(2, 3)
                    self.m_dfns += random.randint(2, 3)
                    self.spd += random.randint(1, 2)
                    self.evad += random.randint(0, 1)
                    self.hp += random.randint(1, 2)
                    self.mp += random.randint(2, 3)
                elif self.class_ == 'rogue':
                    self.attk += random.randint(2, 3)
                    self.dfns += random.randint(1, 2)
                    self.m_attk += random.randint(0, 2)
                    self.m_dfns += random.randint(1, 2)
                    self.spd += random.randint(2, 4)
                    self.evad += random.randint(1, 2)
                    self.hp += random.randint(2, 3)
                    self.mp += random.randint(1, 2)
                temp_ski += self.ext_ski
                magic.new_spells()
                self.exp -= static['r_xp']
                static['r_xp'] = int((math.pow(self.lvl*2, 1.8) - self.lvl))
            print('-'*25)
            self.skill_points(temp_ski)
            static['hp_p'] = self.hp
            static['mp_p'] = self.mp
            print('-'*25)
            save_game()
            return

    def skill_points(self, temp_ski):
        global static
        while temp_ski > 0:
            print('You have {0} skill point{1} left to spend.'.format(
                temp_ski, 's' if temp_ski > 1 else ''))
            while temp_ski > 0:
                skill = input("""Choose a skill to advance:
    [I]ntelligence - Use powerful magic with higher magic stats and MP!
    [S]trength -  Smash through enemies with higher attack and defense!
    [C]onstitution - Become a tank with higher defense stats and HP!
    [D]exterity - Improve your aerobic ability with higher evade/speed stats!
    [L]uck - Receive more gold, more experience, and even more skill points!
Input letter: """)
                try:
                    skill = skill.lower()
                except AttributeError:
                    continue
                if skill[0] in ['i', 's', 'c', 'd', 'l']:
                    if skill.startswith('i'):
                        vis_skill = 'Intelligence'
                    elif skill.startswith('s'):
                        vis_skill = 'Strength'
                    elif skill.startswith('c'):
                        vis_skill = 'Constitution'
                    elif skill.startswith('d'):
                        vis_skill = 'Dexterity'
                    else:
                        vis_skill = 'Luck'
                    while True:
                        y_n = input("Increase your {0}? | Yes or No: ".format(vis_skill))
                        try:
                            y_n = y_n.lower()
                        except AttributeError:
                            continue
                        if y_n.startswith('y'):
                            pass
                        elif y_n in ['n', 'no', 'nope']:
                            break
                        else:
                            continue
                        if skill.startswith('i'):
                            self.m_dfns += 1
                            self.m_attk += 1
                            self.mp += random.randint(3, 5)
                            static['int'] += 1
                        elif skill.startswith('s'):
                            self.attk += 2
                            self.dfns += 2
                            static['str'] += 1
                        elif skill.startswith('c'):
                            self.hp += random.randint(4, 6)
                            self.dfns += random.randint(0, 1)
                            self.m_dfns += random.randint(0, 1)
                            static['con'] += 1
                        elif skill.startswith('d'):
                            self.spd += 2
                            self.evad += 1
                            static['dex'] += 1
                        elif skill.startswith('l'):
                            self.ext_ski += random.choice([0, 0, 0, 1])
                            self.ext_gol += random.randint(0, 2)
                            self.ext_exp += random.randint(0, 1)
                            static['luc'] += 1
                        else:
                            continue
                        print('Your {0} has increased!'.format(vis_skill))
                        temp_ski -= 1
                        break
        print()
        print('You are out of skill points.')

    def player_info(self):
        print("-{0}'s Stats-".format(self.name))
        time.sleep(0.40)
        print('Level: {0} | Class: {1}'.format(self.lvl, self.class_.title()))
        time.sleep(0.40)
        print('HP: {0}/{1} | MP: {2}/{3}'.format(self.hp, static['hp_p'],
                                                 self.mp, static['mp_p']))
        time.sleep(0.40)
        print('Attack: {0} | M. Attack: {1}'.format(self.attk, self.m_attk))
        time.sleep(0.40)
        print('Defense: {0} | M. Defense: {1}'.format(self.dfns, self.m_dfns))
        time.sleep(0.45)
        print('Speed: {0} | Evasion: {1}'.format(self.spd, self.evad))
        time.sleep(0.40)
        print('INT: {0} | STR: {1} | CON: {2} | DEX: {3} | LUC: {4}'.format(
            static['int'], static['str'],
            static['con'], static['dex'],
            static['luc']))
        time.sleep(0.40)
        print('Experience Pts: {0}/{1} | Gold Pieces: {2}'.format(self.exp,
                                                                  static['r_xp'],
                                                                  static['gp']))
        time.sleep(0.40)
        print()
        print('-Equipped Items-')
        time.sleep(0.40)
        print('Weapon: {0}'.format(str(inv_system.equipped['weapon'])))
        time.sleep(0.40)
        print('Armor:')
        time.sleep(0.40)
        print('  Head: {0}'.format(str(inv_system.equipped['head'])))
        time.sleep(0.40)
        print('  Body: {0}'.format(str(inv_system.equipped['body'])))
        time.sleep(0.40)
        print('  Legs: {0}'.format(str(inv_system.equipped['legs'])))
        input('Press Enter/Return ')


def create_player():
    global player
    global static
    player = PlayerCharacter('', 15, 4, 4, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)
    static['hp_p'] = copy.copy(player.hp)
    static['mp_p'] = copy.copy(player.mp)
    player.name = player.choose_name()
    player.class_ = player.choose_class()
    if player.class_ == "warrior":
        static['hp_p'] += 5
        static['mp_p'] -= 1
        player.dfns += 2
        player.attk += 2
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['weapon'] = copy.copy(items.wdn_sht)
    elif player.class_ == "mage":
        static['hp_p'] += 1
        static['mp_p'] += 4
        player.m_attk += 2
        player.m_dfns += 2
        inv_system.equipped['weapon'] = copy.copy(items.mag_twg)
    elif player.class_ == "rogue":
        static['hp_p'] += 2
        static['mp_p'] += 1
        player.attk += 1
        player.dfns += 1
        player.spd += 3
        player.evad += 1
        inv_system.equipped['weapon'] = copy.copy(items.stn_dag)
    player.hp = copy.copy(static['hp_p'])
    player.mp = copy.copy(static['mp_p'])
    print('-'*25)


def check_save():  # Check for save files and load the game if they're found
    global static
    global position
    print('-'*25)
    # Check each part of the save file
    for file in [sav1, sav2, sav3, sav4, sav5, sav6, sav7, sav8, sav9]:
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
        if y_n.startswith('y'):
            print('Loading...')
            time.sleep(0.25)
            try:  # Attempt to open the save files and translate
                # them into objects/dictionaries
                with open(sav1, encoding='utf-8') as a:
                    static = json.load(a)
                with open(sav2, encoding='utf-8') as b:
                    position = json.load(b)
                inv_system.deserialize_inv(sav3)
                inv_system.deserialize_equip(sav4)
                deserialize_player(sav5)
                magic.deserialize_sb(sav6)
                with open(sav7, encoding='utf-8') as g:
                    bosses.defeated_bosses = list(json.load(g))
                npcs.deserialize_dialogue(sav8)
                bosses.deserialize_bosses(sav9)
                print('Load successful.')
                return
            except IOError:
                print('There was an error loading your game. Error code: IO')
            except ValueError:
                print('There was an error loading your game. Error code: VE')
            print('-'*25)
            create_player()
            return
        elif y_n .startswith('y'):
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
        if y_n.startswith('y'):
            print('Saving...')
            time.sleep(0.25)
            # Check if the save directory already exists, and create it if it doesn't
            if not os.path.exists("Save Files"):
                os.makedirs("Save Files")
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
                    json.dump(bosses.defeated_bosses, g,
                              indent=4, separators=(', ', ': '))
                npcs.serialize_dialogue(sav8)
                bosses.serialize_bosses(sav9)
                print('Save successful.')
                return
            except IOError:
                print('There was an error saving your game. Error code: IO')
            except ValueError:
                print('There was an error saving your game. Error code: VE')
        elif y_n.startswith('n'):
            return


def serialize_player(path):  # Save the "PlayerCharacter" object as a JSON file
    spam = {}
    for key in player.__dict__:
        if (player.__dict__[key] != player.current_pet) or (not player.current_pet):
            spam[key] = player.__dict__[key]
        else:
            spam[key] = [player.__dict__[key].name, player.__dict__[key].level]
    with open(path, mode='w', encoding='utf-8') as e:
        json.dump(spam, e, indent=4, separators=(', ', ': '))


def deserialize_player(path):  # Load the JSON file and translate
    # it into a "PlayerCharacter" object
    global player
    player = PlayerCharacter('', 15, 4, 4, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)
    with open(path, encoding='utf-8') as e:
        spam = json.load(e)
    for key in spam:
        if key == 'current_pet' and spam[key]:
            for pet in pets.all_pets:
                if pet.name == spam[key][0]:
                    pet.level = spam[key][1]
                    spam[key] = pet
    player.__dict__ = spam


def title_screen():
    pygame.mixer.music.load('Music/Prologue.ogg')
    pygame.mixer.music.play(-1)
    print("""
      ____        _   _                 _
     |  _ \\ _   _| |_| |__   ___  _ __ (_)_   _ ___
     | |_) | | | | __| '_ \\ / _ \\| '_ \\| | | | / __|
     |  __/| |_| | |_| | | | (_) | | | | | |_| \\__ \\
     |_|    \\__, |\\__|_| |_|\\___/|_| |_|_|\\__,_|___/
            |___/

PythoniusRPG {0} -- Programmed in Python by Stephen Center
-----------------------------------------------------------""".format(game_version))
    while True:
        choice = input('[P]lay Game  |  [C]redits  | [E]xit  |  Input letter: ')
        try:
            choice = choice.lower()
        except AttributeError:
            continue
        if choice.startswith('p'):
            return
        elif choice.startswith('c'):
            print('-'*25)
            with open('Credits.txt') as f:
                for f.readline in f:
                    print(''.join(f.readline.rstrip("\n").split(";")))
                    time.sleep(0.35)
            print('-'*25)
        elif choice.startswith('e'):
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    title_screen()
    check_save()  # Check for save files...
    world.movement_system()  # ...and then start the game
