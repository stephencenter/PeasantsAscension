#!/usr/bin/env python
# PythoniusRPG v0.7 Alpha
game_version = 'v0.7'
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

# A dictionary containing miscellaneous variables made entirely of
misc_vars = {'gp': 20, 'visited_towns': []}

# A dictionary containing all information related to the player's position
position = {'x': 0, 'y': 0, 'avg': '', 'reg': 'Central Forest',
            'reg_music': 'Music/Through the Forest.ogg',
            'h': '', 'v': '', 'prev_town': [0, 0], 'is_aethus': False}

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
import traceback
import stat

import pygame

import world
import inv_system
import battle
import magic
import bosses
import items
import sounds
import towns
import ascii_art

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

sav_position = 'Save Files/{CHARACTER_NAME}/position.json'  # Position

sav_quests_dia = 'Save Files/{CHARACTER_NAME}/quests_dia.json'  # Quests & Dialogue

sav_spellbook = 'Save Files/{CHARACTER_NAME}/spellbook.json'  # Spellbook

sav_prevtowns = 'Save Files/{CHARACTER_NAME}/prevtowns.json'  # Previously visited towns

# PCU Save Files
sav_play_stats = 'Save Files/{CHARACTER_NAME}/play_stats.json'  # Player Stats

sav_solou_stats = 'Save Files/{CHARACTER_NAME}/solou_stats.json'  # Solou's Stats

sav_xoann_stats = 'Save Files/{CHARACTER_NAME}/xoann_stats.json'  # Xoann's Stats

sav_randall_stats = 'Save Files/{CHARACTER_NAME}/randall_stats.json'  # Randall's Stats

sav_ran_af_stats = 'Save Files/{CHARACTER_NAME}/ran_af_stats.json'  # Ran'af's Stats

sav_parsto_stats = 'Save Files/{CHARACTER_NAME}/parsto_stats.json'  # Parsto's Stats

sav_adorine_stats = 'Save Files/{CHARACTER_NAME}/adorine_stats.json'  # Adorine's Stats

# NOTE 1: The save file locations can be changed in the file "settings.cfg".

# NOTE 2: If one of these files is missing, the entire game won't work,
# and as such will not be recognized as a save file anymore.

# NOTE 3: It is entirely possible (and actually very easy) to modify these
# save files to change your character's stats, items, etc. However, it CAN also
# cause the file to become corrupted if it is done incorrectly, so backup your
# files before doing so.

music_vol = 1.0  # The volume of the game, on a scale from 0 (muted) to 1.0 (loudest)
sound_vol = 1.0  # These values can be changed in the settings.cfg file

do_text_scroll = False


