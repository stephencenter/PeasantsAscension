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
import bosses

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

is_defending = False


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
        if not isinstance(self, bosses.Boss):
            self.items = ''

    def monst_damage(self, mode):
        ise = inv_system.equipped
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])

        if mode == 'melee':
            dam_dealt = math.ceil(self.attk*1.2 - (battle.temp_stats['dfns']/3)*(1 + dr))

        else:
            dam_dealt = math.ceil(self.p_attk*1.2 - (battle.temp_stats['p_dfns']/3)*(1 + dr))

        dam_dealt = magic.eval_element(
            p_elem=battle.player.element,
            m_elem=battle.monster.element, m_dmg=dam_dealt)[1]

        if dam_dealt < 1:
            dam_dealt = 1

        if random.randint(1, 100) <= 7:
            print("It's a critical hit! 2x damage!")
            dam_dealt *= 2

        return dam_dealt

    def monst_magic(self):
        ise = inv_system.equipped
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])
        monst_dealt = math.ceil(self.m_attk*1.2 - (battle.temp_stats['m_dfns']/3)*(1 + dr))

        if monst_dealt < 1:
            monst_dealt = 1

        if random.randint(1, 100) <= 14:
            print("It's a critical hit! 2x damage!")
            monst_dealt *= 2

        return monst_dealt

    def monst_level(self):
        global misc_vars
        self.lvl = int((1/3)*abs(position['avg'] - 1)) + 1

        if self.lvl < 1:
            self.lvl = 1

        # Monsters in the Aethus are 15 levels higher than monsters below
        if position['reg'] == 'Aethus':
            self.lvl += 15

        for x in range(0, self.lvl):
            self.hp += random.randint(4, 7)
            self.mp += random.randint(2, 5)
            self.attk = random.randint(2, 4)
            self.dfns += random.randint(2, 3)
            self.p_attk += random.randint(2, 4)
            self.p_dfns += random.randint(2, 3)
            self.m_attk += random.randint(2, 4)
            self.m_dfns += random.randint(2, 3)
            self.spd += random.randint(2, 4)
            self.evad += random.randint(1, 2)

        misc_vars['hp_m'] = self.hp
        misc_vars['mp_m'] = self.mp

        num = random.randint(0, 4)  # 20% chance
        if not num:
            self.items = random.choice(items.monster_drop(self.lvl, self.monster_name))

    def monst_attk(self, dodge, mode):
        sounds.sword_slash.play()
        if isinstance(self, bosses.Boss):
            print('The {0} is getting ready to attack you!'.format(self.name))
        else:
            print('The {0} {1}'.format(self.name, self.attk_msg))
        time.sleep(0.75)

        while msvcrt.kbhit():
            msvcrt.getwch()

        if dodge in range(player.evad, 512):
            damage = self.monst_damage(mode)

            player.hp -= damage
            sounds.enemy_hit.play()
            if mode == 'pierce':
                print('The {0} hits you with a ranged attack, dealing {1} damage!'.format(
                    self.name, damage))
            else:
                print('The {0} hits you with a melee attack, dealing {1} damage!'.format(
                    self.name, damage))

        else:
            sounds.attack_miss.play()
            print("You narrowly avoid the {0}'s attack!".format(self.name))

    def enemy_turn(self, dodge):
        # Default AI used solely by bosses without custom AI
        global is_defending

        if is_defending:
            is_defending = False

            monster.dfns /= 1.1
            monster.m_dfns /= 1.1
            monster.p_dfns /= 1.1
            monster.dfns = math.floor(monster.dfns)
            monster.m_dfns = math.floor(monster.m_dfns)
            monster.p_dfns = math.floor(monster.p_dfns)

        battle.temp_stats['turn_counter'] += 1

        possible_p_dam = math.ceil(self.p_attk - battle.temp_stats['p_dfns']/2)
        possible_m_dam = math.ceil(self.m_attk - battle.temp_stats['m_dfns']/2)
        possible_a_dam = math.ceil(self.attk - battle.temp_stats['dfns']/2)

        most_effective = max([possible_p_dam, possible_m_dam, possible_a_dam])

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

        elif not random.randint(0, 4):
            # Defend
            sounds.buff_spell.play()

            monster.dfns *= 1.1
            monster.m_dfns *= 1.1
            monster.p_dfns *= 1.1
            monster.dfns = math.ceil(monster.dfns)
            monster.m_dfns = math.ceil(monster.m_dfns)
            monster.p_dfns = math.ceil(monster.p_dfns)

            print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(
                self.name))

            is_defending = True

        elif self.hp <= int(misc_vars['hp_m']/4) and self.mp >= 5 and random.randint(0, 1):
            # Magic heal
            sounds.magic_healing.play()

            if 20 < self.hp*0.2:
                self.hp += self.hp*0.2
            else:
                self.hp += 20

            if self.hp > main.misc_vars['hp_m']:
                self.hp = main.misc_vars['hp_m']

            print('The {0} casts a healing spell!'.format(self.name))

        elif most_effective in [possible_p_dam, possible_a_dam]:
            # Non-magic Attack
            if most_effective == possible_p_dam:
                self.monst_attk(dodge, 'pierce')

            else:
                self.monst_attk(dodge, 'melee')

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
                    m_elem=battle.monster.element, m_dmg=self.monst_magic())[1]

                player.hp -= dam_dealt
                sounds.enemy_hit.play()

                print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                    self.name, dam_dealt))

            else:
                sounds.attack_miss.play()
                print("The spell misses you by a landslide!")

            self.mp -= 2

        else:
            if most_effective == possible_p_dam:
                self.monst_attk(dodge, 'pierce')
            else:
                self.monst_attk(dodge, 'melee')

        self.check_poison()

        if isinstance(self, bosses.Boss) and self.multiphase and self.hp <= 0:
            self.enemy_turn(dodge)

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

            elif player.class_ == 'monk':
                status = random.choice(['paralyzed', 'weakened'])

            elif player.class_ == 'paladin':
                status = random.choice(['silenced', 'weakened'])

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

        if random.randint(0, 1):
            print('You are now {0}!'.format(status))
            battle.player.status_ail = status

        else:
            print('The {0} failed to make you {1}!'.format(monster.monster_name, status))

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
        monster_type = {'Pythonian Coastline': ['Shell Mimic', 'Giant Crab',
                                                'Naiad', 'Sea Serpent', 'Squid'],

                        'Bogthorn': ['Bog Slime', 'Moss Ogre',
                                     "Will-o'-the-wisp", 'Vine Lizard', 'Sludge Rat'],

                        'Central Forest': ['Goblin Archer', 'Beetle'
                        if main.player.name != "Flygon Jones" else "Calculator",
                                           'Spriggan', 'Imp', 'Bat'],

                        'Arcadian Desert': ['Mummy', 'Sand Golem',
                                            'Minubis', 'Fire Ant', 'Naga'],

                        'Glacian Plains': ['Ice Soldier', 'Minor Yeti',
                                           'Corrupt Thaumaturge', 'Arctic Wolf', 'Frost Bat'],

                        'Terrius Mt. Range': ['Troll', 'Rock Giant',
                                              'Oread', 'Tengu', 'Giant Worm'],

                        'Overshire Graveyard': ['Zombie', 'Undead Archer',
                                                'Necromancer', 'Skeleton', 'Ghoul'],

                        'Aethus': ['Alicorn', 'Griffin', 'Wraith',
                                   'Harpy', 'Flying Serpent']
                        }

        chosen = random.randint(0, 4)
        self.name = monster_type[position['reg']][chosen]

        # A list of monster-types and what AI they are to have
        magic_enemies = ['Naiad', "Will-o'the-wisp", 'Minubis', 'Oread', 'Necromancer', 'Wraith',
                         'Alicorn', 'Flying Serpent', 'Imp', 'Corrupt Thaumaturge', 'Spriggan']

        melee_enemies = ['Shell Mimic', 'Giant Crab', 'Bog Slime', 'Mummy', 'Sand Golem',
                         'Moss Ogre', 'Vine Lizard', 'Troll', 'Ghoul', 'Griffin', 'Tengu',
                         'Giant Worm', 'Zombie', 'Arctic Wolf', 'Minor Yeti', 'Sludge Rat',
                         'Sea Serpent', 'Beetle', 'Calculator', 'Harpy']

        ranged_enemies = ['Fire Ant', 'Naga', 'Ice Soldier', 'Frost Bat', 'Bat',
                          'Skeleton', 'Squid', 'Rock Giant', 'Undead Archer', 'Goblin Archer']

        # Assign the correct AI and stats to each kind of monster
        if self.name in magic_enemies:
            self.enemy_turn = magic_ai
            magic_stats(self)

        elif self.name in melee_enemies:
            self.enemy_turn = melee_ai
            melee_stats(self)

        elif self.name in ranged_enemies:
            self.enemy_turn = ranged_ai
            ranger_stats(self)

        else:
            raise Exception('Enemy "{0}" does not have an AI set!'.format(self.name))

        # Set the flavor text to match the attack style of various monsters
        biting_monsters = ['Vine Lizard', 'Beetle', 'Zombie', 'Ghoul',
                           'Arctic Wolf', 'Sea Serpent', 'Shell Mimic']
        charging_monsters = ['Giant Worm', 'Bog Slime']
        slashing_monsters = ['Griffin', 'Tengu', 'Harpy', 'Sludge Rat', 'Giant Crab',]
        whacking_monsters = ['Troll', 'Rock Giant']
        spitting_monsters = ['Frost Bat', 'Squid', 'Fire Ant', 'Bat']
        arrow_monsters = ['Naga', 'Ice Soldier', 'Undead Archer', 'Goblin Archer', 'Skeleton',]
        fist_monsters = ['Moss Ogre', 'Minor Yeti', 'Sand Golem', 'Mummy']
        magic_monsters = ['Imp', 'Naiad', "Will-o'the-wisp", 'Minubis',
                          'Oread', 'Necromancer', 'Wraith', 'Alicorn',
                          'Flying Serpent', 'Corrupt Thaumaturge', 'Spriggan']
        math_monsters = ['Calculator']

        if self.name in biting_monsters:
            self.attk_msg = "bears its fangs and tries to bite you!"
        elif self.name in charging_monsters:
            monster.attk_msg = "puts all its weight into trying to charge you!"
        elif self.name in slashing_monsters:
            self.attk_msg = "reveals its claws and prepares to slash you!"
        elif self.name in whacking_monsters:
            self.attk_msg = "finds a nearby rock and prepares to beat you with it!"
        elif self.name in spitting_monsters:
            self.attk_msg = "begins to spit a dangerous projectile at you!"
        elif self.name in arrow_monsters:
            self.attk_msg = "readies its bow to fire a volley of arrows!"
        elif self.name in fist_monsters:
            self.attk_msg = "prepares to smash you with its fists!"
        elif self.name in magic_monsters:
            self.attk_msg = "draws from its magical essense to destroy you!"
        elif self.name in math_monsters:
            self.attk_msg = "begins answering algebra questions in a devastating manner!"

        # Prepare to add the modifier onto the name
        self.monster_name = copy.copy(self.name)

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
            self.spd -= 4
            self.evad -= 2
        elif modifier == 'Fast':  # Very-high speed, above-average speed
            self.spd += 4
            self.evad += 2
        elif modifier == 'Nimble':  # Very-high evasion, above-average speed
            self.evad += 4
            self.spd += 2
        elif modifier == 'Clumsy':  # Very-low evasion, below-average speed
            self.evad -= 4
            self.spd -= 2
        elif modifier == 'Powerful':  # High attack stats
            self.attk += 3
            self.m_attk += 3
            self.p_attk += 3
        elif modifier == 'Ineffective':  # Low attack stats
            self.attk -= 3
            self.m_attk -= 3
            self.p_attk -= 3
        elif modifier == 'Armored':  # High defense stats
            self.dfns += 3
            self.m_dfns += 3
            self.p_dfns += 3
        elif modifier == 'Broken':  # Low defense stats
            self.dfns -= 3
            self.m_dfns -= 3
            self.p_dfns -= 3
        elif modifier == 'Observant':  # High ranged stats
            self.p_attk += 3
            self.p_dfns += 3
        elif modifier == 'Obtuse':  # Low ranged stats
            self.p_attk -= 3
            self.p_dfns -= 3

        else:
            if modifier == 'Strong' and self.m_attk < self.attk and self.m_dfns < self.dfns:
                # High melee stats
                self.attk += 3
                self.dfns += 3

            elif modifier == 'Weak':
                # Low melee stats
                self.attk -= 3
                self.dfns -= 3

            elif modifier == 'Mystic' and self.m_attk > self.attk and self.m_dfns > self.dfns:
                # High magic stats
                self.m_attk += 3
                self.m_dfns += 3
                self.mp += 5

            elif modifier == 'Foolish':
                # Low magic stats
                self.m_attk -= 3
                self.m_dfns -= 3

            else:
                modifier = ''

        # Adjust for problems that may happen with enemy stats
        for stat in ['self.attk', 'self.dfns',
                     'self.p_attk', 'self.p_dfns',
                     'self.m_attk', 'self.m_dfns',
                     'self.spd', 'self.evad'
                     ]:
            if eval(stat) < 1:  # Enemy stats cannot be lower than one
                exec("{0} = 1".format(stat))

            elif isinstance(eval(stat), float):  # Enemy stats must be integers
                exec("{0} = math.ceil({0})".format(stat))

        if position['reg'] == 'Glacian Plains':
            self.element = 'ice'
        elif position['reg'] == 'Arcadian Desert':
            self.element = 'fire'
        elif position['reg'] == 'Terrius Mt. Range':
            self.element = 'earth'
        elif position['reg'] == 'Pythonian Coastline':
            self.element = 'water'
        elif position['reg'] == 'Central Forest':
            self.element = 'electric'
        elif position['reg'] == 'Bogthorn Marsh':
            self.element = 'grass'
        elif position['reg'] == 'Overshire Graveyard':
            self.element = 'death'
        elif position['reg'] == 'Aethus':
            self.element = 'wind'
        else:
            self.element = 'none'

        self.name = ' '.join([modifier, self.name]) if modifier else self.name

