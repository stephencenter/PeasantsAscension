#   This file is part of Peasants' Ascension.
#
#	 Peasants' Ascension is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Peasants' Ascension is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Peasants' Ascension.  If not, see <http://www.gnu.org/licenses/>.

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

monster = ''
is_defending = False


class Monster:
    # All monsters use this class. Bosses use a sub-class called
    # "Boss" (located in bosses.py) which inherits from this.
    def __init__(self, name, hp, mp, attk, dfns, p_attk, p_dfns, m_attk, m_dfns, spd, evad, lvl, element='none'):
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
        self.monster_name = ''  # The name of the monsters species (so a Fast Goblin's monster_name would be Goblin)
        self.status = ''
        self.max_hp = copy.copy(self.hp)
        self.max_mp = copy.copy(self.mp)
        self.is_poisoned = False
        self.items = ''
        self.status_ail = None  # Doesn't do anything, this is just to make some code in a different file work properly

    def physical_damage(self, mode, target):
        ise = inv_system.equipped[target.name if target != main.player else 'player']
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])

        if mode == 'melee':
            dam_dealt = math.ceil(self.attk - (battle.temp_stats[target.name]['dfns']/2)*(1 + dr))

        else:
            dam_dealt = math.ceil(self.p_attk - (battle.temp_stats[target.name]['p_dfns']/2)*(1 + dr))

        dam_dealt = magic.eval_element(p_elem=target.element, m_elem=self.element, m_dmg=dam_dealt)[1]

        if random.randint(1, 100) <= 15:
            dam_dealt *= 1.5
            print("It's a critical hit! 1.5x damage!")

            sounds.critical_hit.play()
            main.smart_sleep(0.5)

        if dam_dealt < 1:
            dam_dealt = 1

        return dam_dealt

    def magical_damage(self, target):
        ise = inv_system.equipped[target.name if target != main.player else 'player']
        dr = sum([ise[armor].defense for armor in ise if isinstance(ise[armor], items.Armor)])
        dam_dealt = math.ceil(self.m_attk - (battle.temp_stats[target.name]['m_dfns']/2)*(1 + dr))

        if dam_dealt < 1:
            dam_dealt = 1

        return dam_dealt

    def monst_level(self): # THIS NEEDS REWORKING!!

        self.lvl = int((1/2.5)*abs(main.party_info['avg'] - 1)) + 1

        # Prevent the monster's level from being below one
        if self.lvl < 1:
            self.lvl = 1

        # Monsters in the Aethus are 15 levels higher than monsters below
        if main.party_info['reg'] == 'Aethus':
            self.lvl += 15

        for x in range(1, self.lvl):
            self.hp += 5
            self.mp += 4
            self.attk += 4
            self.dfns += 3
            self.p_attk += 4
            self.p_dfns += 3
            self.m_attk += 4
            self.m_dfns += 3
            self.spd += 3
            self.evad += 2

        self.max_hp = self.hp
        self.max_mp = self.mp

    def give_status(self, target):
        # Attempt to give the target a status ailment
        status = random.choice([x for x in ['asleep',
                                            'poisoned',
                                            'silenced',
                                            'weakened',
                                            'blinded',
                                            'paralyzed',
                                            'frostbitten',
                                            'burned',
                                            'deafened',
                                            'muted']
                                if x != target.status_ail])

        print('The {0} is attempting to make {1} {2}...'.format(self.monster_name, target.name, status))
        main.smart_sleep(0.75)

        if random.randint(0, 1):
            print('{0} is now {1}!'.format(target.name, status))
            target.status_ail = status

        else:
            print('The {0} failed to make {1} {2}!'.format(self.monster_name, target.name, status))

        self.mp -= 2

    def check_poison(self):
        # Check whether the monster is poisoned or not.
        if self.is_poisoned:
            if random.randint(0, 9):  # 10% chance to recover per turn
                main.smart_sleep(0.5)

                sounds.poison_damage.play()

                poison_damage = math.floor(self.hp/6)
                print('The {0} took poison damage! (-{1} HP)'.format(self.monster_name, poison_damage))
                self.hp -= poison_damage

            else:
                main.smart_sleep(0.5)

                sounds.buff_spell.play()
                print('The {0} recovered from the poison!'.format(self.monster_name))
                self.is_poisoned = False

    def monst_name(self):
        m_type = {'Central Forest': ['Goblin Archer', 'Spriggan', 'Imp', 'Bat',
                                     'Beetle' if main.player.name != "Flygon Jones" else "Calculator",],

                  'Harconian Coastline': ['Shell Mimic', 'Giant Crab', 'Naiad', 'Sea Serpent', 'Squid'],

                  'Glacian Plains': ['Ice Soldier', 'Minor Yeti', 'Corrupt Thaumaturge', 'Arctic Wolf', 'Frost Bat'],

                  'Bogthorn Marsh': ['Bog Slime', 'Moss Ogre', "Will-o'-the-wisp", 'Vine Lizard', 'Sludge Rat'],

                  'Arcadian Desert': ['Mummy', 'Sand Golem', 'Anubis', 'Fire Ant', 'Naga'],

                  'Terrius Mt. Range': ['Troll', 'Rock Giant','Oread', 'Tengu', 'Giant Worm'],

                  'Overshire Graveyard': ['Zombie', 'Undead Archer','Necromancer', 'Skeleton', 'Ghoul'],

                  'Aethus': ['Alicorn', 'Griffin', 'Wraith','Harpy', 'Flying Serpent']
                  }

        self.name = m_type[main.party_info['reg']][random.randint(0, 4)]

        # A list of monster-types and what AI they are to have
        magic_enemies = ['Naiad', "Will-o'the-wisp", 'Anubis', 'Oread', 'Necromancer', 'Wraith',
                         'Alicorn', 'Flying Serpent', 'Imp', 'Corrupt Thaumaturge', 'Spriggan']

        melee_enemies = ['Shell Mimic', 'Giant Crab', 'Bog Slime', 'Mummy', 'Sand Golem',
                         'Moss Ogre', 'Vine Lizard', 'Troll', 'Ghoul', 'Griffin', 'Tengu',
                         'Giant Worm', 'Zombie', 'Arctic Wolf', 'Minor Yeti', 'Sludge Rat',
                         'Sea Serpent', 'Beetle', 'Calculator', 'Harpy']

        ranged_enemies = ['Fire Ant', 'Naga', 'Ice Soldier', 'Frost Bat', 'Bat',
                          'Skeleton', 'Squid', 'Rock Giant', 'Undead Archer', 'Goblin Archer']

        # Assign the correct AI and stats to each kind of monster
        if self.name in magic_enemies:
            self.battle_turn = magic_ai
            magic_stats(self)

        elif self.name in melee_enemies:
            self.battle_turn = melee_ai
            melee_stats(self)

        elif self.name in ranged_enemies:
            self.battle_turn = ranged_ai
            ranger_stats(self)

        else:
            raise Exception('Enemy "{0}" does not have an AI set!'.format(self.name))

        # Set the flavor text to match the attack style of various monsters
        biting_monsters = ['Vine Lizard', 'Beetle', 'Zombie', 'Ghoul', 'Arctic Wolf', 'Sea Serpent', 'Shell Mimic']
        charging_monsters = ['Giant Worm', 'Bog Slime']
        slashing_monsters = ['Griffin', 'Tengu', 'Harpy', 'Sludge Rat', 'Giant Crab']
        whacking_monsters = ['Troll', 'Rock Giant']
        spitting_monsters = ['Frost Bat', 'Squid', 'Fire Ant', 'Bat']
        arrow_monsters = ['Naga', 'Ice Soldier', 'Undead Archer', 'Goblin Archer', 'Skeleton']
        fist_monsters = ['Moss Ogre', 'Minor Yeti', 'Sand Golem', 'Mummy']
        magic_monsters = ['Imp', 'Naiad', "Will-o'the-wisp", 'Anubis', 'Oread', 'Necromancer', 'Wraith', 'Alicorn',
                          'Flying Serpent', 'Corrupt Thaumaturge', 'Spriggan']
        math_monsters = ['Calculator']

        if self.name in biting_monsters:
            self.attk_msg = "bears its fangs and tries to bite"
        elif self.name in charging_monsters:
            monster.attk_msg = "puts all its weight into trying to charge"
        elif self.name in slashing_monsters:
            self.attk_msg = "reveals its claws and prepares to slash"
        elif self.name in whacking_monsters:
            self.attk_msg = "finds a nearby rock and prepares to use it to beat"
        elif self.name in spitting_monsters:
            self.attk_msg = "begins to spit a dangerous projectile at"
        elif self.name in arrow_monsters:
            self.attk_msg = "readies its bow to fire a volley of arrows at"
        elif self.name in fist_monsters:
            self.attk_msg = "prepares its fists to smash"
        elif self.name in magic_monsters:
            self.attk_msg = "draws from its magical essence to destroy"
        elif self.name in math_monsters:
            self.attk_msg = "begins calculating the fuck out of"

        # Prepare to add the modifier onto the name
        self.monster_name = copy.copy(self.name)

        modifiers = ['Slow', 'Fast', 'Powerful', 'Ineffective', 'Nimble', 'Clumsy', 'Armored', 'Broken', 'Mystic',
                     'Foolish', 'Strong', 'Weak', 'Observant', 'Obtuse']

        modifier = random.choice(modifiers)

        if self.name == "Goblin" and random.randint(0, 100) == 42:
            self.modifier = "Whispering"
            self.attk *= 1.2
            self.dfns *= 1.2
            self.m_attk *= 1.2
            self.m_dfns *= 1.2
            self.p_attk *= 1.2
            self.p_dfns *= 1.2
            self.evad *= 1.2
            self.spd *= 1.2

        elif modifier == 'Slow':  # Very-low speed, below-average speed
            self.spd /= 1.3
            self.evad /= 1.1
        elif modifier == 'Fast':  # Very-high speed, above-average speed
            self.spd *= 1.3
            self.evad *= 1.1
        elif modifier == 'Nimble':  # Very-high evasion, above-average speed
            self.evad *= 1.3
            self.spd *= 1.1
        elif modifier == 'Clumsy':  # Very-low evasion, below-average speed
            self.evad /= 1.3
            self.spd /= 1.1
        elif modifier == 'Powerful':  # High attack stats
            self.attk *= 1.2
            self.m_attk *= 1.2
            self.p_attk *= 1.2
        elif modifier == 'Ineffective':  # Low attack stats
            self.attk /= 1.2
            self.m_attk /= 1.2
            self.p_attk /= 1.2
        elif modifier == 'Armored':  # High defense stats
            self.dfns *= 1.2
            self.m_dfns *= 1.2
            self.p_dfns *= 1.2
        elif modifier == 'Broken':  # Low defense stats
            self.dfns /= 1.2
            self.m_dfns /= 1.2
            self.p_dfns /= 1.2
        elif modifier == 'Observant':  # High ranged stats
            self.p_attk *= 1.2
            self.p_dfns *= 1.2
        elif modifier == 'Obtuse':  # Low ranged stats
            self.p_attk /= 1.2
            self.p_dfns /= 1.2

        else:
            if modifier == 'Strong' and self.m_attk < self.attk and self.m_dfns < self.dfns:
                # High melee stats
                self.attk *= 1.2
                self.dfns *= 1.2

            elif modifier == 'Weak':
                # Low melee stats
                self.attk /= 1.2
                self.dfns /= 1.2

            elif modifier == 'Mystic' and self.m_attk > self.attk and self.m_dfns > self.dfns:
                # High magic stats
                self.m_attk *= 1.2
                self.m_dfns *= 1.2
                self.mp *= 1.2

            elif modifier == 'Foolish':
                # Low magic stats
                self.m_attk /= 1.2
                self.m_dfns /= 1.2

            else:
                modifier = ''

        # Adjust for problems that may happen with enemy stats
        for stat in ['self.attk', 'self.dfns', 'self.p_attk', 'self.p_dfns', 'self.m_attk', 'self.m_dfns',
                     'self.spd', 'self.evad'
                     ]:

            if eval(stat) < 1:  # Enemy stats cannot be lower than one
                exec("{0} = 1".format(stat))

            exec("{0} = math.ceil({0})".format(stat))# Enemy stats must be integers

        if self.monster_name == "Calculator":
            self.element = 'grass'
            self.status = 'fucked'
            self.status_msg = "was imbued with bullshit, causing severe fuckage!"

        elif main.party_info['reg'] == 'Glacian Plains':
            self.element = 'ice'
            self.status = 'frostbitten'
            self.status_msg = "was imbued with frost, causing painful frostbite!"

        elif main.party_info['reg'] == 'Arcadian Desert':
            self.element = 'fire'
            self.status = 'burned'
            self.status_msg = "was imbued with fire, causing painful burns!"

        elif main.party_info['reg'] == 'Terrius Mt. Range':
            self.element = 'earth'
            self.status = 'paralyzed'
            self.status_msg = "hit a nerve ending, causing temporary paralysis!"

        elif main.party_info['reg'] == 'Harconian Coastline':
            self.element = 'water'
            self.status = 'muted'
            self.status_msg = "caused organizational issues, leading to impaired item usage!"

        elif main.party_info['reg'] == 'Central Forest':
            self.element = 'electric'
            self.status = 'blinded'
            self.status_msg = "was imbued with darkness, causing impaired vision!"

        elif main.party_info['reg'] == 'Bogthorn Marsh':
            self.element = 'grass'
            self.status = 'poisoned'
            self.status_msg = "was imbued with deadly toxins that will slowly drain health!"

        elif main.party_info['reg'] == 'Overshire Graveyard':
            self.element = 'death'
            self.status = 'asleep'
            self.status_msg = "knocked their target unconscious using noxious fumes!"

        elif main.party_info['reg'] == 'Aethus':
            self.element = 'wind'
            self.status = 'deafened'
            self.status_msg = "brought upon the winds, dampening their target's hearing!"

        else: # This should not happen
            self.element = 'none'
            self.status = False
            self.status_msg = False

        self.name = ' '.join([modifier, self.name]) if modifier else self.name

        # Give the monster a set of items to drop if RNGsus wills it
        if not isinstance(self, bosses.Boss):
            if random.randint(0, 4) == 0: # 20% chance
                self.items = random.choice(items.monster_drop_list[self.monster_name])