class PlayableCharacter:
    # A class for characters whose input can be directly controlled by the player
    def __init__(self, name, hp, mp, attk, dfns, m_attk, m_dfns, p_attk,
                 p_dfns, spd, evad, class_='', enabled=True):
        self.name = name        # Name
        self.hp = hp            # Health
        self.mp = mp            # Mana Points
        self.attk = attk        # Attack
        self.dfns = dfns        # Defense
        self.p_attk = p_attk    # Pierce Attack
        self.p_dfns = p_dfns    # Pierce Defense
        self.m_attk = m_attk    # Magic Attack
        self.m_dfns = m_dfns    # Magic Defense
        self.spd = spd          # Speed
        self.evad = evad        # Evasion
        self.enabled = enabled  # Whether the party member has been recruited or not
        self.class_ = class_    # Player Class

        self.lvl = 1              # Level
        self.exp = 0              # Experience
        self.ext_ski = 0          # Extra Skill Points
        self.ext_gol = 0          # Extra Gold Pieces
        self.ext_exp = 0          # Extra Experience
        self.element = 'none'     # Player's Element
        self.status_ail = 'none'  # Current Status Ailment
        self.req_xp = 3           # Required XP to level up
        self.battle_move = ''     # What move the character chose during battle
        self.dodge = 0            # Variable used to determine chance to dodge

        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)

        self.attributes = {'int': 1,  # Intelligence
                           'wis': 1,  # Wisdom
                           'str': 1,  # Strength
                           'con': 1,  # Constitution
                           'dex': 1,  # Dexterity
                           'per': 1,  # Perception
                           'for': 1}  # Fortune

    def player_damage(self):
        # The formula for PCUs dealing damage

        if inv_system.equipped[
            self.name if self != player else 'player'
        ]['weapon'].type_ != 'ranged':

            dam_dealt = math.ceil(
                battle.temp_stats[self.name]['attk'] - (battle.monster.dfns/2))
            dam_dealt += math.ceil(dam_dealt*inv_system.equipped[
                self.name if self != player else 'player'
            ]['weapon'].power)

            # PCUs deal 1/2 damage with melee attacks when given the weakened status ailment
            if self.status_ail == 'weakened':
                dam_dealt /= 2
                dam_dealt = math.ceil(dam_dealt)
                print('{0} deals half damage because of their weakened state!'.format(self.name))

            # Mages deal 1/2 damage with melee attacks
            if self.class_ == 'mage':
                dam_dealt /= 2
                dam_dealt = math.ceil(dam_dealt)

        else:
            dam_dealt = math.ceil(
                battle.temp_stats[self.name]['p_attk'] - (battle.monster.p_dfns/2))

            dam_dealt += math.ceil(dam_dealt*inv_system.equipped[
                self.name if self != player else 'player'
            ]['weapon'].power)

            # PCUs deal 1/2 damage with ranged attacks when given the blinded status ailment
            if self.status_ail == 'blinded':
                dam_dealt /= 2
                dam_dealt = math.ceil(dam_dealt)
                print("{0}'s poor vision reduces their attack damage by half!".format(self.name))

        # Increase or decrease the damage depending on the PSU/monster's elements
        dam_dealt = magic.eval_element(
            p_elem=inv_system.equipped[
                self.name if self != player else 'player'
            ]['weapon'].element,
            m_elem=battle.monster.element, p_dmg=dam_dealt)[0]

        # All attacks deal a minimum of one damage
        if dam_dealt < 1:
            dam_dealt = 1

        # There is a 7% chance to inflict double damage
        if random.randint(1, 100) <= 7:
            print("It's a critical hit! 2x damage!")
            dam_dealt *= 2

        # Limit the amount of damage to 999 (as if that matters)
        if dam_dealt > 999:
            dam_dealt = 999
            print('Overkill!')

        return dam_dealt

    def choose_name(self):
        while True:
            self.name = input('What is your name, young adventurer? | Input Name: ')

            if not ''.join(self.name.split()):
                continue

            alphanumeric = lambda x: re.sub(r'[|]', '', x)

            self.name = alphanumeric(self.name)

            # Flygon Jones is my real life best friend and the bug-tester for this game!
            if self.name == "Flygon Jones":
                print('Ah, Flygon Jones! My dear friend, it is good to see you again!')
                input('Press enter/return ')

                return self.name

            while True:
                y_n = input('So, your name is {0}? | Yes or No: '.format(self.name))
                y_n = y_n.lower()

                if y_n.startswith('y'):
                    return self.name

                elif y_n.startswith('n'):
                    print()
                    break

    def choose_class(self):
        while True:
            class_ = input("""{0}, which class would you like to train as?\n\
      [1] Mage: Master of the arcane arts capable of using all spells, but has low defense
      [2] Assassin: Deals damage quickly and has high speed and evasion. Can poison foes
      [3] Ranger: An evasive long-distance fighter who uses bows and deals pierce damage
      [4] Paladin: Heavy-armor user who excel at holy and healing magic and uses hammers
      [5] Monk: A master of unarmed combat. High evasion and capable of using buff spells
      [6] Warrior: High defense stats and attack. Can tank lots of hits with its high HP
Input [#]: """.format(self.name))

            try:
                class_ = {'1': "mage",
                          '2': "assassin",
                          '3': "ranger",
                          '4': "paladin",
                          '5': "monk",
                          '6': "warrior"}[class_]

            except KeyError:
                continue

            print('-'*25)

            while True:
                y_n = input('You wish to be of the {0} class? | Yes or No: '.format(
                    class_.title()))

                y_n = y_n.lower()

                if y_n.startswith('y'):
                    return class_

                elif y_n.startswith('n'):
                    print('-'*25)
                    break

    def level_up(self):
        global misc_vars
        if self.exp >= self.req_xp:
            print()
            pygame.mixer.music.load('Music/Adventures in Pixels.ogg')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(music_vol)

            # The player restores all their health and mana when they level up
            self.hp = copy.copy(self.max_hp)
            self.mp = copy.copy(self.max_mp)

            rem_points = 0  # Remaining Skill Points
            extra_points = 0  # The number of extra skill points the player will receive

            while self.exp >= self.req_xp:
                sounds.item_pickup.play()
                self.lvl += 1
                print("{0} has advanced to level {1}!".format(self.name, self.lvl))

                if self.lvl == 5:
                    print()
                    print('{0} now understands the true potential of their class!'.format(
                        self.name
                    ))
                    print('{0} can activate this potential in the form of a "class ability"'.format(
                        self.name
                    ))
                    print('once per battle. Use it wisely!')
                    print()
                    input('Press enter/return ')

                rem_points += 5
                extra_points += self.ext_ski
                magic.new_spells(self)

                if self.class_ == 'warrior':
                    # Total gain: 21 pts.
                    self.p_dfns += 4
                    self.attk += 4
                    self.dfns += 4
                    self.m_attk += 1
                    self.m_dfns += 1
                    self.spd += 1
                    self.evad += 1
                    self.hp += 4
                    self.mp += 1

                elif self.class_ == 'mage':
                    # Total gain: 21 pts.
                    self.p_dfns += 1
                    self.attk += 1
                    self.dfns += 1
                    self.m_attk += 4
                    self.m_dfns += 4
                    self.spd += 2
                    self.evad += 2
                    self.hp += 2
                    self.mp += 4

                elif self.class_ == 'assassin':
                    # Total gain: 21 pts.
                    self.p_dfns += 2
                    self.attk += 4
                    self.dfns += 2
                    self.m_attk += 2
                    self.m_dfns += 1
                    self.spd += 5
                    self.evad += 2
                    self.hp += 2
                    self.mp += 1

                elif self.class_ == 'ranger':
                    # Total gain: 21 pts.
                    self.p_attk += 4
                    self.p_dfns += 2
                    self.dfns += 1
                    self.m_attk += 1
                    self.m_dfns += 2
                    self.spd += 3
                    self.evad += 4
                    self.hp += 2
                    self.mp += 2

                elif self.class_ == 'monk':
                    # Total gain: 21 pts.
                    self.p_dfns += 1
                    self.attk += 4
                    self.dfns += 1
                    self.m_attk += 2
                    self.m_dfns += 2
                    self.spd += 3
                    self.evad += 3
                    self.hp += 3
                    self.mp += 2

                elif self.class_ == 'paladin':
                    # Total gain: 21 pts.
                    self.p_dfns += 3
                    self.attk += 3
                    self.dfns += 3
                    self.m_attk += 2
                    self.m_dfns += 3
                    self.spd += 1
                    self.evad += 1
                    self.hp += 3
                    self.mp += 2

                self.exp -= self.req_xp
                self.req_xp = math.ceil((math.pow(self.lvl*2, 2) - 1.2*self.lvl))

            print('-'*25)
            self.skill_points(rem_points, extra_points)

            self.max_hp = copy.copy(self.hp)
            self.max_mp = copy.copy(self.mp)

            print('-'*25)
            save_game()

            return

    def skill_points(self, rem_points, extra_points):
        global misc_vars

        if extra_points:
            print("{0}'s great fortune has granted them {1} additional skill points!".format(
                self.name, extra_points
            ))
            rem_points += extra_points

        while rem_points > 0:
            print('{0} has {1} skill point{2} left to spend.'.format(
                self.name, rem_points, 's' if rem_points > 1 else ''
            ))

            skill = input("""Choose a skill to advance:
    [I]ntelligence - Use powerful magic with higher magic stats and MP!
    [W]isdom - Cast powerful healing magics with higher proficiency and MP!
    [S]trength -  Smash through enemies with higher attack and defense!
    [C]onstitution - Become a tank with higher defense stats and HP!
    [D]exterity - Improve your aerobic ability with higher evade/speed stats!
    [P]erception - Eliminate your enemies with ease using higher pierce and evasion!
    [F]ortune - Increase your luck in hopes of getting more GP, XP, and skill points!
Input letter: """)

            skill = skill.lower()

            if any(map(skill.startswith, ['i', 'w', 's', 'c', 'd', 'p', 'f'])):
                if skill.startswith('i'):
                    act_skill = 'int'
                    vis_skill = 'Intelligence'

                elif skill.startswith('w'):
                    act_skill = 'wis'
                    vis_skill = 'Wisdom'

                elif skill.startswith('s'):
                    act_skill = 'str'
                    vis_skill = 'Strength'

                elif skill.startswith('c'):
                    act_skill = 'con'
                    vis_skill = 'Constitution'

                elif skill.startswith('d'):
                    act_skill = 'dex'
                    vis_skill = 'Dexterity'

                elif skill.startswith('p'):
                    act_skill = 'per'
                    vis_skill = 'Perception'

                else:
                    act_skill = 'for'
                    vis_skill = 'Fortune'

                print('-'*25)
                print('Current {0}: {1}'.format(vis_skill, self.attributes[act_skill]))
                while True:
                    y_n = input("Increase {0}'s {1}? | Yes or No: ".format(self.name, vis_skill))

                    y_n = y_n.lower()

                    if y_n.startswith('y'):
                        pass
                    elif y_n.startswith('n'):
                        print('-'*25)

                        break

                    else:
                        continue

                    if skill.startswith('i'):
                        self.m_dfns += 1
                        self.m_attk += 1
                        self.mp += 2
                        self.attributes['int'] += 1

                    elif skill.startswith('w'):
                        self.mp += 2
                        self.attributes['wis'] += 1

                    elif skill.startswith('s'):
                        self.attk += 1
                        self.p_dfns += 1
                        self.dfns += 1
                        self.attributes['str'] += 1

                    elif skill.startswith('c'):
                        self.max_hp += 1
                        self.dfns += 1
                        self.p_dfns += 1
                        self.m_dfns += 1
                        self.attributes['con'] += 1

                    elif skill.startswith('d'):
                        self.spd += 1
                        self.p_attk += 1
                        self.evad += 1
                        self.attributes['dex'] += 1

                    elif skill.startswith('p'):
                        self.p_attk += 1
                        self.p_dfns += 1
                        self.evad += 1
                        self.attributes['per'] += 1

                    elif skill.startswith('f'):
                        if self.ext_ski == 10:
                            self.ext_gol += random.randint(0, 2)
                            self.ext_exp += random.randint(0, 2)

                        else:
                            self.ext_ski += 1
                            self.ext_gol += random.randint(0, 1)
                            self.ext_exp += random.randint(0, 1)

                        self.attributes['for'] += 1

                    else:
                        continue

                    print('-'*25)
                    print("{0}'s {1} has increased!".format(self.name, vis_skill))

                    # Decrement remaining points
                    rem_points -= 1

                    print('-'*25) if rem_points else ''

                    break
        print()
        print('{0} is out of skill points.'.format(self.name))

    def player_info(self):
        print("""\
-{0}'s Stats-
Level: {1} | Class: {2} | Element: {3}
HP: {4}/{5} | MP: {6}/{7} | Status Ailment: {8}
Attack: {9} | M. Attack: {10} | P. Attack {11}
Defense: {12} | M. Defense: {13} | P. Defense {14}
Speed: {15} | Evasion: {16}
INT: {17} | WIS: {18} | STR: {19} | CON: {20} | DEX: {21} | PER: {22} | FOR: {23}
Experience Pts: {24}/{25} | Gold Pieces: {26}

-Equipped Items-
Weapon: {27}
Accessory: {28}
Armor:
  Head: {29}
  Body: {30}
  Legs: {31}""".format(self.name,
                       self.lvl, self.class_.title(), self.element.title(),
                       self.hp, self.max_hp, self.mp, self.max_mp, self.status_ail.title(),
                       self.attk, self.m_attk, self.p_attk,
                       self.dfns, self.m_dfns, self.p_dfns,
                       self.spd, self.evad,
                       self.attributes['int'], self.attributes['wis'],
                       self.attributes['str'], self.attributes['con'],
                       self.attributes['dex'], self.attributes['per'],
                       self.attributes['for'],
                       self.exp, self.req_xp, misc_vars['gp'],
                       inv_system.equipped[
                           self.name if self != player else 'player'
                       ]['weapon'], inv_system.equipped[
                           self.name if self != player else 'player'
                       ]['access'],
                       inv_system.equipped[
                           self.name if self != player else 'player'
                       ]['head'],
                       inv_system.equipped[
                           self.name if self != player else 'player'
                       ]['body'],
                       inv_system.equipped[
                           self.name if self != player else 'player'
                       ]['legs']))

        print('-'*25)
        input('Press enter/return ')

    def battle_turn(self, is_boss):
        monster = battle.monster
        while True:
            # "2" refers to magic, which will print this later
            if self.move != '2':
                print("\n-{0}'s Turn-".format(self.name))

            # Basic Attack
            if self.move == '1' or self.move == 'q':
                print(ascii_art.player_art[self.class_.title()] %
                      "{0} is making a move!\n".format(self.name))

                if inv_system.equipped[
                    self.name if self != player else 'player'
                ]['weapon'].type_ in ['melee', 'magic']:

                    sounds.sword_slash.play()
                    print('{0} begin to fiercely attack the {1} using their {2}...'.format(
                        self.name, monster.name, str(inv_system.equipped[
                            self.name if self != player else 'player'
                        ]['weapon'])))

                # Ranged weapons aren't swung, so play a different sound effect
                else:
                    sounds.aim_weapon.play()
                    print('{0} aims carefully at the {1} using their {2}...'.format(
                        self.name, monster.name, str(inv_system.equipped[
                            self.name if self != player else 'player'
                        ]['weapon'])))

                time.sleep(0.75)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                # Check for attack accuracy
                if self.dodge in range(monster.evad, 512):
                    dam_dealt = self.player_damage()
                    monster.hp -= dam_dealt
                    sounds.enemy_hit.play()
                    print("{0}'s attack connects with the {1}, dealing {2} damage!".format(
                        self.name, monster.name, dam_dealt))

                else:
                    sounds.attack_miss.play()
                    print("The {0} dodges {1}'s attack with ease!".format(monster.name, self.name))

            # Class Ability
            elif self.move == '3':
                if not self.class_ability():
                    return False

            # RUN AWAY!!!
            elif self.move == '5':
                if battle.run_away(self):
                    # Attempt to run.
                    # If it succeeds, end the battle without giving the player a reward
                    print('-'*25)
                    pygame.mixer.music.load(position['reg_music'])
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(music_vol)

                    return 'Ran'

            else:
                return False

            # Check to see if the PCU is poisoned
            if self.status_ail == 'poisoned' and monster.hp > 0:
                if random.randint(0, 3):
                    time.sleep(0.5)

                    while msvcrt.kbhit():
                        msvcrt.getwch()

                    sounds.poison_damage.play()

                    poison_damage = math.floor(self.hp/4)
                    print('{0} took poison damage! (-{1} HP)'.format(self.name, poison_damage))
                    self.hp -= poison_damage

                    if self.hp <= 0:
                        break

                else:
                    time.sleep(0.5)

                    while msvcrt.kbhit():
                        msvcrt.getwch()

                    sounds.buff_spell.play()
                    input('{0} starts to feel better! | Press enter/return '.format(self.name))
                    self.status_ail = 'none'

            # Check to see if the PCU is silenced
            elif self.status_ail != 'none' and self.status_ail != 'asleep':
                if not random.randint(0, 3):

                    time.sleep(0.5)

                    while msvcrt.kbhit():
                        msvcrt.getwch()

                    sounds.buff_spell.play()

                    input("{0}'s afflictions have worn off! | Press enter/return ".format(
                        self.name))
                    self.status_ail = 'none'

            if is_boss and monster.multiphase and monster.hp <= 0:
                monster.battle_turn(is_boss)

            return True

    def player_choice(self):
        # Creates a lambda function that strips all non-numeric characters
        # This fixes some (possible) problems later on
        only_num = lambda x: re.compile(r'[^\d]+').sub('', x)

        print("""\
Pick {0}'s Move:
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""".format(self.name))

        while True:
            move = input("Input [#]: ")
            if move != "q":
                # Strip out all non-numeric input
                move = only_num(move)

            if move.isdigit() and int(move) in range(1, 6) or \
                    (move == 'q' and self.name == "Flygon Jones"):

                # Use Magic
                if move == '2':
                    print('-'*25)
                    if not magic.pick_cat(self):
                        print("""\
Pick {0}'s Move:
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""".format(self.name))

                        continue

                    input('\nPress enter/return ')

                # Battle Inventory
                elif move == '4':
                    print('-'*25)
                    if not battle.battle_inventory(self):
                        print("""\
Pick {0}'s Move:
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""".format(self.name))

                        continue

                    input('\nPress enter/return ')

                # Let the player repick if they try to use their class ability when they can't
                elif move == '3':
                    if self.lvl < 5:
                        # You must be at least level 5 to use your class ability
                        print("{0} has not yet realized their class's inner potential \
(must be level 5 to use)\n".format(self.name))
                        input('Press enter/return ')

                        print('-'*25)
                        print("""\
Pick {0}'s Move:
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""".format(self.name))

                        continue

                    elif battle.temp_stats[self.name]['ability_used']:
                        # You can only use your ability once per battle.
                        print('{0} feels drained, and are unable to call upon their class\
ability again.\n')
                        input('Press enter/return ')

                        print('-'*25)
                        print("""\
Pick {0}'s Move:
      [1]: Attack
      [2]: Use Magic
      [3]: Class Ability
      [4]: Use Items
      [5]: Run""".format(self.name))

                        continue

                self.move = move

                return

    def class_ability(self):
        # Class abilities are special abilities only available to characters of certain classes.
        # Their purpose is to help make the characters more diverse, as well as encourage more
        # strategy being used.

        monster = battle.monster
        battle.temp_stats[self.name]['ability_used'] = True

        print(ascii_art.player_art[self.class_.title()] %
              "{0} is making a move!\n".format(self.name))

        print("{0} uses the knowledge they've gained to unleash their class ability!".format(
            self.name
        ))

        # Ranger Ability: Scout
        if self.class_ == 'ranger':
            # The ranger class identifies their enemy and prints their stats.
            # This is really useful for defeating bosses, which are often weak to
            # certain types and elements of attacks.

            print('-'*25)
            print('ABILITY: SCOUT')
            print('-'*25)

            print('As a Ranger, {0} identifies their enemy and focuses\
, increasing their pierce attack!'.format(self.name))

            input("Press enter/return to view your enemy's stats ")

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

            battle.temp_stats[self.name]['p_attk'] *= 1.2
            battle.temp_stats[self.name]['p_attk'] =\
                math.ceil(battle.temp_stats[self.name]['p_attk'])

            return True

        # Warrior Ability: Warrior's Spirit
        elif self.class_ == 'warrior':

            if 20 < 0.2*self.hp:
                self.hp += 0.2*self.hp
                self.hp = math.ceil(self.hp)
            else:
                self.hp += 20

            p_temp_stats['dfns'] *= 1.2
            p_temp_stats['m_dfns'] *= 1.2
            p_temp_stats['p_dfns'] *= 1.2

            print('-'*25)
            print("ABILITY: WARRIOR'S SPIRIT")
            print('-'*25)

            print('As a Warrior, you channel your inner-strength and restore health and defense!')

            if self.hp > self.max_hp:
                self.hp -= (self.hp - self.max_hp)
            if self.mp > self.max_mp:
                self.mp -= (self.mp - self.max_mp)

            return True

        # Mage Ability: Artificial Intelligence
        elif self.class_ == "mage":
            self.mp += copy.copy(self.max_mp)/2

            if self.mp > self.max_mp:
                self.mp = copy.copy(self.max_mp)

            self.mp = math.ceil(self.mp)

            battle.temp_stats[self.name]['m_attk'] *= 1.2
            battle.temp_stats[self.name]['m_dfns'] *= 1.2

            print('-'*25)
            print("ABILITY: ARTIFICIAL INTELLIGENCE")
            print('-'*25)

            print('As a Mage, you focus intently and sharply increase your magical prowess!')
            print('Your magic attack and defense increase, and you regain MP!')

            return True

        # Assassin Ability: Poison Injection
        elif self.class_ == "assassin":
            monster.is_poisoned = True

            print('-'*25)
            print("ABILITY: POISON INJECTION")
            print('-'*25)

            print('As an Assassin, you discreetly inject poison into your enemy!')

            return True

        # Paladin Ability: Divine Intervention
        elif self.class_ == "paladin":
            print('-'*25)
            print('ABILITY: DIVINE INTERVENTION')
            print('-'*25)

            print('As a Paladin, you call upon the power of His Divinity to aid you!')
            print('You enemy has been turned to the "death" element, causing your')
            print('holy spells to inflict more damage! You also regain health and MP.')

            monster.element = "death"

            if 15 < 0.15*self.hp:
                self.hp += 0.1*self.hp
                self.hp = math.ceil(self.hp)
            else:
                self.hp += 15

            if 15 < 0.15*self.mp:
                self.mp += 0.1*self.mp
                self.mp = math.ceil(self.mp)
            else:
                self.mp += 15

            if self.hp > self.max_hp:
                self.hp -= (self.hp - self.max_hp)
            if self.mp > self.max_mp:
                self.mp -= (self.mp - self.max_mp)

            return True

        # Monk Ability: Chakra-smash
        elif self.class_ == 'monk':
            # Essentially a 2.5x crit. As an added bonus, this attack has a 14%
            # chance to get a crit itself, resulting in a total of an 5x critical.
            # This attack lowers your defenses by 25% for three turns to balance it out.
            # If you are weakened, this attack ignores that and will deal full damage anyway.
            print('-'*25)
            print('ABILITY: CHAKRA-SMASH')
            print('-'*25)

            print('As a monk, {0} meditates and focus their inner chi.'.format(self.name))
            print('After a brief moment of confusion from the enemy, {0} strikes, dealing'.format(
                self.name))
            print("an immense amount of damage in a single, powerful strike! As a result, {0}'s\
".format(self.name))
            print('defenses have been lowered by 25% for three turns.')
            print()

            dam_dealt = math.ceil(p_temp_stats['attk']/2 - (monster.dfns/1.25))
            dam_dealt += math.ceil(dam_dealt*inv_system.equipped[
                self.name if self != player else 'player'
            ]['weapon'].power)

            dam_dealt = magic.eval_element(
                p_elem=inv_system.equipped[
                    self.name if self != player else 'player'
                ]['weapon'].element,
                m_elem=monster.element, p_dmg=dam_dealt)[0]

            dam_dealt *= 2.5
            dam_dealt = math.ceil(dam_dealt)

            if dam_dealt < 4:
                dam_dealt = 4

            if random.randint(1, 100) <= 14:
                print("It's a critical hit! 2x damage!")
                print('Overkill!')
                dam_dealt *= 2

            if dam_dealt > 999:
                dam_dealt = 999

            print('The attack deals {0} damage to the {1}!'.format(dam_dealt, monster.name))

            battle.temp_stats[self.name]['dfns'] /= 1.25
            battle.temp_stats[self.name]['m_dfns'] /= 1.25
            battle.temp_stats[self.name]['p_dfns'] /= 1.25

            battle.temp_stats[self.name]['dfns'] = math.floor(
                battle.temp_stats[self.name]['dfns'])

            battle.temp_stats[self.name]['m_dfns'] = math.floor(
                battle.temp_stats[self.name]['m_dfns'])

            battle.temp_stats[self.name]['p_dfns'] = math.floor(
                battle.temp_stats[self.name]['p_dfns'])

            monster.hp -= dam_dealt

            return True


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

                    if player.name == "Flygon Jones":
                        print()
                        print("Since you're my friend, I'm going to give you a small gift: An")
                        print("additional 50 GP to use on your travels, \
as well as an extra potion!")

                        input('Press enter/return ')

                        inv_system.inventory['consum'].append(items.s_potion)
                        misc_vars['gp'] += 50

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
                     'sav_quests_dia', 'sav_spellbook',
                     'sav_prevtowns', 'sav_solou_stats',
                     'sav_xoann_stats', 'sav_randall_stats',
                     'sav_adorine_stats', 'sav_ran_af_stats',
                     'sav_parsto_stats'], key=str.lower):

        spam = globals()[x]
        globals()[x] = '/'.join([save_dir, adventure_name, spam.split('/')[2]])


