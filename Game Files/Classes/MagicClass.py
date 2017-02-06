#   This file is part of Peasants' Ascension.
#
#    Peasants' Ascension is free software: you can redistribute it and/or modify
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

import sys
import json
import random
import time
import math
import pygame

import units
import battle
import inv_system
import sounds
import ascii_art

# THIS IF FOR AUTOMATED BUG-TESTING!!
# THIS SHOULD BE COMMENTED OUT FOR NORMAL USE!!
# def test_input(string):
#    spam = random.choice('0123456789ynxpsewrt')
#    print(string, spam)
#    return spam
#
# input = test_input

if __name__ == "__main__":
    sys.exit()

else:
    main = sys.modules["__main__"]

pygame.mixer.pre_init(frequency=44100)
pygame.mixer.init()

# This is the message that is printed if you attempt to use magic
# without the required amount of mana.
out_of_mana = """-------------------------
You don't have enough mana to cast that spell!"""


class Spell:
    def __init__(self, name, desc, mana, req_lvl, a_c=('mage',)):
        self.name = name
        self.desc = desc
        self.mana = mana
        self.req_lvl = req_lvl
        self.a_c = a_c  # These are the classes that are able to obtain this spell

    def __str__(self):
        return self.name

    def use_mana(self, user):
        user.mp -= self.mana
        if user.mp < 0:
            user.mp = 0


class Healing(Spell):
    # Healing spells are spells that restore your HP during battle
    def __init__(self, name, desc, mana, req_lvl, health, thresh, a_c=('mage', 'paladin')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.health = health
        self.thresh = thresh

    def __str__(self):
        return self.name

    def use_magic(self, user, is_battle):
        if user.mp >= self.mana:
            print()
            Spell.use_mana(self, user)

            target_options = [x for x in [
                units.player,
                units.solou,
                units.xoann,
                units.adorine,
                units.ran_af,
                units.parsto,
                units.chyme] if x.enabled
            ]

            if len(target_options) == 1:
                target = user

            else:
                print("Select Target for {0}:".format(self.name))
                print("     ", "\n      ".join(["[{0}] {1}".format(int(num) + 1, character.name)
                                               for num, character in enumerate(target_options)]))

                while True:
                    target = input("Input [#]: ")
                    try:
                        target = int(target) - 1

                    except ValueError:
                        continue

                    try:
                        target = target_options[target]

                    except IndexError:
                        continue

                    break

            # Healing spells will always restore a minimum of user.hp*thresh.
            # e.g. A spell that heals 20 HP but has a 20% threshold will restore 20 HP for someone
            # with 45 max HP, but will restore 32 HP for someone with 160 max HP.
            # In addition to this, the user restores an additional 2*Wisdom, unless they are a
            # Paladin in which case it it 4*Wisdom.
            if self.health < target.hp*self.thresh:
                total_heal = target.hp*self.thresh + \
                    (4*user.attributes['wis'] if user.class_ == 'paladin' else 2*user.attributes['wis'])

                target.hp += total_heal
                target.hp = math.ceil(target.hp)

            else:
                total_heal = self.health + (2*user.attributes['wis'] if user.class_ !=
                                            'paladin' else 4*user.attributes['wis'])
                target.hp += total_heal

            # Handle HP higher than max due to overheal
            if target.hp > target.max_hp:
                target.hp -= (target.hp - target.max_hp)

            sounds.magic_healing.play()

            if is_battle:
                # Print the ASCII art and "User Turn" info if a battle is going on
                print("-{0}'s Turn-")
                print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            print('Using "{0}", {1} is healed by {2} HP!'.format(self.name, target.name, total_heal))

            return True

        else:
            # Disallow the usage of spells if the player has insufficent MP
            print(out_of_mana)
            return False


class Damaging(Spell):
    # Damaging spells are spells that deal damage to the enemy during battle.
    # Just like normal attacks, they have a chance to miss based on
    # the enemy's evade stat.
    def __init__(self, name, desc, mana, req_lvl, damage, element, a_c=('mage',)):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.damage = damage
        self.element = element

    def __str__(self):
        return self.name

    def use_magic(self, user):
        inv_name = user.name if user != units.player else 'player'

        # Spells cannot be cast if the player does not have enough mana for it
        if user.mp >= self.mana:
            print()
            Spell.use_mana(self, user)

            # Determine the power of the attack
            dam_dealt = math.ceil(battle.temp_stats[user.name]['m_attk'] - units.monster.m_dfns/2)

            if user.class_ == 'mage':
                dam_dealt *= 1.5

            dam_dealt *= 1 + self.damage
            dam_dealt = math.ceil(dam_dealt)

            # Evaluate the element of the attack and the enemy
            dam_dealt = eval_element(
                p_elem=self.element,
                m_elem=units.monster.element,
                p_dmg=dam_dealt)[0]

            if dam_dealt < 1:
                dam_dealt = 1

            print("-{0}'s Turn-".format(user.name))
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")

            if inv_system.equipped[inv_name]['weapon'].class_ == 'magic':
                print('{0} begins to use their {1} to summon a powerful spell...'.format(
                    user.name, inv_system.equipped[inv_name]['weapon']))

            else:
                print('{0} attempts to summon a powerful spell...'.format(user.name))

            sounds.magic_attack.play()
            main.smart_sleep(0.75)

            # If the monster's evasion (with a max of 256) is higher than the user's accuracy roll,
            # the spell will land
            if random.randint(1, 512) in range(units.monster.evad, 512):
                sounds.enemy_hit.play()

                # Mages have a 15% chance to get a critical hit, whereas other classes cannot
                if random.randint(0, 100) <= (15 if user.class_ == 'mage' else -1):
                    dam_dealt *= 1.5
                    print("It's a critical hit! 1.5x damage!")

                    sounds.critical_hit.play()
                    main.smart_sleep(0.5)

                print('Using the power of "{0}", {1} deals {2} damage to the {3}!'.format(
                    self.name, user.name, dam_dealt, units.monster.monster_name))

                units.monster.hp -= dam_dealt

            # Otherwise, the spell with miss and deal no damage
            else:
                sounds.attack_miss.play()
                print("The {0} narrowly dodges {1}'s spell!".format(units.monster.monster_name, user.name))

            return True

        else:
            print(out_of_mana)
            return False


class Buff(Spell):
    # Buffs are spells that temporarily raise the player's stats
    # during battle. They last until the battle is over, at which
    # point the player's stats will return to normal.
    def __init__(self, name, desc, mana, req_lvl, increase, stat, a_c=('mage', 'monk')):
        Spell.__init__(self, name, desc, mana, req_lvl, a_c)
        self.increase = increase
        self.stat = stat

    def __str__(self):
        return self.name

    def use_magic(self, user):
        if user.mp >= self.mana:
            Spell.use_mana(self, user)

            print(f"\n-{user.name}'s Turn-")
            print(ascii_art.player_art[user.class_.title()] % f"{user.name} is making a move!\n")
            print(f'{user.name} raises their stats using the power of {self.name}!')

            sounds.buff_spell.play()

            battle.temp_stats[user.name][self.stat] *= 1 + self.increase
            battle.temp_stats[user.name][self.stat] = math.ceil(battle.temp_stats[user.name][self.stat])
            units.fix_stats()

            return True

        else:
            print(out_of_mana)
            return False