# Enemy Stat Classes:

# -- Tank Stats --
"""
Tanks are resistant to player attacks and has above-average HP.
However, they lacks significantly in the damage-dealing department.
They are slower than most enemies and have low evasion.

"""


def tank_stats(self):
    # Set Tank stats
    global misc_vars

    self.hp *= 1.3
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 0.8
    self.attk = math.ceil(self.attk)

    self.p_attk *= 0.8
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 0.8
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 1.3
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 1.3
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 1.3
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 0.8
    self.spd = math.ceil(self.spd)

    self.evad *= 0.8
    self.evad = math.ceil(self.evad)


# -- Fighter Stats --
"""
Fighters are the opposite of Tanks. They have high attack and above-average
magic attack, as well as above-average speed. However, they have below-average defense
and magic defense. They have low health.

"""


def melee_stats(self):
    # Set stats for melee-class monsters
    self.hp *= 1.2
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 1.5
    self.attk = math.ceil(self.attk)

    self.p_attk *= 0.5
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 0.5
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 1.5
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 1.5
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 0.5
    self.m_dfns = math.ceil(self.m_dfns)

    self.spd *= 0.5
    self.spd = math.ceil(self.spd)


def magic_stats(self):
    # Set stats for Mage-class monsters
    self.mp *= 1.5
    self.mp = math.ceil(self.mp)
    misc_vars['mp_m'] = copy.copy(self.mp)

    self.attk *= 0.5
    self.attk = math.ceil(self.attk)

    self.p_attk *= 0.5
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 1.5
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.9
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 0.9
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 1.5
    self.m_dfns = math.ceil(self.m_dfns)