def create_player():
    global player
    global misc_vars

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    # Set the player's max HP and MP
    player.max_hp = copy.copy(player.hp)
    player.max_mp = copy.copy(player.mp)

    player.name = player.choose_name()
    print()
    player.class_ = player.choose_class()
    print()
    set_adventure_name()

    if player.class_ == "warrior":
        player.max_hp += 5
        player.max_mp -= 1
        player.dfns += 3
        player.p_dfns += 2
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.wdn_sht)

    elif player.class_ == "mage":
        player.max_hp += 1
        player.max_mp += 6
        player.m_attk += 4
        player.m_dfns += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.mag_twg)

    elif player.class_ == "assassin":
        player.max_hp += 2
        player.max_mp += 1
        player.attk += 3
        player.dfns += 2
        player.spd += 4
        player.evad += 2
        inv_system.equipped['player']['weapon'] = copy.copy(items.stn_dag)

    elif player.class_ == "ranger":
        player.max_mp += 2
        player.p_attk += 4
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        inv_system.equipped['player']['weapon'] = copy.copy(items.slg_sht)

    elif player.class_ == "monk":
        player.max_hp += 2
        player.max_mp += 2
        player.attk += 3
        player.m_dfns += 2
        player.evad += 3
        player.spd += 3
        player.dfns -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.fists)

    elif player.class_ == "paladin":
        player.max_hp += 3
        player.max_mp += 4
        player.m_dfns += 3
        player.m_attk += 3
        player.dfns += 3
        player.p_dfns += 3
        player.attk += 3
        player.spd -= 1
        player.evad -= 1
        inv_system.equipped['player']['weapon'] = copy.copy(items.rbr_mlt)

    player.hp = copy.copy(player.max_hp)
    player.mp = copy.copy(player.max_mp)
    print('-'*25)


