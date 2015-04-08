#!/usr/bin/env python
# PythoniusRPG v0.6.4 Alpha
game_version = 'v0.6.4'
# -----------------------------------------------------------------------------#
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
#-----------------------------------------------------------------------------#
# Music by Ben Landis: http://www.benlandis.com/
# And Eric Skiff: http://ericskiff.com/music/
#-----------------------------------------------------------------------------#
# Contact me via Twitter (@RbwNjaFurret) or email (ninjafurret@gmail.com)
# for questions/feedback. My website is http://rbwnjafurret.com/
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

# Establish "player" as a global variable
player = ''

# A dictionary containing miscellaneous variables made entirely of
misc_vars = {'hp_p': '', 'hp_m': '', 'mp_p': '', 'mp_m': '', 'r_xp': 3,
             'int': 1, 'str': 1, 'con': 1, 'dex': 1, 'per': 1, 'for': 1, 'gp': 20}

# A dictionary containing all information related to the player's position
position = {'x': 0, 'y': 0, 'avg': '', 'reg': 'Forest',
            'reg_music': 'Music/Through the Forest.ogg',
            'h': '', 'v': '', 'prev_town': [0, 0]}

import sys
import os
import random
import math
import time
import json
import copy
import configparser
import ctypes
import re
import logging
import msvcrt

import pygame

import world
import inv_system
import battle
import magic
import bosses
import pets
import items
import sounds
import towns

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

# Log everything and send it to stderr.
logging.basicConfig(filename='../error_log.out', level=logging.DEBUG)

logging.debug("Game run")

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

town_list = towns.town_list

save_dir = 'Save Files'
adventure_name = ''

sav_acquired_gems = 'Save Files/{CHARACTER_NAME}/acquired_gems.json'  # Acquired Gems

sav_def_bosses = 'Save Files/{CHARACTER_NAME}/def_bosses.json'  # Defeated Bosses

sav_equip_items = 'Save Files/{CHARACTER_NAME}/equip_items.json'  # Equipped Items

sav_inventory = 'Save Files/{CHARACTER_NAME}/inventory.json'  # Inventory

sav_misc_boss_info = 'Save Files/{CHARACTER_NAME}/misc_boss_info.json'  # Misc Boss Info

sav_misc_vars = 'Save Files/{CHARACTER_NAME}/misc_vars.json'  # Misc Variables

sav_play_stats = 'Save Files/{CHARACTER_NAME}/play_stats.json'  # Player Stats

sav_position = 'Save Files/{CHARACTER_NAME}/position.json'  # Position

sav_quests_dia = 'Save Files/{CHARACTER_NAME}/quests_dia.json'  # Quests & Dialogue

sav_spellbook = 'Save Files/{CHARACTER_NAME}/spellbook.json'  # Spellbook

# NOTE 1: The save file locations can be changed in the file "settings.cfg".

# NOTE 2: If one of these files is missing, the entire game won't work,
# and as such will not be recognized as a save file anymore.

# NOTE 3: It is entirely possible (and actually very easy) to modify these
# save files to change your character's stats, items, etc. However, it CAN also
# cause the file to become corrupted if it is done incorrectly, so backup your
# files before doing so.

music_vol = 1.0  # The volume of the game, on a scale from 0 (muted) to 1.0 (loudest)
sound_vol = 1.0  # These values can be changed in settings.cfg file

text_scroll = True


