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

import random
import sys
import time
import math
import copy

import pygame

import inv_system
import items
import battle
import sounds
import magic


if __name__ == "__main__":
    sys.exit()
else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

player = ''
monster = ''
position = ''
misc_vars = ''
inventory = ''


class Monster:
    # All monsters use this class. Bosses use a sub-class called
    # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, m_attk,
                 m_dfns, spd, evad, lvl, element='none'):
        self.name = name  # Name
        self.hp = hp  # Health
        self.mp = mp  # Mana
        self.attk = attk  # Attack
        self.dfns = dfns  # Defense
        self.m_attk = m_attk  # Magic Attack
        self.m_dfns = m_dfns  # Magic Defense
        self.spd = spd  # Speed
        self.evad = evad  # Evasion
        self.lvl = lvl  # Level
        self.element = element  # Element
        self.items = ''

        num = random.randint(0, 5)
        if num == 4:
            self.items = random.choice(items.monster_drop(self.lvl))

    def monst_damage(self, var):
        monst_dealt = int((self.attk/2) - (battle.temp_stats['dfns']/3) + (self.lvl/3) + var + 1)

        if monst_dealt < 1:
            monst_dealt = 1

        return monst_dealt

    def monst_magic(self, var):
        monst_dealt = int((self.m_attk/2)
                          - (battle.temp_stats['m_dfns']/3)
                          + (self.lvl/3) + var + 1)

        if monst_dealt < 1:
            monst_dealt = 1

        return monst_dealt

    def monst_level(self):
        global misc_vars
        self.lvl = int((1/3)*abs(1.4*position['avg'] - 1)) + 1
        for x in range(1, self.lvl):
            self.hp += random.randint(4, 6)
            self.mp += random.randint(1, 2)
            self.attk = random.randint(1, 3)
            self.dfns += random.randint(1, 2)
            self.m_attk += random.randint(1, 3)
            self.m_dfns += random.randint(1, 2)
            self.spd += random.randint(1, 3)
            self.evad += random.randint(0, 1)

        misc_vars['hp_m'] = self.hp
        misc_vars['mp_m'] = self.mp

    def monst_attk(self, var, dodge):
        sounds.sword_slash.play()
        print('The {0} angrily begins to charge at you!'.format(self.name))
        time.sleep(0.75)

        if dodge in range(player.evad, 250):

            dealt = magic.eval_element(
                p_elem=battle.player.element,
                m_elem=battle.monster.element, m_dmg=self.monst_damage(var))[1]

            player.hp -= dealt
            sounds.enemy_hit.play()

            print('The {0} hits you, dealing {1} damage!'.format(self.name, dealt))

        else:
            sounds.attack_miss.play()
            print("You narrowly avoid the {0}'s attack!".format(self.name))

    def enemy_turn(self, var, dodge):
        # This is the Enemy's AI.

        print('\n-Enemy Turn-')
        if self.hp <= int(misc_vars['hp_m']/4) and self.mp >= 5 and random.randint(0, 1):
            # Magic heal
            sounds.magic_healing.play()

            heal = int(((self.m_attk + self.m_dfns)/2) + self.lvl/2)

            if heal < 5:
                heal = 5

            self.hp += heal
            self.mp -= 5

            print('The {0} casts a healing spell!'.format(self.name))

        elif not random.randint(0, 4) and self.mp >= 2:
            self.give_status()

        elif self.attk >= self.m_attk:
            # Physical Attack
            self.monst_attk(var, dodge)

        elif int((self.dfns + self.m_dfns)/2) <= int(self.lvl/3):
            # Defend
            self.dfns += random.randint(1, 2)
            self.m_dfns += random.randint(1, 2)
            print("The {0} assumes a more defensive stance! (+DEF, +M'DEF)".format(self.name))

        elif self.m_attk >= self.attk and self.mp >= 2:
            # Magic Attack
            sounds.magic_attack.play()

            print('The {0} is attempting to cast a strange spell...'.format(self.name))
            time.sleep(0.75)

            if dodge in range(battle.temp_stats['evad'], 250):
                dealt = magic.eval_element(
                    p_elem=battle.player.element,
                    m_elem=battle.monster.element, m_dmg=self.monst_magic(var))[1]

                player.hp -= dealt
                sounds.enemy_hit.play()

                print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                    self.name, dealt))

            else:
                sounds.attack_miss.play()
                print("The spell misses you by a landslide!")

            self.mp -= 2

        else:
            self.monst_attk(var, dodge)

    def give_status(self):
        # Attempt to give the player a status ailment
        status = random.choice([x for x in ['asleep', 'poisoned', 'silenced']
                                if x != battle.temp_stats['status_effect']])

        print('The {0} is attempting to make you {1}...'.format(self.name, status))
        time.sleep(0.75)

        if random.randint(0, 2):
            print('You are now {0}!'.format(status))
            battle.temp_stats['status_effect'] = status

        else:
            print('The {0} failed to make you {1}.'.format(self.name, status))

        self.mp -= 2

    def monst_name(self):
        monster_type = {'Shore': ['Shell Mimic', 'Giant Crab', 'Naiad',
                                  'Sea Serpent', 'Squid'],
                        'Swamp': ['Bog Slime', 'Moss Ogre', 'Sludge Rat',
                                  'Walking Venus', 'Vine Lizards'],
                        'Forest': ['Goblin', 'Beetle', 'Sprite',
                                   'Imp', 'Bat'],
                        'Desert': ['Mummy', 'Sand Golem', 'Minubis',
                                   'Fire Ant', 'Naga'],
                        'Tundra': ['Ice Soldier', 'Minor Yeti', 'Corrupt Thaumaturge',
                                   'Arctic Wolf', 'Frost Bat'],
                        'Mountain': ['Troll', 'Rock Giant', 'Oread',
                                     'Tengu', 'Giant Worm'],
                        'Graveyard': ['Zombie', 'Undead Warrior', 'Necromancer',
                                      'Skeleton', 'Ghoul']
                        }

        self.name = random.choice(monster_type[position['reg']])

        if self.name == monster_type[position['reg']][0]:
            self.enemy_turn = fighter_ai
            fighter_stats(self)

        if self.name == monster_type[position['reg']][1]:
            self.enemy_turn = tank_ai
            tank_stats(self)

        elif self.name == monster_type[position['reg']][2]:
            # Mage AI -- Not yet implemented!
            pass

        elif (self.name == monster_type[position['reg']][3] or
                self.name == monster_type[position['reg']][4]):
            # Agile AI -- Not yet implemented!
            pass

        modifiers = [
            'Slow', 'Fast',
            'Powerful', 'Ineffective',
            'Nimble', 'Clumsy',
            'Armored', 'Broken',
            'Mystic', 'Foolish',
            'Strong', 'Weak', ''
        ]

        modifier = random.choice(modifiers)

        if modifier == 'Slow':  # Very-low speed, below-average speed
            self.spd -= 3
            self.evad -= 1
        elif modifier == 'Fast':  # Very-high speed, above-average speed
            self.spd += 3
            self.evad += 1
        elif modifier == 'Nimble':  # Very-high evasion, above-average speed
            self.evad += 3
            self.spd += 1
        elif modifier == 'Clumsy':  # Very-low evasion, below-average speed
            self.evad -= 3
            self.spd -= 1
        elif modifier == 'Powerful':  # High attack stats
            self.attk += 2
            self.m_attk += 2
        elif modifier == 'Ineffective':  # Low attack stats
            self.attk -= 2
            self.m_attk -= 2
        elif modifier == 'Armored':  # High defense stats
            self.dfns += 2
            self.m_dfns += 2
        elif modifier == 'Broken':  # Low defense stats
            self.dfns -= 2
            self.m_dfns -= 2

        else:
            if modifier == 'Strong' and self.m_attk < self.attk and self.m_dfns < self.dfns:
                # High melee stats
                self.attk += 2
                self.dfns += 2

            elif modifier == 'Weak':
                # Low melee stats
                self.attk -= 2
                self.dfns -= 2

            elif modifier == 'Mystic' and self.m_attk > self.attk and self.m_dfns > self.dfns:
                # High magic stats
                self.m_attk += 2
                self.m_dfns += 2
                self.mp += 3

            elif modifier == 'Foolish':
                # Low magic stats
                self.m_attk -= 2
                self.m_dfns -= 2

            else:
                modifier = ''

        if position['reg'] == 'Tundra':
            self.element = 'ice'
        elif position['reg'] == 'Desert':
            self.element = 'fire'
        elif position['reg'] == 'Mountain':
            self.element = 'earth'
        elif position['reg'] == 'Shore':
            self.element = 'water'
        elif position['reg'] == 'Forest':
            self.element = 'electric'
        elif position['reg'] == 'Swamp':
            self.element = 'grass'
        elif position['reg'] == 'Graveyard':
            self.element = 'death'
        else:
            self.element = 'none'

        self.name = ' '.join([modifier, self.name]) if modifier else self.name