def change_settings():
    config = configparser.ConfigParser()

    if os.path.isfile("../settings.cfg"):
        config.read("../settings.cfg")

        for x in config['save_files']:
            globals()[x] = config['save_files'][x]

        for x in config['volume_levels']:
            globals()[x] = float(config['volume_levels'][x])/100

        for x in config['do_text_scroll']:
            if config['do_text_scroll'][x] in ['False', 'True']:
                globals()[x] = eval(config['do_text_scroll'][x])
            else:
                globals()[x] = True

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
    save_file_list = [
        sav_acquired_gems, sav_def_bosses,
        sav_equip_items, sav_inventory,
        sav_misc_boss_info, sav_misc_vars,
        sav_play_stats, sav_position,
        sav_quests_dia, sav_spellbook,
        sav_prevtowns, sav_solou_stats,
        sav_xoann_stats
    ]

    for directory in dirs:
        if not os.path.isfile(sav_prevtowns.format(CHARACTER_NAME=directory))\
                and all([os.path.isfile(file.format(CHARACTER_NAME=directory))
                         for file in save_file_list[:-1]]):

                with open(sav_prevtowns.format(CHARACTER_NAME=directory),
                          mode='w', encoding='utf-8') as f:
                    json.dump(misc_vars['visited_towns'], f, indent=4, separators=(', ', ': '))

        # If all save-file components exist...
        if all(map(os.path.isfile, [x.format(CHARACTER_NAME=directory) for x in save_file_list])):

            # ...then set the dictionary key equal to the newly-formatted save file names
            save_files[directory] = [x.format(CHARACTER_NAME=directory) for x in save_file_list]

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
        # If there are no found save files, then have the player make a new character
        print('No save files found. Starting new game...')
        time.sleep(0.35)

        while msvcrt.kbhit():
            msvcrt.getwch()

        print('-'*25)
        create_player()

        return

    print('-'*25)
    print('Found {0} valid save file(s): '.format(len(save_files)))

    # padding is a number that the game uses to determine how much whitespace is needed
    # to make certain visual elements line up on the screen.
    padding = len(max([index for index in save_files], key=len))

    spam = True
    while spam:
        # Print information about each save file and allow the player to choose which
        # file to open
        print('     ', '\n      '.join(
            ['[{0}] {1}{2} | {3}'.format(num + 1, dir_name,
                                         ' '*(padding - len(dir_name)),
                                         menu_info[dir_name])
             for num, dir_name in enumerate([key for key in sorted(save_files)])]))

        while True:
            chosen = input('Input [#] (or type "create new"): ')
            try:
                # Account for the fact that list indices start at 0
                chosen = int(chosen) - 1
                if chosen < 0:
                    continue

            except ValueError:
                chosen = chosen.lower()

                # Let the player create a new save file
                if chosen.startswith("c"):
                    print('-'*25)
                    create_player()
                    return

                else:
                    continue

            try:
                # Sort the save file names in alphanumerical order
                adventure_name = sorted(save_files)[chosen]
            except IndexError:
                continue

            format_save_names()

            print('-'*25)
            print('Loading Save File: "{0}"...'.format(sorted(save_files)[chosen]))
            time.sleep(0.25)

            while msvcrt.kbhit():
                msvcrt.getwch()

            # Attempt to open the save files and translate
            # them into objects/dictionaries
            try:

                with open(sav_def_bosses, encoding='utf-8') as f:
                    bosses.defeated_bosses = list(json.load(f))

                with open(sav_misc_vars, encoding='utf-8') as f:
                    misc_vars = json.load(f)

                with open(sav_position, encoding='utf-8') as f:
                    position = json.load(f)

                # Call functions to serialize more advanced things
                items.deserialize_gems(sav_acquired_gems)
                inv_system.deserialize_equip(sav_equip_items)
                inv_system.deserialize_inv(sav_inventory)
                bosses.deserialize_bosses(sav_misc_boss_info)
                npcs.deserialize_dialogue(sav_quests_dia)
                magic.deserialize_sb(sav_spellbook)

                deserialize_player(
                    sav_play_stats,
                    sav_solou_stats,
                    sav_xoann_stats,
                    sav_adorine_stats,
                    sav_randall_stats,
                    sav_ran_af_stats,
                    sav_parsto_stats
                )

                print('Load successful.')

                if not towns.search_towns(position['x'], position['y'], enter=False):
                    print('-'*25)
                return

            except (OSError, ValueError):
                logging.exception('Error loading game:')
                input('There was an error loading your game | Press enter/return ')
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
            try:
                os.makedirs('/'.join([save_dir, adventure_name]))
            except FileExistsError:
                pass

            format_save_names()

            try:
                with open(sav_def_bosses, mode='w', encoding='utf-8') as f:
                    json.dump(bosses.defeated_bosses, f, indent=4, separators=(', ', ': '))

                with open(sav_misc_vars, mode='w', encoding='utf-8') as f:
                    json.dump(misc_vars, f, indent=4, separators=(', ', ': '))

                with open(sav_position, mode='w', encoding='utf-8') as f:
                    json.dump(position, f, indent=4, separators=(', ', ': '))

                with open(sav_prevtowns, mode='w', encoding='utf-8') as f:
                    json.dump(misc_vars['visited_towns'], f, indent=4, separators=(', ', ': '))

                items.serialize_gems(sav_acquired_gems)
                inv_system.serialize_equip(sav_equip_items)
                inv_system.serialize_inv(sav_inventory)
                bosses.serialize_bosses(sav_misc_boss_info)
                npcs.serialize_dialogue(sav_quests_dia)
                magic.serialize_sb(sav_spellbook)

                serialize_player(
                    sav_play_stats,
                    sav_solou_stats,
                    sav_xoann_stats,
                    sav_adorine_stats,
                    sav_randall_stats,
                    sav_ran_af_stats,
                    sav_parsto_stats
                )

                with open('/'.join([save_dir, adventure_name, 'menu_info.txt']),
                          mode='w', encoding='utf-8') as f:
                    f.write("{0} | LVL: {1} | Class: {2}".format(player.name,
                                                                 player.lvl,
                                                                 player.class_.title()))

                print('Save successful.')
                return

            except (OSError, ValueError):
                logging.exception('Error saving game:')
                input('There was an error saving your game (Press enter/return)')

        elif y_n.startswith('n'):
            return


def serialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Save the "PlayableCharacter" objects as JSON files

    with open(path, mode='w', encoding='utf-8') as f:
        json.dump(player.__dict__, f, indent=4, separators=(', ', ': '))
    with open(s_path, mode='w', encoding='utf-8') as f:
        json.dump(solou.__dict__, f, indent=4, separators=(', ', ': '))
    with open(x_path, mode='w', encoding='utf-8') as f:
        json.dump(xoann.__dict__, f, indent=4, separators=(', ', ': '))
    with open(a_path, mode='w', encoding='utf-8') as f:
        json.dump(adorine.__dict__, f, indent=4, separators=(', ', ': '))
    with open(r_path, mode='w', encoding='utf-8') as f:
        json.dump(randall.__dict__, f, indent=4, separators=(', ', ': '))
    with open(f_path, mode='w', encoding='utf-8') as f:
        json.dump(ran_af.__dict__, f, indent=4, separators=(', ', ': '))
    with open(p_path, mode='w', encoding='utf-8') as f:
        json.dump(parsto.__dict__, f, indent=4, separators=(', ', ': '))


def deserialize_player(path, s_path, x_path, a_path, r_path, f_path, p_path):
    # Load the JSON files and translate them into "PlayableCharacter" objects
    global player
    global solou
    global xoann
    global adorine
    global randall
    global ran_af
    global parsto

    player = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    solou = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    xoann = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    adorine = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    randall = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    ran_af = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)
    parsto = PlayableCharacter('', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3)

    with open(path, encoding='utf-8') as f:
        player.__dict__ = json.load(f)
    with open(s_path, encoding='utf-8') as f:
        solou.__dict__ = json.load(f)
    with open(x_path, encoding='utf-8') as f:
        xoann.__dict__ = json.load(f)
    with open(a_path, encoding='utf-8') as f:
        adorine.__dict__ = json.load(f)
    with open(r_path, encoding='utf-8') as f:
        randall.__dict__ = json.load(f)
    with open(f_path, encoding='utf-8') as f:
        ran_af.__dict__ = json.load(f)
    with open(p_path, encoding='utf-8') as f:
        parsto.__dict__ = json.load(f)