class PlayerCharacter:  # The Player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk,
                 p_dfns, spd, evad, lvl, exp, ext_ski, ext_gol, ext_exp,
                 class_='', element='none'):
        self.name = name  # Name
        self.hp = hp  # Health
        self.mp = mp  # Mana Points
        self.attk = attk  # Attack
        self.dfns = dfns  # Defense
        self.p_attk = p_attk  # Pierce Attack
        self.p_dfns = p_dfns  # Pierce Defense
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
        self.element = element
        self.status_ail = 'none'  # Current Status Ailment

    def player_damage(self, var):  # The formula for the player dealing damage
        if inv_system.equipped['weapon'].type_ != 'ranged':
            dam_dealt = math.ceil(battle.temp_stats['attk']/2 - (battle.monster.dfns/2)) + var
            if self.status_ail == 'weakened':
                dam_dealt /= 2
                dam_dealt = math.ceil(dam_dealt)
                print('You deal less damage because of your weakened state.')

        else:
            dam_dealt = math.ceil(battle.temp_stats['p_attk']/2 - (battle.monster.p_dfns/2)) + var
            dam_dealt *= 2
            if self.status_ail == 'blinded':
                dam_dealt /= 2
                dam_dealt = math.ceil(dam_dealt)
                print('You deal less damage because your eyesight made aiming difficult.')


        dam_dealt = magic.eval_element(
            p_elem=inv_system.equipped['weapon'].element,
            m_elem=battle.monster.element, p_dmg=dam_dealt)[0]

        if dam_dealt < 1:
            dam_dealt = 1

        if random.randint(1, 100) <= 7:
            print("It's a critical hit! 2x damage!")

        return dam_dealt

    def choose_name(self):
        while True:
            self.name = input('What is your name, young adventurer? | Input Name: ')

            if not ''.join(self.name.split()):
                continue

            while True:
                y_n = input('So, your name is {0}? | Yes or No: '.format(self.name))
                y_n = y_n.lower()

                if y_n.startswith('y'):
                    return self.name

                elif y_n.startswith('n'):
                    break

    def choose_class(self):
        while True:
            class_ = input('{0}, which class would you like to train as?\n\
    Warrior, Mage, Assassin, or Ranger: '.format(self.name))

            class_ = class_.lower()
            classes = ['warrior', 'mage', 'assassin', 'ranger']

            spam = False

            for x, y in enumerate(['w', 'm', 'a', 'r']):
                if class_.startswith(y):
                    class_ = classes[x]
                    spam = True

            if not spam:
                continue

            while True:
                y_n = input('You wish to be of the {0} class? | Yes or No: '.format(
                    class_.title()))

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    return class_

                elif y_n.startswith('n'):
                    break

    def level_up(self):
        global misc_vars
        if self.exp >= misc_vars['r_xp']:
            print()
            pygame.mixer.music.load('Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(music_vol)

            self.hp = misc_vars['hp_p']
            self.mp = misc_vars['mp_p']

            rem_points = 0  # Remaining Skill Points
            extra_points = 0  # The number of extra skill points the player will receive

            while self.exp >= misc_vars['r_xp']:
                sounds.item_pickup.play()
                self.lvl += 1
                print("You've advanced to level {0}!".format(self.lvl))

                rem_points += 1
                extra_points += self.ext_ski
                magic.new_spells()

                if self.class_ == 'warrior':
                    self.p_attk += random.randint(0, 2)
                    self.p_dfns += random.randint(1, 3)
                    self.attk += random.randint(1, 3)
                    self.dfns += random.randint(1, 3)
                    self.m_attk += random.randint(0, 2)
                    self.m_dfns += random.randint(0, 2)
                    self.spd += random.randint(1, 2)
                    self.evad += random.randint(0, 1)
                    self.hp += random.randint(1, 2)
                    self.mp += random.randint(1, 2)

                elif self.class_ == 'mage':
                    self.p_attk += random.randint(0, 2)
                    self.p_dfns += random.randint(0, 2)
                    self.attk += random.randint(0, 2)
                    self.dfns += random.randint(0, 2)
                    self.m_attk += random.randint(1, 3)
                    self.m_dfns += random.randint(1, 3)
                    self.spd += random.randint(1, 2)
                    self.evad += random.randint(0, 1)
                    self.hp += random.randint(1, 2)
                    self.mp += random.randint(2, 3)

                elif self.class_ == 'assassin':
                    self.p_attk += random.randint(0, 2)
                    self.p_dfns += random.randint(1, 2)
                    self.attk += random.randint(1, 3)
                    self.dfns += random.randint(1, 2)
                    self.m_attk += random.randint(0, 2)
                    self.m_dfns += random.randint(1, 2)
                    self.spd += random.randint(2, 4)
                    self.evad += random.randint(1, 2)
                    self.hp += random.randint(2, 3)
                    self.mp += random.randint(1, 2)

                elif self.class_ == 'ranger':
                    self.p_attk += random.randint(2, 4)
                    self.p_dfns += random.randint(0, 2)
                    self.attk += random.randint(1, 2)
                    self.dfns += random.randint(0, 2)
                    self.m_attk += random.randint(0, 2)
                    self.m_dfns += random.randint(1, 2)
                    self.spd += random.randint(2, 4)
                    self.evad += random.randint(2, 3)
                    self.hp += random.randint(1, 3)
                    self.mp += random.randint(1, 3)

                self.exp -= misc_vars['r_xp']
                misc_vars['r_xp'] = int((math.pow(self.lvl*2, 2) - 1.2*self.lvl))

            print('-'*25)
            self.skill_points(rem_points, extra_points)

            misc_vars['hp_p'] = self.hp
            misc_vars['mp_p'] = self.mp

            print('-'*25)
            save_game()
            return

    def skill_points(self, rem_points, extra_points):
        global misc_vars

        if extra_points:
            print('Your great fortune has granted you {0} additional skill points!'.format(
                extra_points))
            rem_points += extra_points

        while rem_points > 0:
            print('You have {0} skill point{1} left to spend.'.format(
                rem_points, 's' if rem_points > 1 else ''))

            while rem_points > 0:
                skill = input("""Choose a skill to advance:
    [I]ntelligence - Use powerful magic with higher magic stats and MP!
    [S]trength -  Smash through enemies with higher attack and defense!
    [C]onstitution - Become a tank with higher defense stats and HP!
    [D]exterity - Improve your aerobic ability with higher evade/speed stats!
    [P]erception - Eleminate your enemies with ease using higher pierce and evasion!
    [F]ortune - Increase your luck in hopes of getting more GP, XP, and skill points!
Input letter: """)

                skill = skill.lower()

                if any(map(skill.startswith, ['i', 's', 'c', 'd', 'p', 'f'])):
                    if skill.startswith('i'):
                        vis_skill = 'Intelligence'
                    elif skill.startswith('s'):
                        vis_skill = 'Strength'
                    elif skill.startswith('c'):
                        vis_skill = 'Constitution'
                    elif skill.startswith('d'):
                        vis_skill = 'Dexterity'
                    elif skill.startswith('p'):
                        vis_skill = 'Perception'
                    else:
                        vis_skill = 'Fortune'

                    while True:
                        y_n = input("Increase your {0}? | Yes or No: ".format(vis_skill))

                        y_n = y_n.lower()

                        if y_n.startswith('y'):
                            pass
                        elif y_n.startswith('n'):
                            print('-'*25)
                            break
                        else:
                            continue

                        if skill.startswith('i'):
                            self.m_dfns += random.randint(1, 2)
                            self.m_attk += random.randint(1, 2)
                            self.mp += random.randint(3, 5)
                            misc_vars['int'] += 1

                        elif skill.startswith('s'):
                            self.attk += random.randint(1, 2)
                            self.p_dfns += random.randint(0, 1)
                            self.dfns += random.randint(1, 2)
                            misc_vars['str'] += 1

                        elif skill.startswith('c'):
                            self.hp += random.randint(3, 5)
                            self.dfns += random.randint(0, 1)
                            self.p_dfns += random.randint(0, 1)
                            self.m_dfns += random.randint(0, 1)
                            misc_vars['con'] += 1

                        elif skill.startswith('d'):
                            self.spd += 3
                            self.p_attk += 1
                            self.evad += 1
                            misc_vars['dex'] += 1

                        elif skill.startswith('p'):
                            self.hp += 1
                            self.p_attk += 2
                            self.p_dfns += 2
                            self.evad += random.randint(0, 2)
                            misc_vars['per'] += 1

                        elif skill.startswith('f'):
                            self.hp += random.randint(0, 1)
                            self.mp += random.randint(0, 1)
                            if random.randint(0, 1):
                                self.ext_ski += (0, 1)

                            self.ext_gol += random.randint(0, 2)
                            self.ext_exp += random.randint(0, 2)

                            misc_vars['for'] += 1

                        else:
                            continue

                        print('Your {0} has increased!'.format(vis_skill))
                        rem_points -= 1
                        break
        print()
        print('You are out of skill points.')

    def player_info(self):
        print("""\
-{0}'s Stats-
Level: {1} | Class: {2} | Element: {3}
HP: {4}/{5} | MP: {6}/{7}
Attack: {8} | M. Attack: {9} | P. Attack {10}
Defense: {11} | M. Defense: {12} | P. Defense {13}
INT: {14} | STR: {15} | CON: {16} | DEX: {17} | PER: {18} | FOR: {19}
Experience Pts: {20}/{21} | Gold Pieces: {22}

-Equipped Items-
Weapon: {23}
Accessory: {24}
Armor:
  Head: {25}
  Body: {26}
  Legs: {27}

-Current Pet-""".format(self.name,
                        self.lvl, self.class_.title(), self.element,
                        self.hp, misc_vars['hp_p'], self.mp, misc_vars['mp_p'],
                        self.attk, self.m_attk, self.p_attk,
                        self.dfns, self.m_dfns, self.p_dfns,
                        misc_vars['int'], misc_vars['str'], misc_vars['con'],
                        misc_vars['dex'], misc_vars['per'], misc_vars['for'],
                        self.exp, misc_vars['r_xp'], misc_vars['gp'],
                        inv_system.equipped['weapon'], inv_system.equipped['access'],
                        inv_system.equipped['head'], inv_system.equipped['body'],
                        inv_system.equipped['legs']))

        if inv_system.equipped['pet'] != '(None)':
            print('  Name: {0}'.format(inv_system.equipped['pet']))
            print('  Type: {0}'.format(inv_system.equipped['pet'].pet_type.title()))
            print('  Level: {0}'.format(inv_system.equipped['pet'].level))

        else:
            print('  (None)')

        print('-'*25)
        input('Press Enter/Return ')


def set_adventure_name():
    # This function asks the player for an "adventure name". This is the
    # name of the directory in which his/her save files will be stored.
    global adventure_name

    while True:
        # Certain OSes don't allow certain characters, so this removes those characters
        # and replaces them with whitespace. The player is then asked if this is okay.
        choice = input("Finally, what do you want to name this adventure? ")
        new_choice = re.sub('[^\w\-_ ]', '', choice)

        if not choice:  # Files/Folders cannot be have "" as their filename.
            print("Silence doesn't really make for a great adventure name.")
            print()
            continue

        elif os.path.isdir('/'.join([save_dir, new_choice])) and new_choice:
            # Make sure that the folder doesn't already exist, because
            # certain OSes don't allow duplicate folder names.
            print("I've already read about adventures with that name; be original!")
            print()
            continue

        elif new_choice != choice:
            if not new_choice and choice:
                print("Please name it something different.")
                print()
                continue

            while True:
                y_n = input('I had to change some of that. Does "{0}" sound okay? | Yes or No: '.
                            format(new_choice))

                y_n = y_n.lower()

                if y_n.startswith("y"):
                    adventure_name = new_choice
                    format_save_names()
                    return

                elif y_n.startswith("n"):
                    print()
                    break

        elif len(choice) > 35 and len(new_choice) > 30:
            print('The maximum Adventure Name size is 35 characters - sorry!]')

            continue

        else:
            while True:
                y_n = input('You wish for your adventure to be known as "{0}"? | Yes or No: '.
                            format(choice))

                y_n = y_n.lower()

                if y_n.startswith("y"):
                    adventure_name = choice
                    format_save_names()
                    return

                elif y_n.startswith("n"):
                    print()
                    break


def format_save_names():
    # Replace "{CHARACTER_NAME}" in the save-file paths to the player's adventure name.
    # e.g. "Save Files/{CHARACTER_NAME}/sav_acquired_gems" --> "Save Files/ADV/sav_acquired_gems

    for x in sorted(['sav_acquired_gems', 'sav_def_bosses',
                     'sav_equip_items', 'sav_inventory',
                     'sav_misc_boss_info', 'sav_misc_vars',
                     'sav_play_stats', 'sav_position',
                     'sav_quests_dia', 'sav_spellbook'], key=str.lower):

        spam = globals()[x]
        globals()[x] = '/'.join([save_dir, adventure_name, spam.split('/')[2]])


def create_player():
    global player
    global misc_vars

    player = PlayerCharacter('', 15, 4, 3, 1, 3, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)

    # Set the player's max HP and MP
    misc_vars['hp_p'] = copy.copy(player.hp)
    misc_vars['mp_p'] = copy.copy(player.mp)

    player.name = player.choose_name()
    print()
    player.class_ = player.choose_class()
    print()
    set_adventure_name()

    if player.class_ == "warrior":
        misc_vars['hp_p'] += 5
        misc_vars['mp_p'] -= 1
        player.dfns += 2
        player.p_dfns += 1
        player.attk += 2
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['weapon'] = copy.copy(items.wdn_sht)

    elif player.class_ == "mage":
        misc_vars['hp_p'] += 1
        misc_vars['mp_p'] += 4
        player.m_attk += 2
        player.m_dfns += 2
        inv_system.equipped['weapon'] = copy.copy(items.mag_twg)

    elif player.class_ == "assassin":
        misc_vars['hp_p'] += 2
        misc_vars['mp_p'] += 1
        player.attk += 1
        player.dfns += 1
        player.spd += 3
        player.evad += 1
        inv_system.equipped['weapon'] = copy.copy(items.stn_dag)

    elif player.class_ == "ranger":
        misc_vars['mp_p'] += 2
        player.p_attk += 3
        player.m_dfns += 1
        player.evad += 2
        player.spd += 2
        inv_system.equipped['weapon'] = copy.copy(items.slg_sht)

    player.hp = copy.copy(misc_vars['hp_p'])
    player.mp = copy.copy(misc_vars['mp_p'])
    print('-'*25)


def change_settings():
    config = configparser.ConfigParser()

    if os.path.isfile("../settings.cfg"):
        config.read("../settings.cfg")

        for x in config['save_files']:
            globals()[x] = config['save_files'][x]

        for x in config['volume_levels']:
            globals()[x] = float(config['volume_levels'][x])/100

        for x in config['text_scroll']:
            globals()[x] = config['text_scroll'][x]

        sounds.change_volume()


def check_save():  # Check for save files and load the game if they're found
    global misc_vars
    global position
    global adventure_name

    print('-'*25)

    # Check each part of the save file
    print('Searching for valid save files...')

    if not os.path.isdir(save_dir):
        time.sleep(0.25)

        while msvcrt.kbhit():
            msvcrt.getwch()

        print('No save files found. Starting new game...')
        time.sleep(0.35)

        while msvcrt.kbhit():
            msvcrt.getwch()

        print('-'*25)
        create_player()
        return

    dirs = [d for d in os.listdir('Save Files') if os.path.isdir(os.path.join('Save Files', d))]
    save_files = {}
    menu_info = {}

    for directory in dirs:

        # If all save-file components exist...
        if all(map(os.path.isfile, [
            x.format(CHARACTER_NAME=directory) for x in [
                sav_acquired_gems, sav_def_bosses,
                sav_equip_items, sav_inventory,
                sav_misc_boss_info, sav_misc_vars,
                sav_play_stats, sav_position,
                sav_quests_dia, sav_spellbook]])):

            # ...then set the dictionary key equal to the newly-formatted save file names
            save_files[directory] = [x.format(CHARACTER_NAME=directory) for x in [
                sav_acquired_gems, sav_def_bosses,
                sav_equip_items, sav_inventory,
                sav_misc_boss_info, sav_misc_vars,
                sav_play_stats, sav_position,
                sav_quests_dia, sav_spellbook]]

            try:
                with open('/'.join(['Save Files', directory, "menu_info.txt"]),
                          encoding='utf-8') as f:
                    menu_info[directory] = f.read()
            except FileNotFoundError:
                menu_info[directory] = "Unable to load preview info"

    time.sleep(0.25)

    while msvcrt.kbhit():
        msvcrt.getwch()

    if not save_files:
        print('No save files found. Starting new game...')
        time.sleep(0.35)

        while msvcrt.kbhit():
            msvcrt.getwch()

        print('-'*25)
        create_player()

        return

    print('-'*25)
    print('Found {0} valid save file(s): '.format(len(save_files)))

    padding = len(max([index for index in save_files], key=len))

    spam = True
    while spam:
        print('     ', '\n      '.join(
            ['[{0}] {1}{2} | {3}'.format(num + 1, dir_name,
                                         ' '*(padding - len(dir_name)),
                                         menu_info[dir_name])
             for num, dir_name in enumerate([key for key in sorted(save_files)])]))

        while True:
            chosen = input('Input [#] (or type "create new"): ')
            try:
                chosen = int(chosen) - 1
                if chosen < 0:
                    continue

            except ValueError:
                chosen = chosen.lower()

                if chosen == "create new":
                    print('-'*25)
                    create_player()
                    return

                else:
                    continue

            try:
                adventure_name = sorted(save_files)[chosen]
            except IndexError:
                continue

            format_save_names()

            print('-'*25)
            print('Loading Save File: "{0}"...'.format(sorted(save_files)[chosen]))
            time.sleep(0.25)

            while msvcrt.kbhit():
                msvcrt.getwch()

            try:  # Attempt to open the save files and translate
                # them into objects/dictionaries

                with open(sav_def_bosses, encoding='utf-8') as f:
                    bosses.defeated_bosses = list(json.load(f))

                with open(sav_misc_vars, encoding='utf-8') as f:
                    misc_vars = json.load(f)

                with open(sav_position, encoding='utf-8') as f:
                    position = json.load(f)

                items.deserialize_gems(sav_acquired_gems)
                inv_system.deserialize_equip(sav_equip_items)
                inv_system.deserialize_inv(sav_inventory)
                bosses.deserialize_bosses(sav_misc_boss_info)
                deserialize_player(sav_play_stats)
                npcs.deserialize_dialogue(sav_quests_dia)
                magic.deserialize_sb(sav_spellbook)

                if 'status_ail' not in player.__dict__ or 'per' not in misc_vars:
                    print('Attemping to make save file compatible with v0.6.2...')
                    if 'status_ail' not in player.__dict__:
                        player.status_ail = 'none'
                    if 'per' not in misc_vars:
                        misc_vars['per'] = 1
                    print('Attempt successful!')

                if 'access' not in inv_system.inventory or 'access' not in inv_system.equipped \
                        or 'pet' not in inv_system.equipped \
                        or('luc' in misc_vars and 'for' not in misc_vars):

                    print('Attempting to make save file compatible with v0.6.4...')
                    if 'access' not in inv_system.inventory:
                        inv_system.inventory['access'] = []

                    if 'access' not in inv_system.equipped:
                        inv_system.equipped['access'] = '(None)'

                    if 'pet' not in inv_system.equipped:
                        inv_system.equipped['pet'] = '(None)'

                    if 'luc' in misc_vars and 'for' not in misc_vars:
                        misc_vars['for'] = misc_vars['luc']
                        del misc_vars['luc']

                    print('Attempt successful!')

                print('Load successful.')

                if not towns.search_towns(position['x'], position['y'], enter=False):
                    print('-'*25)
                return

            except (OSError, ValueError):
                logging.exception('Error loading game:')
                input('There was an error loading your game | Press Enter/Return ')
                print('-'*25)
                break


def save_game():
    while True:
        y_n = input('Do you wish to save your progress? | Yes or No: ')

        y_n = y_n.lower()

        if y_n.startswith('y'):
            print('Saving...')
            time.sleep(0.25)

            while msvcrt.kbhit():
                msvcrt.getwch()

            # Check if the save directory already exists, and create it if it doesn't
            if not os.path.exists('/'.join([save_dir, adventure_name])):
                os.makedirs('/'.join([save_dir, adventure_name]))

            format_save_names()

            try:
                with open(sav_def_bosses, mode='w', encoding='utf-8') as f:
                    json.dump(bosses.defeated_bosses, f, indent=4, separators=(', ', ': '))

                with open(sav_misc_vars, mode='w', encoding='utf-8') as f:
                    json.dump(misc_vars, f, indent=4, separators=(', ', ': '))

                with open(sav_position, mode='w', encoding='utf-8') as f:
                    json.dump(position, f, indent=4, separators=(', ', ': '))

                items.serialize_gems(sav_acquired_gems)
                inv_system.serialize_equip(sav_equip_items)
                inv_system.serialize_inv(sav_inventory)
                bosses.serialize_bosses(sav_misc_boss_info)
                serialize_player(sav_play_stats)
                npcs.serialize_dialogue(sav_quests_dia)
                magic.serialize_sb(sav_spellbook)

                with open('/'.join([save_dir, adventure_name, 'menu_info.txt']),
                          mode='w', encoding='utf-8') as f:
                    f.write("{0} | LVL: {1} | Class: {2}".format(player.name,
                                                                 player.lvl,
                                                                 player.class_.title()))

                print('Save successful.')
                return

            except (OSError, ValueError):
                logging.exception('Error saving game:')
                input('There was an error saving your game (Press Enter/Return)')

        elif y_n.startswith('n'):
            return


def serialize_player(path):  # Save the "PlayerCharacter" object as a JSON file
    with open(path, mode='w', encoding='utf-8') as e:
        json.dump(player.__dict__, e, indent=4, separators=(', ', ': '))


def deserialize_player(path):  # Load the JSON file and translate
    # it into a "PlayerCharacter" object
    global player

    player = PlayerCharacter('', 15, 4, 3, 1, 3, 1, 3, 1, 3, 1, 1, 0, 1, 0, 0)

    with open(path, encoding='utf-8') as e:
        player_dict = json.load(e)

    player.__dict__ = player_dict


title_logo = """\
 ____          _    _                    _              ____   ___     ____
|  _ \  _   _ | |_ | |__    ___   _ __  (_) _   _  ___ |  _ \ |  _ \  / ___|
| |_) || | | || __|| '_ \  / _ \ | '_ \ | || | | |/ __|| |_) || |_) || |  _
|  __/ | |_| || |_ | | | || (_) || | | || || |_| |\__ \|  _ < |  __/ | |_| |
|_|     \__, | \__||_| |_| \___/ |_| |_||_| \__,_||___/|_| \_\|_|     \____|
        |___/
PythoniusRPG {0} -- Programmed in Python by Stephen Center (RbwNjaFurret)
Licensed under the GNU GPLv3: [https://www.gnu.org/copyleft/gpl.html]
Check here often for updates: [http://www.rbwnjafurret.com/pythoniusrpg/]
------------------------------------------------------------------------------""".format(
    game_version)


def title_screen():
    pygame.mixer.music.load('Music/Prologue.ogg')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(music_vol)

    print(title_logo)

    while True:
        choice = input('[P]lay Game | [C]redits | [S]tory | [E]xit  |  Input Letter: ')

        choice = choice.lower()

        if choice.startswith('p'):
            return

        elif choice.startswith('c'):
            print('-'*25)

            try:
                pygame.mixer.music.load('Music/Credits Music for an 8-bit RPG.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)
                with open('../Credits.txt') as f:
                    for number, f.readline in enumerate(f):
                        print(''.join(f.readline.rstrip("\n").split(";")))
                        time.sleep([0.75, 1.25, 0.75, 1.25, 1, 1, 0.5, 0.5, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                    1, 1, 1, 0.5, 0.5, 1, 0.5, 0.5, 1, 0.5,
                                    0.5, 1, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,
                                    0.5, 0.5, 0.5, 0.5][number])

                    time.sleep(3)

                    pygame.mixer.music.load('Music/Prologue.ogg')
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(music_vol)

                    while msvcrt.kbhit():
                        msvcrt.getwch()

            except FileNotFoundError:
                print('The "Credits.txt" file could not be found.')

            except OSError:
                logging.exception('Error loading Credits.txt:')
                print('There was a problem opening "Credits.txt".')

            print(title_logo)

        elif choice.startswith('s'):
            print('-'*25)
            input('Press Enter/Return after each line to advance the text ')
            print('-'*25)

            try:
                pygame.mixer.music.load('Music/CopperNickel.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                with open('../pythonius_plot.txt', encoding='utf-8') as f:
                    for f.readline in f:
                        if ''.join(char for char in f.readline.split(" ") if char.isalnum()):
                            input(''.join(f.readline.rstrip("\n").split(";")))
                        else:
                            print(''.join(f.readline.rstrip("\n").split(";")))

                pygame.mixer.music.load('Music/Prologue.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

            except FileNotFoundError:
                print('The "pythonius_plot.txt" file could not be found.')

            except OSError:
                logging.exception('Error loading Pythonius Plot.txt:')
                print('There was an problem opening "Pythonius Plot.txt".')

            print('-'*25)

        elif choice.startswith('e'):
            pygame.quit()
            sys.exit()


def main():
    # Set the console title to be "PythoniusRPG [game version]"

    if os.name == 'nt':  # Windows
        ctypes.windll.kernel32.SetConsoleTitleA("PythoniusRPG {0}".format(game_version).encode())

        # Set the window size to fit the text output and character dialogue.
        os.system("mode con cols=100 lines=40")

    elif os.name == 'posix':  # Most Unix Devices
        sys.stdout.write("\x1b]2;Pythonius RPG {0}\x07".format(game_version))

    change_settings()  # Set the save file locations
    change_settings()  # Set the sound & music volume

    title_screen()
    check_save()  # Check for save files...
    world.movement_system()  # ...and then start the game


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    import npcs

    try:  # Run the game
        main()
    except Exception:  # If an exception is raised and not caught, log the error message.
        logging.exception('Got exception of main handler:')
        raise