def ranger_stats(self):
    # Set stats for Ranger-class monsters
    self.hp *= 0.9
    self.hp = math.ceil(self.hp)
    misc_vars['hp_m'] = copy.copy(self.hp)

    self.attk *= 0.8
    self.attk = math.ceil(self.attk)

    self.p_attk *= 1.5
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 0.8
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.8
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 1.3
    self.p_dfns = math.ceil(self.p_dfns)

    self.spd *= 1.5
    self.spd = math.ceil(self.spd)

    self.evad *= 1.5
    self.evad = math.ceil(self.evad)


def magic_ai(dodge):
    if player.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(
        monster.monster_name
    ))

    # Only do this on turns that are a multiple of 4 (or turn 1)
    if (not battle.temp_stats['turn_counter'] % 4 or
        battle.temp_stats['turn_counter'] == 1) \
            and random.randint(0, 1) and monster.mp > 2:

        monster.give_status()

    elif monster.hp <= int(misc_vars['hp_m']/4) and monster.mp >= 5:
        # Magic heal
        sounds.magic_healing.play()

        if 20 < monster.hp*0.2:
            monster.hp += monster.hp*0.2
        else:
            monster.hp += 20

        if monster.hp > main.misc_vars['hp_m']:
            monster.hp = main.misc_vars['hp_m']

        print('The {0} casts a healing spell!'.format(monster.name))

    elif monster.mp >= 3:
        # Magic Attack
        sounds.magic_attack.play()

        print('The {0} {1}'.format(monster.name, monster.attk_msg))
        time.sleep(0.75)

        while msvcrt.kbhit():
            msvcrt.getwch()

        if dodge in range(battle.temp_stats['evad'], 512):
            dam_dealt = magic.eval_element(
                p_elem=battle.player.element,
                m_elem=battle.monster.element, m_dmg=monster.monst_magic())[1]

            player.hp -= dam_dealt
            sounds.enemy_hit.play()

            print("The {0}'s spell succeeds, and deals {1} damage to you!".format(
                monster.name, dam_dealt))

        else:
            sounds.attack_miss.play()
            print("The spell misses you by a landslide!")

        monster.mp -= 2

    else:
        # Non-magic Attack
        random.choice([monster.monst_attk(dodge, 'pierce'),
                       monster.monst_attk(dodge, 'melee')])

    monster.check_poison()

    if isinstance(monster, bosses.Boss) and monster.multiphase and monster.hp <= 0:
        monster.enemy_turn(dodge)