# This is the logo that's displayed on the titlescreen
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
        # Give the user a choice of keys to press to do specific actions
        choice = input('[P]lay Game | [C]redits | [S]tory | [L]ore | [E]xit  |  Input Letter: ')

        choice = choice.lower()

        if choice.startswith('p'):
            return

        elif choice.startswith('c'):
            print('-'*25)

            try:
                pygame.mixer.music.load('Music/Credits Music for an 8-bit RPG.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display the credits one line at a time with specific lengths
                # of time in between each line.
                # These periods of time line up with the music that should be playing
                # at the specific time.
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
                # Display this is the Credits.txt file couldn't be found
                print('The "Credits.txt" file could not be found.')

            except OSError:
                # If there is a problem opening the Credits.txt file, but it does exist,
                # display this message and log the error
                logging.exception('Error loading Credits.txt:')
                print('There was a problem opening "Credits.txt".')

            print(title_logo)

        elif choice.startswith('s'):
            # Display the storyline of the game
            print('-'*25)
            input('Press enter/return after each line to advance the text ')
            print('-'*25)

            try:
                pygame.mixer.music.load('Music/CopperNickel.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display each line one at a time, and require the pressing of enter
                # on lines that aren't solely whitespace
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
                # Display this is the pythonius_plot.txt file couldn't be found
                print('The "pythonius_plot.txt" file could not be found.')

            except OSError:
                # If there is a problem opening the pythonius_plot.txt file, but it does exist,
                # display this message and log the error
                logging.exception('Error loading pythonius_plot.txt:')
                print('There was an problem opening "pythonius_plot.txt".')

            print('-'*25)

        elif choice.startswith('l'):
            # Display side-story lore and the history of Pythonia
            print('-'*25)
            input('Press enter/return after each line to advance the text ')
            print('-'*25)

            try:
                pygame.mixer.music.load('Music/CopperNickel.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

                # Display each line one at a time, and require the pressing of enter
                # on lines that aren't solely whitespace
                with open('../pythonius_lore.txt', encoding='utf-8') as f:
                    for f.readline in f:
                        if ''.join(char for char in f.readline.split(" ") if char.isalnum()):
                            input(''.join(f.readline.rstrip("\n").split(";")))
                        else:
                            print(''.join(f.readline.rstrip("\n").split(";")))

                pygame.mixer.music.load('Music/Prologue.ogg')
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(music_vol)

            except FileNotFoundError:
                print('The "pythonius_lore.txt" file could not be found.')

            except OSError:
                logging.exception('Error loading pythonius_lore.txt:')
                print('There was an problem opening "pythonius_lore.txt".')

            print('-'*25)

        elif choice.startswith('e'):
            # Exit the game
            pygame.quit()
            sys.exit()


# Configure the properties of the command prompt so that everything fits/looks right
def set_prompt_properties():

    # Calculate the screen size of the player
    screensize = ctypes.windll.user32.GetSystemMetrics(0),\
        ctypes.windll.user32.GetSystemMetrics(1)

    class Coord(ctypes.Structure):
        _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

    class ConsoleFontInfo(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_ulong),
                    ("nFont", ctypes.c_ulong),
                    ("dwFontSize", Coord),
                    ("FontFamily", ctypes.c_uint),
                    ("FontWeight", ctypes.c_uint),
                    ("FaceName", ctypes.c_wchar*32)]

    font = ConsoleFontInfo()
    font.cbSize = ctypes.sizeof(ConsoleFontInfo)
    font.nFont = 12

    # Adjust for screen sizes
    font.dwFontSize.X = 8 if screensize[0] < 1024 else 10 \
        if screensize[0] < 1280 else 12 if screensize[0] < 1920 else 15
    font.dwFontSize.Y = 14 if screensize[0] < 1024 else 18 \
        if screensize[0] < 1280 else 22 if screensize[1] < 1080 else 28

    font.FontFamily = 54
    font.FontWeight = 400
    font.FaceName = "Lucida Console"

    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))

    # Calculate the proper width for the buffer size and then set the height to be 200
    # A height of 200 should allow the player to scroll back up to read previous events if needs
    # be.
    # os.system("@echo off")
    # os.system("conSize.bat {0} {1} {2} {3}".format(
    #     math.ceil(screensize[0]/font.dwFontSize.X),
    #     math.ceil(screensize[1]/font.dwFontSize.Y),
    #     math.ceil(screensize[0]/font.dwFontSize.X),
    #     200)
    # )

    # Set the console title
    ctypes.windll.kernel32.SetConsoleTitleA("PythoniusRPG {0}".format(game_version).encode())