# Enemy AI + Stats:
# -- Melee Stats --
def melee_stats(self):
    # Set stats for melee-class monsters
    self.hp *= 1.2
    self.hp = math.ceil(self.hp)
    self.max_hp = copy.copy(self.hp)

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
    self.max_mp = copy.copy(self.mp)

    self.attk *= 0.5
    self.attk = math.ceil(self.attk)

    self.p_attk *= 0.5
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 1.5
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.65
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 0.65
    self.p_dfns = math.ceil(self.p_dfns)

    self.m_dfns *= 1.5
    self.m_dfns = math.ceil(self.m_dfns)


def ranger_stats(self):
    # Set stats for Ranger-class monsters
    self.hp *= 0.9
    self.hp = math.ceil(self.hp)
    self.max_hp = copy.copy(self.hp)

    self.attk *= 0.8
    self.attk = math.ceil(self.attk)

    self.p_attk *= 1.5
    self.p_attk = math.ceil(self.p_attk)

    self.m_attk *= 0.8
    self.m_attk = math.ceil(self.m_attk)

    self.dfns *= 0.8
    self.dfns = math.ceil(self.dfns)

    self.p_dfns *= 1.2
    self.p_dfns = math.ceil(self.p_dfns)

    self.spd *= 1.5
    self.spd = math.ceil(self.spd)

    self.evad *= 1.5
    self.evad = math.ceil(self.evad)


