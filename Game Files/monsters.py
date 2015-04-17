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
import msvcrt

import pygame

import inv_system
import items
import battle
import sounds
import magic
import ascii_art

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#     spam = random.choice('0123456789ynxpsewrt')
#     print(string, spam)
#     return spam
#
# input = test_input

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
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk,
                 m_dfns, spd, evad, lvl, element='none'):
        self.name = name  # Name
        self.hp = hp  # Health
        self.mp = mp  # Mana
        self.attk = attk  # Attack
        self.dfns = dfns  # Defense
        self.p_attk = p_attk  # Pierce Attack
        self.p_dfns = p_dfns  # Pierce Defense
        self.m_attk = m_attk  # Magic Attack
        self.m_dfns = m_dfns  # Magic Defense
        self.spd = spd  # Speed
        self.evad = evad  # Evasion
        self.lvl = lvl  # Level
        self.element = element  # Element
        self.monster_name = ''
        self.items = ''

    def monst_damage(self, var):
        if self.attk >= self.p_attk:
            dam_dealt = math.ceil(self.attk/2 - battle.temp_stats['dfns']/2) + var
            type_ = 'melee'
        else:
            dam_dealt = math.ceil(self.p_attk/2 - battle.temp_stats['p_dfns']/2) + var
            type_ = 'range'

        dam_dealt = magic.eval_element(
            p_elem=battle.player.element,
            m_elem=battle.monster.element, m_dmg=dam_dealt)[1]

        if dam_dealt < 1:
            dam_dealt = 1

        if random.randint(1, 100) <= 7:
            print("It's a critical hit! 2x damage!")
            dam_dealt *= 2

        return dam_dealt, type_

    def monst_magic(self, var):
        monst_dealt = math.ceil(self.m_attk/2 - battle.temp_stats['m_dfns']/2) + var

        if monst_dealt < 1:
            monst_dealt = 1

        if random.randint(1, 100) <= 7:
            print("It's a critical hit! 2x damage!")
            monst_dealt *= 2

        return monst_dealt

    def monst_level(self):
        global misc_vars
        self.lvl = int((1/3)*abs(1.4*position['avg'] - 1)) + 1
        for x in range(1, self.lvl):
            self.hp += random.randint(4, 6)
            self.mp += random.randint(1, 2)
            self.attk = random.randint(1, 3)
            self.dfns += random.randint(1, 2)
            self.p_attk += random.randint(1, 3)
            self.p_dfns += random.randint(1, 2)
            self.m_attk += random.randint(1, 3)
            self.m_dfns += random.randint(1, 2)
            self.spd += random.randint(1, 3)
            self.evad += random.randint(0, 1)

        misc_vars['hp_m'] = self.hp
        misc_vars['mp_m'] = self.mp

        num = random.randint(0, 4)  # 20% chance
        if not num:
            self.items = random.choice(items.monster_drop(self.lvl, self.monster_name))

    def monst_attk(self, var, dodge):
        sounds.sword_slash.play()
        print('The {0} is getting ready to attack you!'.format(self.name))
        time.sleep(0.75)

        while msvcrt.kbhit():
            msvcrt.getwch()

        if dodge in range(player.evad, 512):
            damage, type_ = self.monst_damage(var)

            player.hp -= damage
            sounds.enemy_hit.play()
            if type_ == 'ranged':
                print('The {0} hits you with a ranged attack, dealing {1} damage!'.format(
                    self.name, damage))
            else:
                print('The {0} hits you with a melee attack, dealing {1} damage!'.format(
                    self.name, damage))

        else:
            sounds.attack_miss.play()
            print("You narrowly avoid the {0}'s attack!".format(self.name))

    def enemy_turn(self, var, dodge):
        # This is the Enemy's AI.

        battle.temp_stats['turn_counter'] += 1

        if player.spd >= monster.spd:
            print('-'*25)

        print('\n-Enemy Turn-')
        print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(
            self.monster_name
        ))

        # Only do this on turns that are a multiple of 4 (or turn 1)
        if (not battle.temp_stats['turn_counter'] % 4 or
            battle.temp_stats['turn_counter'] == 1) \
                and random.randint(0, 1) and self.mp > 2:

            self.give_status()

        elif battle.temp_stats['turn_counter'] <= 3 and random.randint(0, 1):
            # Defend
            sounds.buff_spell.play()

            self.dfns += random.randint(2, 3)
            self.m_dfns += random.randint(2, 3)
            self.p_dfns += random.randint(2, 3)
            print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(
                self.name))

        elif self.hp <= int(misc_vars['hp_m']/4) and self.mp >= 5 and random.randint(0, 1):
            # Magic heal
            sounds.magic_healing.play()

            heal = math.ceil((self.m_attk + self.m_dfns)/2)
            # Healing power is determined by magic stats

            if heal < 5:
                heal = 5

            self.hp += heal
            self.mp -= 5

            print('The {0} casts a healing spell!'.format(self.name))

        elif self.attk > self.m_attk:
            # Physical Attack
            self.monst_attk(var, dodge)

        elif self.m_attk > self.attk and self.mp >= 2:
            # Magic Attack
            sounds.magic_attack.play()

            print('The {0} is attempting to cast a strange spell...'.format(self.name))
            time.sleep(0.75)

            while msvcrt.kbhit():
                msvcrt.getwch()

            if dodge in range(battle.temp_stats['evad'], 512):
                dam_dealt = magic.eval_element(
                    p_elem=battle.player.element,
                    m_elem=battle.monster.element, m_dmg=self.monst_magic(var))[1]

                player.hp -= dam_dealt
                sounds.enemy_hit.play()

                print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                    self.name, dam_dealt))

            else:
                sounds.attack_miss.play()
                print("The spell misses you by a landslide!")

            self.mp -= 2

        else:
            self.monst_attk(var, dodge)

        self.check_poison()

    def give_status(self):
        # Attempt to give the player a status ailment

        if random.randint(1, 6) < 4:
            if player.class_ == 'warrior':
                status = 'weakened'  # Severely lowers melee attack

            elif player.class_ == 'mage':
                status = 'silenced'  # Makes the use of magic impossible, except for spells
                                     # that cure status (such as silence)

            elif player.class_ == 'ranger':
                status = 'blinded'  # Severely lowers pierce attack

            elif player.class_ == 'assassin':
                status = 'paralyzed'  # Severely lowers speed and evasion

        else:
            status = random.choice(['asleep',  # Skips the players turn until they wake up
                                    'poisoned'  # The player takes damage each turn until cured
            ])

        if status == battle.player.status_ail:
            status = random.choice([x for x in ['asleep', 'poisoned', 'silenced', 'weakened',
                                                'blinded', 'paralyzed']
                                    if x != battle.player.status_ail])

        print('The {0} is attempting to make you {1}...'.format(self.name, status))
        time.sleep(0.75)

        while msvcrt.kbhit():
            msvcrt.getwch()

        print('You are now {0}!'.format(status))
        battle.player.status_ail = status

        self.mp -= 2

    def check_poison(self):
        # Check whether the monster is poisoned or not.
        if battle.temp_stats['m_ispoisoned']:
            if random.randint(0, 9):  # 10% chance to recover per turn
                time.sleep(0.5)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                sounds.poison_damage.play()

                poison_damage = int(math.ceil(misc_vars['hp_m']/10))
                print('The {0} took poison damage! (-{1} HP)'.format(self.name, poison_damage))
                self.hp -= poison_damage

            else:
                time.sleep(0.5)

                while msvcrt.kbhit():
                    msvcrt.getwch()

                sounds.buff_spell.play()
                print('The {0} recovered from the poison!'.format(self.name))
                battle.temp_stats['m_ispoisoned'] = False

    def monst_name(self):
        monster_type = {'Shore': ['Shell Mimic', 'Giant Crab', 'Naiad',
                                  'Sea Serpent', 'Squid'],
                        'Swamp': ['Bog Slime', 'Moss Ogre', 'Sludge Rat',
                                  'Walking Venus', 'Vine Lizard'],
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
        self.monster_name = copy.copy(self.name)

        if self.name == monster_type[position['reg']][0]:
            fighter_stats(self)

        if self.name == monster_type[position['reg']][1]:
            tank_stats(self)

        elif self.name == monster_type[position['reg']][2]:
            # Mage stats -- Not yet implemented!
            pass

        elif (self.name == monster_type[position['reg']][3] or
                self.name == monster_type[position['reg']][4]):
            # Agile stats -- Not yet implemented!
            pass

        modifiers = [
            'Slow', 'Fast',
            'Powerful', 'Ineffective',
            'Nimble', 'Clumsy',
            'Armored', 'Broken',
            'Mystic', 'Foolish',
            'Strong', 'Weak',
            'Observant', 'Obtuse', ''
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
        elif modifier == 'Observant':  # High ranged stats
            self.p_attk += 2
            self.p_dfns += 2
        elif modifier == 'Obtuse':  # Low ranged stats
            self.p_attk -= 2
            self.p_dfns -= 2

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
Tanks are resistant to player attacks and has above-average HP.
However, they lacks significantly in the damage-dealing department.
They are slower than most enemies and have low evasion.

"""


def tank_stats(self):
    # Set Tank stats
    global misc_vars

    self.hp *= 1.2
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 0.8
    self.attk = math.ceil(self.attk)

    self.p_attk *= 0.8
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 0.8
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 1.2
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 1.2
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 1.2
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 0.8
    self.spd = math.ceil(self.spd)

    self.evad *= 0.8
    self.evad = math.ceil(self.evad)


# -- Fighter AI --
"""
Fighters are the opposite of Tanks. They have high attack and above-average
magic attack, as well as above-average speed. However, they have below-average defense
and magic defense. They have low health.

"""


def fighter_stats(self):
    # Set stats for Fighter AI
    self.hp *= 0.8
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 1.2
    self.attk = math.ceil(self.attk)

    self.p_attk *= 1.2

    self.m_attk *= 1.2
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.8
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 0.8
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 0.8
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 1.2
    self.spd = math.ceil(self.spd)


def spawn_monster():
    global monster
    setup_vars()
    monster = Monster('', random.randint(6, 8), random.randint(3, 4), 2, 1, 2, 1, 2, 1, 2, 1, 1)
    monster.monst_name()
    monster.monst_level()
    if monster.evad > 256:
        monster.evad = 256

def setup_vars():
    global player
    global misc_vars
    global position
    global inventory

    player = main.player
    misc_vars = main.misc_vars
    position = main.position
    inventory = inv_system.inventory