def copy_error(text):
    # This is a modified verstion of Albert Sweigart's "Pyperclip" module.
    # It is licensed under the BSD (link: http://opensource.org/licenses/BSD-2-Clause)
    # I removed a large portion of it due to it being unnessesary, and changed the variable names
    # to match my naming conventions.

    d = ctypes.windll
    d.user32.OpenClipboard(None)
    d.user32.EmptyClipboard()
    hcd = d.kernel32.GlobalAlloc(0x2000, len(text.encode('utf-16-le')) + 2)
    pch_data = d.kernel32.GlobalLock(hcd)
    ctypes.cdll.msvcrt.wcscpy(ctypes.c_wchar_p(pch_data), text)
    d.kernel32.GlobalUnlock(hcd)
    d.user32.SetClipboardData(13, hcd)
    d.user32.CloseClipboard()


def main():
    # main() handles all the setup for the game, and includes the main game loop.
    # Everything happens in this function in one way or another.

    set_prompt_properties()  # Set the CMD size and whatnot...
    change_settings()  # ...set the volume and save file settings...
    title_screen()  # ...display the titlescreen...
    check_save()  # ...check for save files...
    world.movement_system()  # ...and then start the game.


if __name__ == "__main__":  # If this file is being run and not imported, run main()
    import npcs

    # Establish all three characters as global variables
    player = ''

    # Pronounced "So-low"
    solou = PlayableCharacter('Solou', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                              class_='mage', enabled=False)

    # Pronounced "Zo-ann"
    xoann = PlayableCharacter('Xoann', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                              class_='assassin', enabled=False)

    # Pronounced "Adore-een"
    adorine = PlayableCharacter('Adorine', 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                                class_='warrior', enabled=False)

    # Pronounced "Rahn-ahf"
    ran_af = PlayableCharacter("Ran'Af", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                               class_='monk', enabled=False)

    # Pronounced "Parse-toe"
    parsto = PlayableCharacter("Parsto", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                               class_='ranger', enabled=False)

    # Pronounced "Ran-dull"
    randall = PlayableCharacter("Randall", 20, 5, 8, 5, 8, 5, 8, 5, 6, 3,
                                class_='paladin', enabled=False)

    # Yes, this is a try...except statement that includes functions that span
    # over 8000 lines, but it's necessary for error logging.
    try:
        # Run the game.
        main()

    except Exception as e:
        # If an exception is raised and not caught, log the error message.

        logging.exception('Got exception of main handler:')
        pygame.mixer.music.stop()
        print(traceback.format_exc())

        print('''PythoniusRPG encountered an error and crashed! The error message above should
be sent immediately to RbwNjaFurret (ninjafurret@gmail.com) to make sure the bug gets fixed.
The error message can be immediately copied to your clipboard if you wish.''')
        print('-'*25)

        # The player is given the option to copy it instead of just being forced, because
        # I personally hate programs that overwrite your clipboard without permission.
        while True:
            c = input('Type in "copy" to copy to your clipboard, or simply press enter to exit: ')
            if c.lower() == "copy":
                copy_error(traceback.format_exc())
                print('-'*25)
                print('The error message has been copied to your clipboard.')
                input('Press enter/return to exit ')

                raise

            elif c.lower() == '':
                raise