def magic_ai():
    global monster

    battle.turn_counter += 1

    target = random.choice([x for x in [
        main.player,
        main.solou,
        main.xoann,
        main.randall,
        main.ran_af,
        main.parsto,
        main.adorine
    ] if x.enabled and x.status_ail != 'dead'])

    if target.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(monster.monster_name))

    # 16.67% chance for the enemy to give a status ailment
    if target.status_ail == "none" and random.randint(0, 5) == 0:
        monster.give_status(target)

    elif monster.hp <= monster.max_hp/5 and monster.mp >= monster.max_mp*0.2:
        # Magic heal
        sounds.magic_healing.play()

        if 20 < monster.hp*0.2:
            monster.hp += monster.hp*0.2

        else:
            monster.hp += 20

        if monster.hp > monster.max_hp:
            monster.hp = monster.max_hp

        print('The {0} casts a healing spell!'.format(monster.monster_name))

        monster.mp -= monster.max_mp*0.2

    elif monster.mp >= monster.max_mp*0.15:
        # Magic Attack
        sounds.magic_attack.play()

        print('The {0} is preparing to cast a damaging spell on {1}'.format(monster.monster_name, target.name))
        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
            dam_dealt = magic.eval_element(p_elem=target.element, m_elem=monster.element,
                                           m_dmg=monster.magical_damage(target))[1]

            print("The {0}'s spell succeeds, and deals {1} damage to {2}!".format(monster.monster_name, dam_dealt, target.name))

            target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print("The {0}'s spell narrowly misses {1}!".format(monster.monster_name, target.name))

        monster.mp -= monster.max_mp*0.15

    else:
        # Non-magic Attack

        print('The {0} {1} {2}'.format(monster.monster_name, monster.attk_msg, target.name))
        sounds.aim_weapon.play()

        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
            dam_dealt = magic.eval_element(p_elem=target.element, m_elem=monster.element,
                                           m_dmg=monster.physical_damage('pierce', target))[1]

            print("The {0}'s attack lands, dealing {1} damage to {2}!".format(monster.monster_name, dam_dealt, target.name))

            target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print("The {0}'s attack narrowly misses {1}!".format(monster.monster_name, target.name))

    monster.check_poison()
    monster.mp = math.ceil(monster.mp)