def ranged_ai(dodge):
    # This is the Enemy's AI.
    global is_defending
    global monster

    if is_defending:
        # Set defense back to normal
        is_defending = False

        monster.dfns /= 1.1
        monster.m_dfns /= 1.1
        monster.p_dfns /= 1.1
        monster.dfns = math.floor(monster.dfns)
        monster.m_dfns = math.floor(monster.m_dfns)
        monster.p_dfns = math.floor(monster.p_dfns)

    battle.temp_stats['turn_counter'] += 1

    if player.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(
        monster.monster_name
    ))

    if not random.randint(0, 4):
        # Defend
        sounds.buff_spell.play()

        # Scaling Defense
        monster.dfns *= 1.1
        monster.m_dfns *= 1.1
        monster.p_dfns *= 1.1

        monster.dfns = math.ceil(monster.dfns)
        monster.p_dfns = math.ceil(monster.p_dfns)
        monster.m_dfns = math.ceil(monster.m_dfns)

        print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(
            monster.name))

        is_defending = True

    else:
        monster.monst_attk(dodge, 'pierce')

    monster.check_poison()

    if isinstance(monster, bosses.Boss) and monster.multiphase and monster.hp <= 0:
        monster.enemy_turn(dodge)


def melee_ai(dodge):
    # This is the Enemy's AI.
    global is_defending
    global monster

    if is_defending:
        # Set defense back to normal
        is_defending = False

        monster.dfns /= 1.1
        monster.m_dfns /= 1.1
        monster.p_dfns /= 1.1
        monster.dfns = math.floor(monster.dfns)
        monster.m_dfns = math.floor(monster.m_dfns)
        monster.p_dfns = math.floor(monster.p_dfns)

    battle.temp_stats['turn_counter'] += 1

    if player.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(
        monster.monster_name
    ))

    if not random.randint(0, 4):
        # Defend
        sounds.buff_spell.play()

        # Scaling Defense
        monster.dfns *= 1.1
        monster.m_dfns *= 1.1
        monster.p_dfns *= 1.1

        monster.dfns = math.ceil(monster.dfns)
        monster.p_dfns = math.ceil(monster.p_dfns)
        monster.m_dfns = math.ceil(monster.m_dfns)

        print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(
            monster.name))

        is_defending = True

    else:
        monster.monst_attk(dodge, 'melee')

    monster.check_poison()

    if isinstance(monster, bosses.Boss) and monster.multiphase and monster.hp <= 0:
        monster.enemy_turn(dodge)


def spawn_monster():
    global monster
    setup_vars()
    monster = Monster('', random.randint(2, 3), random.randint(2, 4), 1, 1, 1, 1, 1, 1, 1, 1, 1)
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