# Enemy AIs:

# -- Tank AI --
"""
Tank AI is resistant to player attacks and has above-average HP.
However, it lacks significantly in the damage-dealing department.
It defends more often than normal enemies and heals frequently.
They are slower than most enemies and have low evasion.

"""


def tank_stats(self):
    # Set Tank stats
    global misc_vars

    self.hp *= 1.1
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 0.8
    self.attk = math.ceil(self.attk)
    if self.attk < 1:
        self.attk = 1

    self.m_attk *= 0.8
    self.m_attk = math.ceil(self.m_attk)
    if self.m_attk < 1:
        self.m_attk = 1

    self.dfns *= 1.1
    self.dfns = math.ceil(self.dfns)

    self.m_dfns *= 1.1
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 0.8
    self.spd = math.ceil(self.spd)

    self.evad *= 0.8
    self.evad = math.ceil(self.evad)


def tank_ai(var, dodge):
    # Enemy turn for Tank AI

    self = monster
    print('\n-Enemy Turn-')

    if self.hp <= int(misc_vars['hp_m']/3) and self.mp >= 5 and random.randint(0, 2):
        # Magic heal
        sounds.magic_healing.play()

        heal = int(((self.m_attk + self.m_dfns)/2) + self.lvl/2)

        if heal < 5:
            heal = 5

        self.hp += heal
        self.mp -= 5

        print('The {0} casts a healing spell!'.format(self.name))

    elif int((self.dfns + self.m_dfns)/1.5) <= int(self.lvl/3):
        # Defend
        self.dfns += random.randint(1, 2)
        self.m_dfns += random.randint(1, 2)
        print("The {0} assumes a more defensive stance! (+DEF, +M'DEF)".format(self.name))

    elif not random.randint(0, 4) and self.mp >= 2:
        self.give_status()

    elif self.attk >= self.m_attk:
        # Physical Attack
        self.monst_attk(var, dodge)

    elif self.m_attk >= self.attk and self.mp >= 2:
        # Magic Attack
        sounds.magic_attack.play()

        print('The {0} is attempting to cast a strange spell...'.format(self.name))
        time.sleep(0.75)

        if dodge in range(battle.temp_stats['evad'], 250):
            dealt = magic.eval_element(
                p_elem=battle.player.element,
                m_elem=battle.monster.element, m_dmg=self.monst_magic(var))[1]

            player.hp -= dealt
            sounds.enemy_hit.play()
            print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                self.name, dealt))

        else:
            sounds.attack_miss.play()
            print("The spell misses you by a landslide!")

        self.mp -= 2

    else:
        self.monst_attk(var, dodge)