def ranged_ai():
    global monster

    battle.turn_counter += 1

    target = random.choice([x for x in [
        main.player,
        main.solou,
        main.xoann,
        main.randall,
        main.ran_af,
        main.parsto,
        main.adorine
    ] if x.enabled and x.status_ail != 'dead'])

    if target.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(monster.monster_name))

    # At the moment, Ranged monsters are only capable of attacking
    print('The {0} {1} {2}'.format(monster.monster_name, monster.attk_msg, target.name))
    sounds.aim_weapon.play()

    main.smart_sleep(0.75)

    if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
        dam_dealt = magic.eval_element(p_elem=target.element, m_elem=monster.element,
                                       m_dmg=monster.physical_damage('pierce', target))[1]

        print("The {0}'s attack lands, dealing {1} damage to {2}!".format(monster.monster_name, dam_dealt, target.name))

        target.hp -= dam_dealt
        sounds.enemy_hit.play()

    else:
        sounds.attack_miss.play()
        print("The {0}'s attack narrowly misses {1}!".format(monster.monster_name, target.name))

    monster.check_poison()


def melee_ai():
    global is_defending
    global monster

    battle.turn_counter += 1

    target = random.choice([x for x in [
        main.player,
        main.solou,
        main.xoann,
        main.randall,
        main.ran_af,
        main.parsto,
        main.adorine
    ] if x.enabled and x.status_ail != 'dead'])

    if is_defending:
        # Set defense back to normal
        is_defending = False

        monster.dfns /= 1.5
        monster.m_dfns /= 1.5
        monster.p_dfns /= 1.5
        monster.dfns = math.floor(monster.dfns)
        monster.m_dfns = math.floor(monster.m_dfns)
        monster.p_dfns = math.floor(monster.p_dfns)

    if target.spd >= monster.spd:
        print('-'*25)

    print('\n-Enemy Turn-')
    print(ascii_art.monster_art[monster.monster_name] % "The {0} is making a move!\n".format(monster.monster_name))

    # Melee monsters have a 1 in 5 (20%) chance to defend
    if random.randint(0, 4) == 0:
        is_defending = True
        sounds.buff_spell.play()

        # Scaling Defense
        monster.dfns *= 1.5
        monster.m_dfns *= 1.5
        monster.p_dfns *= 1.5

        monster.dfns = math.ceil(monster.dfns)
        monster.p_dfns = math.ceil(monster.p_dfns)
        monster.m_dfns = math.ceil(monster.m_dfns)

        print("The {0} defends itself from further attacks! (Enemy Defense Raised!)".format(monster.monster_name))

    # If the monster doesn't defend, then it will attack!
    else:
        print('The {0} {1} {2}'.format(monster.monster_name, monster.attk_msg, target.name))
        sounds.sword_slash.play()

        main.smart_sleep(0.75)

        if random.randint(1, 512) in range(battle.temp_stats[target.name]['evad'], 512):
            dam_dealt = magic.eval_element(p_elem=target.element, m_elem=monster.element,
                                           m_dmg=monster.physical_damage('melee', target))[1]

            print("The {0}'s attack lands, dealing {1} damage to {2}!".format(monster.monster_name, dam_dealt, target.name))

            target.hp -= dam_dealt
            sounds.enemy_hit.play()

        else:
            sounds.attack_miss.play()
            print("The {0}'s attack narrowly misses {1}!".format(monster.monster_name, target.name))

    monster.check_poison()


def spawn_monster():
    global monster

    monster = Monster('', 10, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1)
    monster.monst_name()
    monster.monst_level()

    if monster.evad > 256:
        monster.evad = 256