# -- Fighter AI --
"""
Fighter AI is the opposite of the Tank AI. It has high attack and above-average
magic attack, as well as above-average speed. However, it has below-average defense
and magic defense. It rarely defends or heals. It has low health.

"""


def fighter_stats(self):
    # Set stats for Fighter AI
    self.hp *= 0.8
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 1.2
    self.attk = math.ceil(self.attk)

    self.m_attk *= 1.1
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.8
    self.dfns = math.ceil(self.dfns)

    self.m_dfns *= 0.8
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 1.1
    self.spd = math.ceil(self.spd)


def fighter_ai(var, dodge):
    self = monster
    print('\n-Enemy Turn-')

    if not random.randint(0, 5) and self.mp >= 2:
        self.give_status()

    elif self.attk >= self.m_attk:
        # Physical Attack
        self.monst_attk(var, dodge)

    elif self.m_attk >= self.attk and self.mp >= 2:
        # Magic Attack
        sounds.magic_attack.play()

        print('The {0} is attempting to cast a strange spell...'.format(self.name))
        time.sleep(0.75)

        if dodge in range(battle.temp_stats['evad'], 250):
            dealt = magic.eval_element(
                p_elem=battle.player.element,
                m_elem=battle.monster.element, m_dmg=self.monst_magic(var))[1]

            player.hp -= dealt
            sounds.enemy_hit.play()
            print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                self.name, dealt))

        else:
            sounds.attack_miss.play()
            print("The spell misses you by a landslide!")

        self.mp -= 2

    elif self.hp <= int(misc_vars['hp_m']/5) and self.mp >= 5 and random.randint(0, 1):
        # Magic heal
        sounds.magic_healing.play()

        heal = int(((self.m_attk + self.m_dfns)/2) + self.lvl/2)
        if heal < 5:
            heal = 5

        self.hp += heal
        self.mp -= 5

        print('The {0} casts a healing spell!'.format(self.name))

    elif int((self.dfns + self.m_dfns)/1.5) <= int(self.lvl/5):
        # Defend
        self.dfns += random.randint(1, 2)
        self.m_dfns += random.randint(1, 2)
        print("The {0} assumes a more defensive stance! (+DEF, +M'DEF)".format(self.name))

    else:
        self.monst_attk(var, dodge)

# End of Enemy AIs


def spawn_monster():
    global monster
    setup_vars()
    monster = Monster('', random.randint(6, 8), random.randint(3, 4), 2, 1, 2, 1, 2, 1, 1)
    monster.monst_level()
    monster.monst_name()


def setup_vars():
    global player
    global misc_vars
    global position
    global inventory

    player = main.player
    misc_vars = main.misc_vars
    position = main.position
    inventory = inv_system.inventory
